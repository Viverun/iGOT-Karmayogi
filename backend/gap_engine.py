"""Competency gap engine + personalized roadmap recommender.

Persistent memory model:
- user_competency stores each area's skill level (0-100), EWMA-updated whenever
  the user takes an assessment or a quiz.
- Courses completed via the (dummy) iGOT connector boost the areas they tag.
- Gap = max(0, target - current) per area, weighted by how central the area is
  to the department profile. The roadmap sequences catalogue courses to close
  the highest-weighted gaps first (foundations before advanced).
"""
import json
import random

from db import get_db
from ontology import target_profile, area_type, CHAPTER_TITLES, DEFAULT_TARGET, ROLE_PROFILES, role_profile

# Bloom-ish difficulty ordering for prerequisite sequencing
LEVEL_ORDER = {"Basic": 0, "Intermediate": 1, "Advanced": 2}


def update_competency(user_id: int, area_scores: dict):
    """EWMA merge of new evidence into persistent skill levels."""
    conn = get_db()
    for area, pct in area_scores.items():
        row = conn.execute("SELECT score FROM user_competency WHERE user_id=? AND area=?",
                           (user_id, area)).fetchone()
        new = round(0.6 * row["score"] + 0.4 * pct, 1) if row else round(pct, 1)
        conn.execute(
            "INSERT INTO user_competency (user_id, area, score, updated_at) VALUES (?,?,?,datetime('now')) "
            "ON CONFLICT(user_id, area) DO UPDATE SET score=?, updated_at=datetime('now')",
            (user_id, area, new, new))
    conn.commit()
    conn.close()


def log_event(user_id: int, etype: str, detail: dict):
    conn = get_db()
    conn.execute("INSERT INTO learning_events (user_id, etype, detail_json) VALUES (?,?,?)",
                 (user_id, etype, json.dumps(detail)))
    conn.commit()
    conn.close()


