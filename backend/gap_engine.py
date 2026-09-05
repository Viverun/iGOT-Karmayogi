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
from ontology import target_profile, area_type, CHAPTER_TITLES, DEFAULT_TARGET

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


def competency_vector(user_id: int, department_key: str) -> list:
    """Current vector (assessment + quizzes + completed-course boosts) vs targets."""
    targets = target_profile(department_key)
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

    areas = sorted(set(targets) | set(current), key=lambda a: a.lower())
    return [{
        "area": a,
        "type": area_type(a),
        "current": round(current.get(a, 0), 1),
        "target": targets.get(a, DEFAULT_TARGET if a in current else 0),
        "gap": round(max(0, targets.get(a, DEFAULT_TARGET if a in current else 0) - current.get(a, 0)), 1),
    } for a in areas]


def _verified_course_completions(user_id: int) -> int:
    """Courses completed with a solid quiz record (avg quiz score >= 60).
    Merely finishing videos isn't enough — the quizzes back it up."""
    conn = get_db()
    rows = conn.execute(
        "SELECT course_id, AVG(quiz_score) AS avg_score FROM chapter_progress "
        "WHERE user_id=? GROUP BY course_id", (user_id,)).fetchall()
    conn.close()
    conn2 = get_db()
    completed = {r["course_id"] for r in conn2.execute(
        "SELECT course_id FROM enrollments WHERE user_id=? AND status='completed'", (user_id,)).fetchall()}
    conn2.close()
    return sum(1 for r in rows
               if r["course_id"] in completed and r["avg_score"] is not None and r["avg_score"] >= 60)


def compute_gaps(user_id: int, department_key: str) -> dict:
    vector = competency_vector(user_id, department_key)
    scored = [v for v in vector if v["target"] > 0]

    # evidence-based readiness:
    #  - per-area contribution is clamped at the role target (overshooting a
    #    target in one area can't hide a gap in another)
    #  - assessments/quizzes alone can only demonstrate up to 30% readiness;
    #    beyond that, readiness grows only through VERIFIED course completions
    #    (course finished + avg quiz score >= 60), +14% each, capped at 100
    base = round(100 * sum(min(v["current"], v["target"]) for v in scored)
                 / max(1, sum(v["target"] for v in scored)))
    verified = _verified_course_completions(user_id)
    cap = min(100, 30 + 14 * verified)
    readiness = min(base, cap)

    overall_current = round(sum(v["current"] for v in scored) / max(1, len(scored)), 1)
    overall_target = round(sum(v["target"] for v in scored) / max(1, len(scored)), 1)
    gaps = sorted(scored, key=lambda v: v["gap"], reverse=True)
    worst = [g for g in gaps if g["gap"] > 0]
    explanations = [
        f"{g['area']}: current {g['current']}/100 vs role target {g['target']}/100 — "
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
        reasons = [f"Closes '{a}' (gap {severity[a]:.0f} pts)" for a in overlap]
        scored_courses.append((weight - prereq_penalty, c, reasons))

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