def get_active_swaps(user_id: int) -> dict:
    """original_key -> replacement_key for every course this learner has
    downgraded to a foundational alternative."""
    conn = get_db()
    rows = conn.execute(
        "SELECT original_key, replacement_key FROM course_swaps WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return {r["original_key"]: r["replacement_key"] for r in rows}


def swap_roadmap_course(user_id: int, original_key: str, reason: str = "") -> dict:
    """Downgrade a core roadmap course to its foundational easier_alt.
    Called by the learner chatbot when someone says a course is too hard.
    Returns the replacement course dict, or raises ValueError if the course
    has no easier alternative defined."""
    import roadmap_data
    course = roadmap_data.get_course(original_key)
    if not course:
        raise ValueError(f"Unknown course '{original_key}'")
    replacement_key = course.get("easier_alt")
    if not replacement_key:
        raise ValueError(f"'{course['name']}' has no foundational alternative yet")
    replacement = roadmap_data.get_course(replacement_key)
    conn = get_db()
    conn.execute(
        "INSERT INTO course_swaps (user_id, original_key, replacement_key, reason, created_at) "
        "VALUES (?,?,?,?,datetime('now')) "
        "ON CONFLICT(user_id, original_key) DO UPDATE SET replacement_key=excluded.replacement_key, "
        "reason=excluded.reason, created_at=datetime('now')",
        (user_id, original_key, replacement_key, reason))
    conn.commit()
    conn.close()
    log_event(user_id, "roadmap_course_swapped",
              {"original": original_key, "replacement": replacement_key, "reason": reason})
    return replacement


def revert_roadmap_course(user_id: int, original_key: str):
    """Undo a swap — go back to the core course."""
    conn = get_db()
    conn.execute("DELETE FROM course_swaps WHERE user_id=? AND original_key=?", (user_id, original_key))
    conn.commit()
    conn.close()
    log_event(user_id, "roadmap_course_swap_reverted", {"original": original_key})
    conn.close()


def competency_vector(user_id: int, department_key: str, role_id: str | None = None,
                      *, prefetch: dict | None = None) -> list:
    """Current vector (assessment + quizzes + completed-course boosts) vs targets.

    `prefetch` (from bulk_context) lets a caller that needs this for many users
    — /api/admin/analytics — supply already-loaded rows instead of issuing two
    queries per user."""
    targets = target_profile(department_key, role_id)
    if prefetch is not None:
        rows = prefetch["competency"].get(user_id, [])
        completed = list(prefetch["completed"].get(user_id, []))
    else:
        conn = get_db()
        rows = conn.execute("SELECT area, score FROM user_competency WHERE user_id=?", (user_id,)).fetchall()
        completed = [r["course_id"] for r in conn.execute(
            "SELECT course_id FROM enrollments WHERE user_id=? AND status='completed'", (user_id,)).fetchall()]
        conn.close()

    from main import COURSES_BY_ID  # catalogue tags
    boosts = {}
    for cid in completed:
        for area in COURSES_BY_ID.get(cid, {}).get("competencyAreas", []):
            boosts[area] = boosts.get(area, 0) + 12  # +12 per completed course, capped below

    current = {r["area"]: r["score"] for r in rows}
    for area, b in boosts.items():
        current[area] = min(100, current.get(area, 40) + b)

    # ML primary: blend the Kaggle-trained XGBoost estimate 50/50 with the
    # EWMA store when the artifact + evidence exist. The SAME core runs for
    # single-user and bulk (admin) paths — only the evidence loading differs —
    # so dashboard and analytics can never disagree. Any failure -> EWMA.
    ml_source = {}
    try:
        import ml_scorers as ml
        if ml.xgb_available():
            evidence = (_evidence_from_prefetch(prefetch, user_id)
                        if prefetch is not None else _load_evidence(user_id))
            ml_source = _ml_blend_core(department_key, role_id, targets,
                                       current, evidence)
            for area, score in ml_source.items():
                current[area] = score
    except Exception as e:
        print("gap_engine: ml blend skipped, ewma fallback:", e)
        ml_source = {}

    areas = sorted(set(targets) | set(current), key=lambda a: a.lower())
    return [{
        "area": a,
        "type": area_type(a),
        "current": round(current.get(a, 0), 1),
        "target": targets.get(a, DEFAULT_TARGET if a in current else 0),
        "gap": round(max(0, targets.get(a, DEFAULT_TARGET if a in current else 0) - current.get(a, 0)), 1),
        "source": "xgb-blend" if a in ml_source else "ewma",
    } for a in areas]


def _load_evidence(user_id: int) -> dict:
    """Single-user evidence for the XGB blend (2 small queries)."""
    import json as _json
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT scores_json FROM assessment_results WHERE user_id=? "
            "ORDER BY id DESC LIMIT 1", (user_id,)).fetchone()
        assessed = _json.loads(row["scores_json"]) if row else {}
        quiz_rows = conn.execute(
            "SELECT course_id, AVG(quiz_score) AS avg_score FROM chapter_progress "
            "WHERE user_id=? GROUP BY course_id", (user_id,)).fetchall()
        avgs = [r["avg_score"] for r in quiz_rows if r["avg_score"] is not None]
        urow = conn.execute(
            "SELECT work_experience_years FROM users WHERE id=?", (user_id,)).fetchone()
        exp_yrs = float(urow["work_experience_years"] or 0) if urow else 0.0
    finally:
        conn.close()
    return {"assessed": assessed,
            "quiz_mean": (sum(avgs) / len(avgs)) if avgs else None,
            "exp_yrs": exp_yrs}


def _evidence_from_prefetch(prefetch: dict, user_id: int) -> dict:
    """Same evidence shape, sourced from bulk_context (no extra queries)."""
    assessed = prefetch.get("assessed", {}).get(user_id, {})
    rows = prefetch.get("chapters", {}).get(user_id, [])
    avgs = [r["avg_score"] for r in rows if r["avg_score"] is not None]
    return {"assessed": assessed,
            "quiz_mean": (sum(avgs) / len(avgs)) if avgs else None,
            "exp_yrs": float(prefetch.get("experience", {}).get(user_id, 0) or 0)}


def _ml_blend(user_id: int, department_key: str, role_id: str | None,
              targets: dict, current: dict) -> dict:
    """Legacy single-path entry (kept for tests): load + blend."""
    return _ml_blend_core(department_key, role_id, targets, current,
                          _load_evidence(user_id))


def _ml_blend_core(department_key: str, role_id: str | None,
                   targets: dict, current: dict, evidence: dict) -> dict:
    """XGBoost competency estimates per area, 0-100. Returns {} if unusable."""
    import ml_scorers as ml
    if not ml.xgb_available():
        return {}
    assessed = evidence.get("assessed") or {}
    quiz_mean = evidence.get("quiz_mean")
    exp_yrs = float(evidence.get("exp_yrs") or 0)
    from ontology import COMPETENCY_TYPE
    skill_order = sorted(COMPETENCY_TYPE)
    out = {}
    for area, target in targets.items():
        a_score = float(assessed.get(area, current.get(area, 50)))
        q_score = float(quiz_mean if quiz_mean is not None else a_score)
        channels = 1 + (1 if quiz_mean is not None else 0) + (1 if area in assessed else 0)
        ev = {
            "required_level": max(1.0, min(5.0, target / 20.0)),
            "assessment_score": a_score,
            "quiz_score": q_score,
            "practical_score": a_score,
            "assessment_reliability": 0.85,
            "evidence_completeness": channels / 3.0,
            "evidence_count": min(3, channels),
            "evidence_confidence": 0.9 * channels / 3.0,
            "recency_weight": 0.8,
            "experience_years": exp_yrs,
            "skill_id": skill_order.index(area) % 40 if area in skill_order else 0,
            "role_id": ml.stable_idx(role_id or department_key, 60),
        }
        pred = ml.predict_competency(ev)
        if pred is None:
            continue
        ml100 = max(0.0, min(100.0, pred * 20.0))
        out[area] = round(0.5 * current.get(area, 50) + 0.5 * ml100, 1)
    return out


def bulk_context(user_ids) -> dict:
    """Load everything compute_gaps() needs for MANY users in 3 queries instead
    of ~4 per user. Pass the result as compute_gaps(..., prefetch=...).

    /api/admin/analytics computes readiness for every registered user; done one
    user at a time that is ~5 Supabase round-trips each, which took ~3 minutes
    at 64 users and grew with every new signup."""
    ids = list(user_ids)
    empty = {"competency": {}, "completed": {}, "chapters": {},
             "assessed": {}, "experience": {}}
    if not ids:
        return empty
    conn = get_db()
    try:
        competency, completed, chapters = {}, {}, {}
        for r in conn.execute(
                "SELECT user_id, area, score FROM user_competency WHERE user_id = ANY(?)",
                (ids,)).fetchall():
            competency.setdefault(r["user_id"], []).append(r)
        for r in conn.execute(
                "SELECT user_id, course_id FROM enrollments "
                "WHERE status='completed' AND user_id = ANY(?)", (ids,)).fetchall():
            completed.setdefault(r["user_id"], []).append(r["course_id"])
        for r in conn.execute(
                "SELECT user_id, course_id, AVG(quiz_score) AS avg_score, COUNT(*) AS n_modules "
                "FROM chapter_progress WHERE user_id = ANY(?) GROUP BY user_id, course_id",
                (ids,)).fetchall():
            chapters.setdefault(r["user_id"], []).append(r)
        # ML-blend evidence (same signals as the single-user path):
        # latest assessment scores + years of experience per user.
        import json as _json
        for r in conn.execute(
                "SELECT DISTINCT ON (user_id) user_id, scores_json FROM assessment_results "
                "WHERE user_id = ANY(?) ORDER BY user_id, id DESC",
                (ids,)).fetchall():
            try:
                empty["assessed"][r["user_id"]] = _json.loads(r["scores_json"])
            except Exception:
                empty["assessed"][r["user_id"]] = {}
        for r in conn.execute(
                "SELECT id, work_experience_years FROM users WHERE id = ANY(?)",
                (ids,)).fetchall():
            empty["experience"][r["id"]] = r["work_experience_years"] or 0
    finally:
        conn.close()
    return {"competency": competency, "completed": completed, "chapters": chapters,
            "assessed": empty["assessed"], "experience": empty["experience"]}


def verified_completions_detail(user_id: int, *, prefetch: dict | None = None) -> dict:
    """Courses completed with a solid quiz record (avg quiz score >= 60).
    Merely finishing videos isn't enough — the quizzes back it up.

    Two course families feed this: iGOT catalogue courses (verified against
    `enrollments.status='completed'`) and roadmap courses (verified by having
    a graded chapter_progress row — course_id 'roadmap:<key>' — for every
    module the course actually has, per roadmap_data). Returns both the count
    and which specific courses qualified, so callers (e.g. the dashboard's
    "learning hours" / "X of Y courses" stats) can total up roadmap-course
    hours too, not just iGOT-catalogue ones."""
    import roadmap_data

    if prefetch is not None:
        rows = prefetch["chapters"].get(user_id, [])
        completed_igot = set(prefetch["completed"].get(user_id, []))
    else:
        conn = get_db()
        rows = conn.execute(
            "SELECT course_id, AVG(quiz_score) AS avg_score, COUNT(*) AS n_modules "
            "FROM chapter_progress WHERE user_id=? GROUP BY course_id", (user_id,)).fetchall()
        completed_igot = {r["course_id"] for r in conn.execute(
            "SELECT course_id FROM enrollments WHERE user_id=? AND status='completed'", (user_id,)).fetchall()}
        conn.close()

    roadmap_keys, igot_ids = [], []
    for r in rows:
        if r["avg_score"] is None or r["avg_score"] < 60:
            continue
        course_id = r["course_id"]
        if isinstance(course_id, str) and course_id.startswith("roadmap:"):
            key = course_id.split(":", 1)[1]
            course = roadmap_data.get_course(key)
            if course and r["n_modules"] >= len(course["modules"]):
                roadmap_keys.append(key)
        elif course_id in completed_igot:
            igot_ids.append(course_id)
    return {"count": len(roadmap_keys) + len(igot_ids), "roadmap_keys": roadmap_keys, "igot_ids": igot_ids}


def _verified_course_completions(user_id: int) -> int:
    return verified_completions_detail(user_id)["count"]


def compute_gaps(user_id: int, department_key: str, role_id: str | None = None,
                 *, prefetch: dict | None = None) -> dict:
    vector = competency_vector(user_id, department_key, role_id, prefetch=prefetch)
    scored = [v for v in vector if v["target"] > 0]

    # evidence-based readiness:
    #  - per-area contribution is clamped at the role target (overshooting a
    #    target in one area can't hide a gap in another)
    #  - assessments/quizzes alone can only demonstrate up to 30% readiness;
    #    beyond that, readiness grows only through VERIFIED course completions
    #    (course finished + avg quiz score >= 60), +14% each, capped at 100
    base = round(100 * sum(min(v["current"], v["target"]) for v in scored)
                 / max(1, sum(v["target"] for v in scored)))
    verified = verified_completions_detail(user_id, prefetch=prefetch)["count"]
    cap = min(100, 30 + 14 * verified)
    readiness = min(base, cap)

    overall_current = round(sum(v["current"] for v in scored) / max(1, len(scored)), 1)
    overall_target = round(sum(v["target"] for v in scored) / max(1, len(scored)), 1)
    gaps = sorted(scored, key=lambda v: v["gap"], reverse=True)
    worst = [g for g in gaps if g["gap"] > 0]
    role_note = ""
    if role_id and role_id in ROLE_PROFILES:
        role_note = f" for role '{ROLE_PROFILES[role_id]['title']}'"
    explanations = [
        f"{g['area']}: current {g['current']}/100 vs target {g['target']}/100{role_note} — "
        f"gap of {g['gap']} points ({g['type']} competency)."
        for g in worst[:5]
    ]
    return {
        "vector": vector,
        "overall_current": overall_current,
        "overall_target": overall_target,
        "readiness_pct": readiness,
        "readiness_cap": cap,
        "verified_completions": verified,
        "top_gaps": worst[:5],
        "explanations": explanations,
    }


def course_areas(course: dict) -> set:
    return set(course["competencyAreas"])


def build_roadmap(user_id: int, department_key: str, courses: list, gaps: dict,
                  completed_ids: set) -> dict:
    """Phase-sequenced plan: close highest-severity gaps first, Basic before Advanced."""
    enrolled = _enrolled_ids(user_id)
    severity = {g["area"]: g["gap"] for g in gaps["top_gaps"]}
    scored_courses = []
    for c in courses:
        if c["identifier"] in completed_ids:
            continue
        overlap = course_areas(c) & set(severity)
        if not overlap:
            continue
        weight = sum(severity[a] for a in overlap) / max(1, len(overlap))
        prereq_penalty = 0
        if LEVEL_ORDER[c["level"]] > 0:
            # penalize advanced courses in areas the user hasn't done basics for
            for a in overlap:
                if not any(x["identifier"] in completed_ids | enrolled
                           and c["identifier"] != x["identifier"]
                           and LEVEL_ORDER[x["level"]] < LEVEL_ORDER[c["level"]]
                           and a in course_areas(x) for x in courses):
                    prereq_penalty += 10
        cur = {g["area"]: g for g in gaps["vector"]}
        reasons = [
            (f"{a}: measured {cur[a]['current']:.0f}/100 against target {cur[a]['target']}/100 — "
             f"closes a {severity[a]:.0f}-point gap ({cur[a]['type']} competency)")
            for a in overlap
        ]
        scored_courses.append((weight - prereq_penalty, c, reasons))

    # ML primary: Hybrid-NCF rerank blend (60% rule / 40% NCF). Any failure
    # (no torch, no weights) keeps the rule-based order above.
    try:
        scored_courses = _ncf_rerank(user_id, scored_courses, severity)
    except Exception as e:
        print("gap_engine: ncf rerank skipped, rule-based fallback:", e)

    scored_courses.sort(key=lambda t: t[0], reverse=True)
    phases = {"1": [], "2": [], "3": []}
    for _, c, reasons in scored_courses:
        lv = LEVEL_ORDER[c["level"]]
        phase = "1" if lv == 0 else ("2" if lv == 1 else "3")
        phases[phase].append({
            "course_id": c["identifier"], "name": c["name"], "provider": c["provider"],
            "level": c["level"], "durationMinutes": c["durationMinutes"],
            "competencyAreas": c["competencyAreas"], "reasons": reasons,
        })
    roadmap = {
        "phases": [
            {"phase": 1, "title": "Foundations — close critical basic gaps", "courses": phases["1"]},
            {"phase": 2, "title": "Core skills — role-relevant deepening", "courses": phases["2"]},
            {"phase": 3, "title": "Advanced — mastery & emerging tech", "courses": phases["3"]},
        ],
        "total_courses": sum(len(v) for v in phases.values()),
        "total_hours": round(sum(c["durationMinutes"] for _, c, _ in scored_courses) / 60, 1),
    }
    conn = get_db()
    conn.execute("INSERT INTO roadmaps (user_id, data_json, updated_at) VALUES (?,?,datetime('now')) "
                 "ON CONFLICT(user_id) DO UPDATE SET data_json=?, updated_at=datetime('now')",
                 (user_id, json.dumps(roadmap), json.dumps(roadmap)))
    conn.commit()
    conn.close()
    log_event(user_id, "roadmap_updated", {"total_courses": roadmap["total_courses"]})
    return roadmap


def _ncf_rerank(user_id: int, scored: list, severity: dict) -> list:
    """Blend rule weights with Hybrid-NCF scores. Returns original list if NCF off."""
    import ml_scorers as ml
    if not ml.ncf_available() or not scored:
        return scored
    wmax = max((w for w, _, _ in scored), default=1) or 1
    out = []
    for w, c, reasons in scored:
        overlap = course_areas(c) & set(severity)
        max_gap = max((severity[a] for a in overlap), default=0)
        ctx = {
            "gap_alignment_score": min(1.0, max_gap / 100.0),
            "prerequisite_fit": 1.0 if LEVEL_ORDER[c["level"]] == 0 else 0.6,
            "expected_gain": min(1.0, max(0.0, w) / 100.0),
            "completion_probability": 0.6,
            "novelty": 1.0,
        }
        s = ml.ncf_score(user_id, c["identifier"], ctx)
        if s is None:
            out.append((w, c, reasons))
            continue
        blended = 0.6 * w + 0.4 * s * 100.0
        out.append((blended, c, reasons + [
            f"ML-ranked (hybrid-NCF score {s:.2f})"]))
    return out


def _enrolled_ids(user_id: int) -> set:
    conn = get_db()
    rows = conn.execute("SELECT course_id FROM enrollments WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return {r["course_id"] for r in rows}


def chapters_for(course: dict) -> list:
    return [{"chapter_no": i + 1, "title": t,
             "areas": course["competencyAreas"],
             "durationMinutes": max(10, course["durationMinutes"] // len(CHAPTER_TITLES))}
            for i, t in enumerate(CHAPTER_TITLES)]


def pick_questions(bank: list, areas: list, n: int = 5, rng: random.Random | None = None) -> list:
    """Sample quiz questions for the given competency areas from a department bank."""
    rng = rng or random.Random()
    pool = [q for q in bank if q["area"] in areas] or bank
    picked = rng.sample(pool, min(n, len(pool)))
    return [{"id": q["id"], "qtype": q["qtype"], "area": q["area"],
             "text": q["text"], "options": q["options"]} for q in picked]
