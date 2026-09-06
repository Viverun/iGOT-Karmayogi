"""Dummy iGOT backend: fake auth + Sunbird-shaped catalogue/enrollment/progress APIs.

Endpoints the AI system will call (mirroring Sunbird ED contracts):
  POST /api/v1/content/search       -> course catalogue (Sunbird search shape)
  GET  /api/v1/content/read/{id}    -> single course (Sunbird read shape)
  POST /api/enrollments             -> enroll a user in a course
  GET  /api/enrollments             -> list a user's enrollments + progress
  PATCH /api/enrollments/{id}       -> update progress / toggle completion
Auth endpoints are deliberately dummy (no hashing/JWT): demo-only.
"""
import secrets
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import json
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from db import get_db, init_db, DEMO_USER
from assessment import questions_for, department_key, QUESTION_BANK
from ontology import CHAPTER_TITLES
from gap_engine import chapters_for
import gap_engine as ge
import materials as mat_engine
import llm
from llm import KNOWLEDGE_QUIZ_PROMPT

init_db()
COURSES = json.loads((Path(__file__).parent / "data" / "courses.json").read_text())
COURSES_BY_ID = {c["identifier"]: c for c in COURSES}

app = FastAPI(title="Dummy iGOT Karmayogi API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # demo only
    allow_methods=["*"],
    allow_headers=["*"],
)


def strength_weakness(area_scores: dict):
    """Weakness only exists if something was scored below 100; strength only if something scored above 0."""
    if not area_scores:
        return None, None
    smax = max(area_scores, key=area_scores.get)
    smin = min(area_scores, key=area_scores.get)
    strength = smax if area_scores[smax] > 0 else None
    weakness = smin if area_scores[smin] < 100 else None
    return strength, weakness


def transcript_context_for(query_text: str, videos: list, total: int = 55000) -> tuple[str, list]:
    """Context from Pinecone (semantic retrieval) first, raw cached transcripts second."""
    video_ids = [v["yt"] for v in videos if not v.get("playlist")]
    try:
        import vector_store
        hits = vector_store.query_transcripts(query_text, video_ids=video_ids, top_k=10)
        if hits:
            text = "\n\n---\n\n".join(h["text"] for h in hits)[:total]
            return text, list({h["video_id"] for h in hits})
    except Exception as e:
        print("vector transcript retrieval failed:", e)
    import transcripts as ts
    return ts.module_context(videos, total=total)


def sunbird_envelope(result: dict) -> dict:
    return {
        "id": "api.content.search",
        "ver": "3.0",
        "ts": datetime.now(timezone.utc).isoformat(),
        "params": {"resmsgid": str(uuid.uuid4()), "status": "successful", "errmsg": None},
        "responseCode": "OK",
        "result": result,
    }


def course_to_content(c: dict) -> dict:
    """Sunbird-ish content metadata fields."""
    return {
        "identifier": c["identifier"],
        "name": c["name"],
        "description": c["description"],
        "creator": c["provider"],
        "organisation": c["provider"],
        "duration": c["durationMinutes"] * 60,  # seconds, like Sunbird
        "level": c["level"],
        "competencyType": c["competencyType"],
        "competencyAreas": c["competencyAreas"],
        "status": "Live",
        "mimeType": "application/vnd.ekstep.html-archive",
        "primaryKey": "identifier",
    }


def require_user(auth_header: Optional[str]) -> int:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing bearer token")
    token = auth_header.removeprefix("Bearer ")
    conn = get_db()
    row = conn.execute(
        "SELECT user_id FROM tokens WHERE token = ?", (token,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(401, "Invalid token")
    return row["user_id"]


# ---------- Auth (dummy) ----------

class AuthBody(BaseModel):
    name: Optional[str] = None
    email: str
    password: str
    designation: Optional[str] = None
    department: Optional[str] = None


@app.post("/api/auth/register")
def register(body: AuthBody):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (name, email, password, designation, department) VALUES (?,?,?,?,?)",
            (body.name or body.email.split("@")[0], body.email, body.password,
             body.designation or "", body.department or ""),
        )
        conn.commit()
    except Exception:
        raise HTTPException(409, "User with this email already exists")
    finally:
        conn.close()
    return {"message": "Registered. You can sign in now.", "email": body.email}


@app.post("/api/auth/login")
def login(body: AuthBody):
    conn = get_db()
    row = conn.execute(
        "SELECT id, name, email, designation, department FROM users WHERE email = ? AND password = ?",
        (body.email, body.password),
    ).fetchone()
    if not row:
        conn.close()
        raise HTTPException(401, "Invalid email or password")
    token = secrets.token_hex(16)
    conn.execute("INSERT INTO tokens (token, user_id) VALUES (?,?)", (token, row["id"]))
    conn.commit()
    conn.close()
    return {
        "access_token": token,  # dummy token, not a real JWT
        "token_type": "bearer",
        "user": {k: row[k] for k in ("name", "email", "designation", "department")},
    }


class ResetDemoBody(BaseModel):
    email: str


@app.post("/api/auth/reset-demo")
def reset_demo(body: ResetDemoBody):
    """DEMO-ONLY: wipe ALL learning memory for the demo user so every
    registration starts a fresh session (assessments, progress, roadmap)."""
    conn = get_db()
    row = conn.execute("SELECT id FROM users WHERE email = ?", (body.email,)).fetchone()
    if row:
        uid = row["id"]
        for table in ("tokens", "learning_events", "chapter_progress", "lesson_quizzes",
                      "personalized_quizzes", "assessment_results", "user_competency",
                      "enrollments", "roadmaps"):
            conn.execute(f"DELETE FROM {table} WHERE user_id = ?", (uid,))
        conn.commit()
    conn.close()
    return {"message": "Demo session wiped — fresh start"}


@app.post("/api/auth/logout")
def logout(authorization: Optional[str] = Header(None)):
    """Invalidate the session token server-side."""
    if not authorization or not authorization.startswith("Bearer "):
        return {"message": "No active session"}
    token = authorization.removeprefix("Bearer ")
    conn = get_db()
    conn.execute("DELETE FROM tokens WHERE token = ?", (token,))
    conn.commit()
    conn.close()
    return {"message": "Logged out"}


@app.get("/api/auth/me")
def me(authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    conn = get_db()
    row = conn.execute(
        "SELECT name, email, designation, department FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return row


# ---------- Catalogue (Sunbird-shaped) ----------

@app.post("/api/v1/content/search")
def content_search(body: dict):
    query: str = (body.get("query") or "").lower()
    filters = body.get("filters") or {}
    results = COURSES
    if query:
        results = [c for c in results if query in c["name"].lower()
                   or query in c["provider"].lower()
                   or any(query in a.lower() for a in c["competencyAreas"])]
    if filters.get("competencyType"):
        results = [c for c in results if c["competencyType"] == filters["competencyType"]]
    if filters.get("level"):
        results = [c for c in results if c["level"] == filters["level"]]
    return sunbird_envelope({
        "count": len(results),
        "content": [course_to_content(c) for c in results],
    })


@app.get("/api/v1/content/read/{identifier}")
def content_read(identifier: str):
    c = COURSES_BY_ID.get(identifier)
    if not c:
        raise HTTPException(404, "Content not found")
    return sunbird_envelope({"content": course_to_content(c)})


# ---------- Enrollments & progress ----------

class EnrollBody(BaseModel):
    course_id: str


class ProgressBody(BaseModel):
    status: Optional[str] = None  # enrolled | in_progress | completed
    progress_pct: Optional[int] = None


class ChapterCompleteBody(BaseModel):
    answers: list[dict]


@app.post("/api/enrollments")
def enroll(body: EnrollBody, authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    if body.course_id not in COURSES_BY_ID:
        raise HTTPException(404, "Unknown course")
    conn = get_db()
    conn.execute(
        "INSERT OR IGNORE INTO enrollments (user_id, course_id) VALUES (?,?)",
        (user_id, body.course_id),
    )
    conn.commit()
    conn.close()
    return {"message": "Enrolled", "course_id": body.course_id, "status": "enrolled"}


@app.get("/api/enrollments")
def my_enrollments(authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    conn = get_db()
    rows = conn.execute(
        "SELECT id, course_id, status, progress_pct, updated_at FROM enrollments WHERE user_id = ?",
        (user_id,),
    ).fetchall()
    conn.close()
    return [
        {**dict(r), "course": course_to_content(COURSES_BY_ID[r["course_id"]])}
        for r in rows
    ]


@app.patch("/api/enrollments/{enrollment_id}")
def update_progress(enrollment_id: int, body: ProgressBody,
                    authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    status = body.status
    pct = body.progress_pct
    if status == "completed":
        pct = 100
    if pct is not None and status is None:
        status = "completed" if pct >= 100 else "in_progress"
    conn = get_db()
    cur = conn.execute(
        "UPDATE enrollments SET status = COALESCE(?, status), progress_pct = COALESCE(?, progress_pct),"
        " updated_at = datetime('now') WHERE id = ? AND user_id = ?",
        (status, pct, enrollment_id, user_id),
    )
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(404, "Enrollment not found")
    conn.commit()
    row = conn.execute("SELECT id, course_id, status, progress_pct FROM enrollments WHERE id = ?",
                       (enrollment_id,)).fetchone()
    conn.close()
    return dict(row)


# ---------- Personalized learning roadmap (on-site YouTube courses) ----------

@app.get("/api/roadmap")
def get_roadmap_api(authorization: Optional[str] = Header(None)):
    """On-site learning roadmap. Requires a completed assessment — no profile, no prescription."""
    user_id = require_user(authorization)
    dept, key = _user_department(user_id)
    conn = get_db()
    assessment_done = conn.execute(
        "SELECT COUNT(*) AS n FROM assessment_results WHERE user_id=?", (user_id,)).fetchone()["n"] > 0
    conn.close()
    if not assessment_done:
        return {"assessment_done": False, "courses": None,
                "message": "Take the competency assessment first — your roadmap is built from your measured gaps."}
    import roadmap_data
    courses = roadmap_data.get_roadmap(key)
    return {"assessment_done": True, "department": dept,
            "courses": [{"key": c["key"], "name": c["name"], "provider": c["provider"],
                         "badge": c["badge"], "level": c["level"], "hours": c["hours"],
                         "areas": c["areas"], "description": c["description"],
                         "modules": [{"title": m["title"], "video_count": len(m["videos"])}
                                     for m in c["modules"]]}
                        for c in courses]}


@app.get("/api/roadmap/{course_key}")
def get_roadmap_course(course_key: str, authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    conn = get_db()
    assessment_done = conn.execute(
        "SELECT COUNT(*) AS n FROM assessment_results WHERE user_id=?", (user_id,)).fetchone()["n"] > 0
    done_rows = conn.execute(
        "SELECT chapter_no, quiz_score FROM chapter_progress WHERE user_id=? AND course_id=?",
        (user_id, f"roadmap:{course_key}")).fetchall()
    lesson_scores = {f"{r['module_no']}:{r['video_no']}": r["score"]
                     for r in conn.execute(
        "SELECT module_no, video_no, score FROM lesson_quizzes WHERE user_id=? AND course_key=? AND score IS NOT NULL",
        (user_id, course_key)).fetchall()}
    conn.close()
    if not assessment_done:
        raise HTTPException(403, "Take the competency assessment before accessing your learning roadmap")
    import roadmap_data
    c = roadmap_data.get_course(course_key)
    if not c:
        raise HTTPException(404, "Course not found in your roadmap")
    done = {r["chapter_no"]: r["quiz_score"] for r in done_rows}
    return {**c,
            "completed_modules": {str(k): v for k, v in done.items()},
            "lesson_scores": lesson_scores,
            "progress_pct": round(100 * len(done) / max(1, len(c["modules"])))}


MODULE_QUIZ_PROMPT = """You are a subject-matter examiner for India's capacity-building programmes.
A learner just finished the module "{module_title}" (course: {course_name}) watching these video lectures.
Using ONLY the lecture transcripts below, write {n} multiple-choice questions that precisely test
comprehension of what the lectures actually taught. Tag each question with its difficulty level:
"L1" (easy/recall), "L2" (medium/applied) or "L3" (hard/analytical) — include a mix, roughly 2 L1, 2 L2, 1 L3.
For each question, set "area" to the CLOSEST match from this list: {areas}.
Return STRICT JSON: a list of objects with fields:
question, options (exactly 4 strings), correct_index (0-3), explanation, source_snippet (quote from the transcript), area, level.
Do not introduce facts not present in the transcripts. Vary the position of the correct answer.

Lecture transcripts:
{context}
"""


@app.post("/api/roadmap/{course_key}/module/{module_no}/quiz")
def roadmap_module_quiz(course_key: str, module_no: int, authorization: Optional[str] = Header(None)):
    """5-question quiz for a roadmap module, generated from the module's actual video transcripts."""
    user_id = require_user(authorization)
    import roadmap_data
    c = roadmap_data.get_course(course_key)
    if not c:
        raise HTTPException(404, "Course not found in your roadmap")
    if not 1 <= module_no <= len(c["modules"]):
        raise HTTPException(404, "Unknown module")
    module = c["modules"][module_no - 1]

    # reuse the stored quiz for retakes so grading stays consistent —
    # but self-upgrade a fallback quiz once transcripts + LLM are available
    conn = get_db()
    stored = conn.execute(
        "SELECT id, questions_json, generator FROM module_quizzes WHERE user_id=? AND course_key=? AND module_no=?",
        (user_id, course_key, module_no)).fetchone()
    conn.close()
    if stored and not (stored["generator"] == "fallback" and llm.llm_available()):
        return {"course_key": course_key, "module_no": module_no,
                "module_title": module["title"], "generator": stored["generator"],
                "questions": json.loads(stored["questions_json"])}
    if stored:
        conn = get_db()
        conn.execute("DELETE FROM module_quizzes WHERE id=?", (stored["id"],))
        conn.commit()
        conn.close()

    _, key = _user_department(user_id)
    questions, generator = [], "fallback"
    context, fetched = [], []
    try:
        import transcripts as ts
        query_text = f"{c['name']} — {module['title']}. Topics: {', '.join(c['areas'])}."
        context, fetched = transcript_context_for(query_text, module["videos"])
    except Exception as e:
        print("transcript fetch failed:", e)

    if context and llm.llm_available():
        try:
            from ontology import COMPETENCY_TYPE
            allowed = ", ".join(sorted(set(c["areas"]) | set(COMPETENCY_TYPE)))
            raw = llm.generate(MODULE_QUIZ_PROMPT.format(
                module_title=module["title"], course_name=c["name"], n=5,
                areas=allowed, context=context), max_tokens=6000)
            questions = llm.parse_llm_quiz(raw)[:5]
            for q in questions:
                q["level"] = q.get("level", "L2") if "level" in q else "L2"
            generator = "llm-transcript"
        except Exception as e:
            print("LLM module quiz failed:", e)

    if not questions and llm.llm_available():
        # transcripts unavailable (e.g. cloud egress blocked): still let the model
        # generate from the course/module metadata so learners always get fresh quizzes
        try:
            from ontology import COMPETENCY_TYPE
            allowed = ", ".join(sorted(set(c["areas"]) | set(COMPETENCY_TYPE)))
            meta_context = (f"Course: {c['name']}. Description: {c['description']}\n"
                            f"Module: {module['title']}. Lessons: "
                            + "; ".join(v["title"] for v in module["videos"])
                            + f".\nCompetency areas covered: {', '.join(c['areas'])}.")
            raw = llm.generate(KNOWLEDGE_QUIZ_PROMPT.format(
                n=5, areas=allowed, context=meta_context), max_tokens=6000)
            questions = llm.parse_llm_quiz(raw)[:5]
            for q in questions:
                q.setdefault("level", "L2")
            generator = "llm-knowledge"
        except Exception as e:
            print("knowledge-based generation failed:", e)

    if not questions:
        # bank fallback: pick_questions strips answers for client serving, so
        # re-attach the answer key from the bank before storing for grading
        bank_full = {q["id"]: q for q in QUESTION_BANK[key]}
        qs = ge.pick_questions(QUESTION_BANK[key], c["areas"], n=5)
        questions = [{**q, **({"answer": bank_full[q["id"]]["answer"]} if q["id"] in bank_full else {}),
                      "question": q["text"], "level": "L2"} for q in qs]

    conn = get_db()
    conn.execute("INSERT INTO module_quizzes (user_id, course_key, module_no, questions_json, generator) VALUES (?,?,?,?,?)",
                 (user_id, course_key, module_no, json.dumps(questions), generator))
    conn.commit()
    conn.close()
    return {"course_key": course_key, "module_no": module_no,
            "module_title": module["title"], "generator": generator,
            "transcript_videos_used": len(fetched),
            "questions": [{k: q[k] for k in ("id", "question", "options", "area", "level") if k in q}
                          for q in questions]}


@app.post("/api/roadmap/{course_key}/module/{module_no}/complete")
def roadmap_module_complete(course_key: str, module_no: int, body: ChapterCompleteBody,
                            authorization: Optional[str] = Header(None)):
    """Grade the module quiz against the stored transcript-grounded questions; feed memory."""
    user_id = require_user(authorization)
    import roadmap_data
    c = roadmap_data.get_course(course_key)
    if not c:
        raise HTTPException(404, "Course not found in your roadmap")
    if not 1 <= module_no <= len(c["modules"]):
        raise HTTPException(404, "Unknown module")

    conn = get_db()
    row = conn.execute(
        "SELECT questions_json FROM module_quizzes WHERE user_id=? AND course_key=? AND module_no=?",
        (user_id, course_key, module_no)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(400, "Take the module quiz first")

    bank = {q["id"]: q for q in json.loads(row["questions_json"])}
    per_area, correct = {}, 0
    for a in body.answers:
        q = bank.get(a.get("question_id"))
        if not q:
            continue
        ok = a.get("chosen") == q["answer"]
        correct += ok
        st = per_area.setdefault(q.get("area", "General"), {"correct": 0, "total": 0})
        st["total"] += 1
        st["correct"] += ok
    if not per_area:
        raise HTTPException(400, "No valid answers submitted")
    total_q = sum(v["total"] for v in per_area.values())
    score = round(100 * correct / total_q)
    area_scores = {area: round(100 * v["correct"] / v["total"]) for area, v in per_area.items()}

    conn = get_db()
    conn.execute(
        "INSERT INTO chapter_progress (user_id, course_id, chapter_no, quiz_score) VALUES (?,?,?,?) "
        "ON CONFLICT(user_id, course_id, chapter_no) DO UPDATE SET quiz_score=?, completed_at=datetime('now')",
        (user_id, f"roadmap:{course_key}", module_no, score, score))
    done = conn.execute("SELECT COUNT(*) AS n FROM chapter_progress WHERE user_id=? AND course_id=?",
                        (user_id, f"roadmap:{course_key}")).fetchone()["n"]
    conn.commit()
    conn.close()

    # persistent memory: module strengths/weaknesses feed the same competency vector
    ge.update_competency(user_id, area_scores)
    s_w = strength_weakness(area_scores)
    ge.log_event(user_id, "module_quiz_completed",
                 {"course_key": course_key, "module_no": module_no, "score": score,
                  "areas": list(area_scores), "strength": s_w[0], "weakness": s_w[1]})
    _, key = _user_department(user_id)
    gaps = ge.compute_gaps(user_id, key, _user_context(user_id)[2])
    ge.build_roadmap(user_id, key, COURSES, gaps, completed_ids=_completed_ids(user_id))

    strength, weakness = strength_weakness(area_scores)
    return {"module_score": score, "area_scores": area_scores,
            "strength": strength, "weakness": weakness,
            "course_progress_pct": round(100 * done / len(c["modules"])),
            "readiness_pct": gaps["readiness_pct"]}


@app.get("/api/health")
def health():
    return {"status": "ok", "demo_user": DEMO_USER["email"], "courses": len(COURSES)}


@app.on_event("startup")
def startup_indexing():
    try:
        import vector_store
        n = vector_store.index_courses(COURSES)
        print(f"course catalogue indexed into Pinecone ({n} vectors)")
    except Exception as e:
        print("Pinecone course indexing skipped:", e)
    _seed_mospi_library()


def _seed_mospi_library():
    """Pre-load official NSSTA/MoSPI manuals into the Trainer Studio library
    (shared rows with user_id=0) so MCQ generation can be demoed instantly."""
    import os
    data_dir = os.path.join(os.path.dirname(__file__), "data", "mospi")
    if not os.path.isdir(data_dir):
        return
    conn = get_db()
    # shared-library system user (id=0) so FK constraints hold
    conn.execute("INSERT OR IGNORE INTO users (id, name, email, password, designation, department) "
                 "VALUES (0, 'NSSTA Training Library', 'library@nssta.gov.in', '-', 'Library', 'NSSTA / MoSPI')")
    seeded = 0
    for fn in sorted(os.listdir(data_dir)):
        if not fn.endswith(".txt"):
            continue
        exists = conn.execute("SELECT id FROM materials WHERE filename=? AND user_id=0",
                              (fn,)).fetchone()
        if exists:
            continue
        text = open(os.path.join(data_dir, fn), encoding="utf-8", errors="ignore").read()
        conn.execute("INSERT INTO materials (user_id, filename, text) VALUES (0, ?, ?)", (fn, text))
        seeded += 1
    conn.commit()
    conn.close()
    if seeded:
        print(f"seeded {seeded} NSSTA/MoSPI manuals into the material library")


# ---------- Assessment (department-aware, scored server-side) ----------

class SubmitBody(BaseModel):
    answers: list[dict]  # [{question_id, chosen}]


@app.get("/api/assessment/questions")
def assessment_questions(authorization: Optional[str] = Header(None)):
    """Questions picked by the logged-in user's department (no answers exposed)."""
    user_id = require_user(authorization)
    conn = get_db()
    row = conn.execute("SELECT department FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    dept = row["department"] if row else ""
    qs = [{k: q[k] for k in ("id", "qtype", "area", "text", "options", "level")}
          for q in questions_for(dept)]
    return {"department": dept, "department_key": department_key(dept), "questions": qs}


@app.post("/api/assessment/submit")
def assessment_submit(body: SubmitBody, authorization: Optional[str] = Header(None)):
    """Grade against the question bank, store per-area scores, return them."""
    user_id = require_user(authorization)
    conn = get_db()
    row = conn.execute("SELECT department FROM users WHERE id = ?", (user_id,)).fetchone()
    dept = row["department"] if row else ""
    key = department_key(dept)
    bank = {q["id"]: q for q in QUESTION_BANK[key]}

    graded, per_area = [], {}
    for a in body.answers:
        q = bank.get(a.get("question_id"))
        if not q:
            continue
        chosen = a.get("chosen")
        correct = chosen == q["answer"]
        graded.append({"question_id": q["id"], "area": q["area"], "qtype": q["qtype"],
                       "chosen": chosen, "correct": correct})
        area = per_area.setdefault(q["area"], {"correct": 0, "total": 0})
        area["total"] += 1
        if correct:
            area["correct"] += 1
    scores = {area: round(100 * v["correct"] / v["total"]) for area, v in per_area.items()}
    overall = round(100 * sum(v["correct"] for v in per_area.values()) /
                    max(1, sum(v["total"] for v in per_area.values())))

    conn.execute(
        "INSERT INTO assessment_results (user_id, department_key, answers_json, scores_json) VALUES (?,?,?,?)",
        (user_id, key, json.dumps(graded), json.dumps(scores)),
    )
    conn.commit()
    conn.close()

    # Persistent memory: merge scores, log the event, refresh the roadmap.
    ge.update_competency(user_id, scores)
    ge.log_event(user_id, "assessed", {"department_key": key, "overall": overall})
    gaps = ge.compute_gaps(user_id, key, _user_context(user_id)[2])
    roadmap = ge.build_roadmap(user_id, key, COURSES, gaps,
                               completed_ids=_completed_ids(user_id))
    return {"overall": overall, "scores": scores, "answers": graded,
            "readiness_pct": gaps["readiness_pct"], "roadmap": roadmap}


def _user_department(user_id: int) -> tuple[str, str]:
    dept, key, _ = _user_context(user_id)
    return dept, key


def _user_context(user_id: int) -> tuple[str, str, str | None]:
    """(department, department_key, role_id) — role_id maps designation/department
    to a standard MoSPI role profile when one matches."""
    conn = get_db()
    row = conn.execute("SELECT designation, department FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    dept = (row["department"] if row else "") or ""
    desig = (row["designation"] if row else "") or ""
    from ontology import resolve_role_id
    return dept, department_key(dept), resolve_role_id(desig, dept)


def _completed_ids(user_id: int) -> set:
    conn = get_db()
    rows = conn.execute("SELECT course_id FROM enrollments WHERE user_id=? AND status='completed'",
                        (user_id,)).fetchall()
    conn.close()
    return {r["course_id"] for r in rows}


# ---------- Employee dashboard (persistent memory + gaps + roadmap) ----------

@app.get("/api/dashboard")
def dashboard(authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    dept, key, role_id = _user_context(user_id)
    gaps = ge.compute_gaps(user_id, key, role_id)
    roadmap_row = get_db().execute("SELECT data_json FROM roadmaps WHERE user_id=?", (user_id,)).fetchone()
    conn = get_db()
    profile = conn.execute("SELECT name, email, designation, department FROM users WHERE id=?",
                           (user_id,)).fetchone()
    enrollments = conn.execute(
        "SELECT e.id, e.course_id, e.status, e.progress_pct, e.updated_at FROM enrollments e WHERE e.user_id=?",
        (user_id,)).fetchall()
    conn.close()
    enrollments = [{**dict(e), "course": course_to_content(COURSES_BY_ID[e["course_id"]])}
                   for e in enrollments if e["course_id"] in COURSES_BY_ID]
    learning_hours = round(sum(e["course"]["duration"] for e in enrollments
                               if e["status"] == "completed") / 3600, 1)
    conn = get_db()
    assessment_done = conn.execute(
        "SELECT COUNT(*) AS n FROM assessment_results WHERE user_id=?", (user_id,)).fetchone()["n"] > 0
    conn.close()
    return {
        "profile": {**dict(profile), "role_id": role_id},
        "assessment_done": assessment_done,
        "competency_vector": gaps["vector"],
        "overall_current": gaps["overall_current"],
        "overall_target": gaps["overall_target"],
        "readiness_pct": gaps["readiness_pct"],
        "readiness_cap": gaps["readiness_cap"],
        "verified_completions": gaps["verified_completions"],
        "top_gaps": gaps["top_gaps"],
        "explanations": gaps["explanations"],
        "roadmap": json.loads(roadmap_row["data_json"]) if roadmap_row else None,
        "enrollments": enrollments,
        "learning_hours": learning_hours,
    }


# ---------- NSSTA TPAC pathways, competency taxonomy & standard roles ----------

@app.get("/api/tpac/pathways")
def tpac_pathways(authorization: Optional[str] = Header(None)):
    """NSSTA TPAC-recommended training programmes, ranked against measured gaps."""
    user_id = require_user(authorization)
    _, key, role_id = _user_context(user_id)
    gaps = ge.compute_gaps(user_id, key, role_id)
    import tpac_data
    pathways = tpac_data.get_tpac_pathways(key, gaps["top_gaps"])
    gap_by_area = {g["area"]: g["gap"] for g in gaps["top_gaps"]}
    return {"pathways": [{**p, "gap_points": round(max((gap_by_area.get(a, 0) for a in p["areas"]), default=0))}
                         for p in pathways]}


@app.get("/api/taxonomy")
def get_taxonomy():
    """FRAC-flavoured competency taxonomy (the 4 MoSPI pillars)."""
    from ontology import COMPETENCY_TYPE
    pillars = {"Domain": "Statistical & Domain Competencies",
               "Functional": "Technical Competencies",
               "Behavioural": "Behavioural & Managerial Competencies",
               "Digital Governance": "Digital Governance"}
    out = {}
    for area, t in COMPETENCY_TYPE.items():
        out.setdefault(t, []).append(area)
    return {"pillars": [{"type": t, "label": pillars.get(t, t), "areas": sorted(areas)}
                        for t, areas in out.items()]}


@app.get("/api/roles")
def get_roles():
    """Standard MoSPI job roles with their target competency baselines."""
    from ontology import ROLE_PROFILES
    return {"roles": [{"role_id": rid, **{k: v for k, v in r.items() if k != "targets"},
                       "target_areas": len(r["targets"])} for rid, r in ROLE_PROFILES.items()]}

# ---------- Chapters & chapter quizzes ----------

@app.get("/api/courses/{course_id}/chapters")
def course_chapters(course_id: str, authorization: Optional[str] = Header(None)):
    require_user(authorization)
    c = COURSES_BY_ID.get(course_id)
    if not c:
        raise HTTPException(404, "Unknown course")
    chapters = chapters_for(c)
    return {"course_id": course_id, "course_name": c["name"], "chapters": chapters}


@app.post("/api/courses/{course_id}/chapters/{chapter_no}/quiz")
def chapter_quiz(course_id: str, chapter_no: int, authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    c = COURSES_BY_ID.get(course_id)
    if not c:
        raise HTTPException(404, "Unknown course")
    if not 1 <= chapter_no <= len(CHAPTER_TITLES):
        raise HTTPException(404, "Unknown chapter")
    _, key = _user_department(user_id)
    qs = ge.pick_questions(QUESTION_BANK[key], c["competencyAreas"], n=5)
    return {"course_id": course_id, "chapter_no": chapter_no,
            "chapter_title": CHAPTER_TITLES[chapter_no - 1], "questions": qs}


@app.post("/api/courses/{course_id}/chapters/{chapter_no}/complete")
def chapter_complete(course_id: str, chapter_no: int, body: ChapterCompleteBody,
                     authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    c = COURSES_BY_ID.get(course_id)
    if not c:
        raise HTTPException(404, "Unknown course")
    if not 1 <= chapter_no <= len(CHAPTER_TITLES):
        raise HTTPException(404, "Unknown chapter")
    _, key = _user_department(user_id)
    bank = {q["id"]: q for q in QUESTION_BANK[key]}

    per_area, correct = {}, 0
    for a in body.answers:
        q = bank.get(a.get("question_id"))
        if not q:
            continue
        ok = a.get("chosen") == q["answer"]
        correct += ok
        st = per_area.setdefault(q["area"], {"correct": 0, "total": 0})
        st["total"] += 1
        st["correct"] += ok
    if not per_area:
        raise HTTPException(400, "No valid answers submitted")
    total_q = sum(v["total"] for v in per_area.values())
    score = round(100 * correct / total_q)
    area_scores = {area: round(100 * v["correct"] / v["total"]) for area, v in per_area.items()}

    conn = get_db()
    conn.execute(
        "INSERT INTO chapter_progress (user_id, course_id, chapter_no, quiz_score) VALUES (?,?,?,?) "
        "ON CONFLICT(user_id, course_id, chapter_no) DO UPDATE SET quiz_score=?, completed_at=datetime('now')",
        (user_id, course_id, chapter_no, score, score))
    done = conn.execute("SELECT COUNT(*) AS n FROM chapter_progress WHERE user_id=? AND course_id=?",
                        (user_id, course_id)).fetchone()["n"]
    pct = round(100 * done / len(CHAPTER_TITLES))
    conn.execute(
        "INSERT INTO enrollments (user_id, course_id, status, progress_pct) VALUES (?,?,?,?) "
        "ON CONFLICT(user_id, course_id) DO UPDATE SET progress_pct=?, status=?, updated_at=datetime('now')",
        (user_id, course_id,
         "completed" if pct >= 100 else "in_progress", pct,
         pct, "completed" if pct >= 100 else "in_progress"))
    conn.commit()
    conn.close()

    ge.update_competency(user_id, area_scores)
    ge.log_event(user_id, "chapter_completed",
                 {"course_id": course_id, "chapter_no": chapter_no, "score": score})
    if pct >= 100:
        ge.log_event(user_id, "course_completed", {"course_id": course_id})
        # course completion closes the loop: refresh gaps + roadmap
        gaps = ge.compute_gaps(user_id, key, _user_context(user_id)[2])
        ge.build_roadmap(user_id, key, COURSES, gaps, completed_ids=_completed_ids(user_id))

    return {"chapter_score": score, "course_progress_pct": pct,
            "course_status": "completed" if pct >= 100 else "in_progress",
            "area_scores": area_scores}


# ---------- Personalized quizzes (targeted at the user's weakest areas) ----------

@app.get("/api/quiz/personalized")
def personalized_quiz(authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    dept, key = _user_department(user_id)
    conn = get_db()
    rows = conn.execute("SELECT area, score FROM user_competency WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    if rows:
        weak = sorted(rows, key=lambda r: r["score"])[:3]
        areas = [r["area"] for r in weak]
    else:
        areas = list(target_profile_areas(key))
    qs = ge.pick_questions(QUESTION_BANK[key], areas, n=6)
    return {"target_areas": areas, "questions": qs}


def target_profile_areas(key: str) -> set:
    from ontology import target_profile
    return set(target_profile(key))


class QuizSubmitBody(BaseModel):
    answers: list[dict]


@app.post("/api/quiz/personalized/submit")
def personalized_quiz_submit(body: QuizSubmitBody, authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    _, key = _user_department(user_id)
    bank = {q["id"]: q for q in QUESTION_BANK[key]}
    per_area, results = {}, []
    for a in body.answers:
        q = bank.get(a.get("question_id"))
        if not q:
            continue
        ok = a.get("chosen") == q["answer"]
        results.append({"question_id": q["id"], "area": q["area"], "correct": ok})
        st = per_area.setdefault(q["area"], {"correct": 0, "total": 0})
        st["total"] += 1
        st["correct"] += ok
    if not per_area:
        raise HTTPException(400, "No valid answers submitted")
    scores = {area: round(100 * v["correct"] / v["total"]) for area, v in per_area.items()}
    ge.update_competency(user_id, scores)
    ge.log_event(user_id, "quiz_taken", {"scores": scores})
    gaps = ge.compute_gaps(user_id, key, _user_context(user_id)[2])
    ge.build_roadmap(user_id, key, COURSES, gaps, completed_ids=_completed_ids(user_id))
    return {"scores": scores, "results": results, "readiness_pct": gaps["readiness_pct"]}


# ---------- Uploaded material -> MCQ generation ----------

from fastapi import UploadFile, File


@app.get("/api/materials")
def list_materials(authorization: Optional[str] = Header(None)):
    """User's uploaded materials + the pre-loaded NSSTA/MoSPI manual library."""
    user_id = require_user(authorization)
    conn = get_db()
    rows = conn.execute("SELECT id, filename, user_id, LENGTH(text) AS chars, created_at "
                        "FROM materials WHERE user_id=? OR user_id=0 ORDER BY user_id, id",
                        (user_id,)).fetchall()
    conn.close()
    return {"materials": [dict(r) for r in rows]}


@app.post("/api/materials/upload")
async def upload_material(file: UploadFile = File(...), authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    raw = await file.read()
    try:
        text = mat_engine.extract_text(file.filename, raw)
    except ValueError as e:
        raise HTTPException(400, str(e))
    if len(text.strip()) < 100:
        raise HTTPException(400, "Material too short to generate a quiz from")
    conn = get_db()
    cur = conn.execute("INSERT INTO materials (user_id, filename, text) VALUES (?,?,?)",
                       (user_id, file.filename, text))
    conn.commit()
    mid = cur.lastrowid
    conn.close()
    chunks = mat_engine.chunk_text(text)
    chunks_indexed = 0
    try:
        import vector_store
        chunks_indexed = vector_store.index_material(mid, chunks)
    except Exception as e:
        print("vector index failed:", e)
    return {"material_id": mid, "filename": file.filename, "chars": len(text),
            "chunks": len(chunks), "chunks_indexed": chunks_indexed,
            "llm_available": llm.llm_available()}


@app.post("/api/materials/{material_id}/generate-quiz")
def generate_material_quiz(material_id: int, n: int = 5, level: str = "Understand",
                           personalized: bool = True,
                           authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    conn = get_db()
    row = conn.execute("SELECT * FROM materials WHERE id=? AND user_id IN (0, ?)",
                       (material_id, user_id)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Material not found")

    # Personalization: build the retrieval query from the user's weakest areas.
    focus_query = None
    weak_areas = []
    if personalized:
        _, key, role_id = _user_context(user_id)
        gaps = ge.compute_gaps(user_id, key, role_id)
        weak = [g["area"] for g in gaps["top_gaps"][:3]]
        if weak:
            weak_areas = weak
            focus_query = (f"Training material about {', '.join(weak)} "
                           f"for a {row['filename']} learner with weak areas: {', '.join(weak)}")
    questions, generator, used_chunks = mat_engine.generate_quiz_from_material(
        row["text"], n=n, level=level, focus_query=focus_query, material_id=material_id)
    conn = get_db()
    cur = conn.execute("INSERT INTO generated_quizzes (material_id, user_id, questions_json, generator) VALUES (?,?,?,?)",
                       (material_id, user_id, json.dumps(questions), generator))
    conn.commit()
    quiz_id = cur.lastrowid
    conn.close()
    return {"quiz_id": quiz_id, "generator": generator, "material_id": material_id,
            "personalized_for_areas": weak_areas, "chunks_used": len(used_chunks),
            "questions": [{k: q[k] for k in ("id", "question", "options", "area", "difficulty")}
                          for q in questions]}


@app.get("/api/courses/search/semantic")
def semantic_course_search(q: str, top_k: int = 5, authorization: Optional[str] = Header(None)):
    """Natural-language course search over the Pinecone-embedded catalogue."""
    require_user(authorization)
    try:
        import vector_store
        hits = vector_store.search_courses(q, top_k=top_k)
        return {"query": q, "results": hits}
    except Exception as e:
        raise HTTPException(503, f"Vector search unavailable: {e}")


@app.post("/api/materials/quizzes/{quiz_id}/grade")
def grade_generated_quiz(quiz_id: int, body: QuizSubmitBody, authorization: Optional[str] = Header(None)):
    """Grade answers against a generated quiz (answers were stripped client-side)."""
    user_id = require_user(authorization)
    conn = get_db()
    row = conn.execute("SELECT questions_json, generator FROM generated_quizzes WHERE id=? AND user_id=?",
                       (quiz_id, user_id)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Quiz not found")
    bank = {q["id"]: q for q in json.loads(row["questions_json"])}
    results, correct = [], 0
    for a in body.answers:
        q = bank.get(a.get("question_id"))
        if not q:
            continue
        ok = a.get("chosen") == q["answer"]
        correct += ok
        results.append({"question_id": a.get("question_id"), "correct": ok,
                        "explanation": q.get("explanation", ""),
                        "source_snippet": q.get("source_snippet", "")})
    total = max(1, len(results))
    return {"score": round(100 * correct / total), "results": results, "generator": row["generator"]}


# ---------- Admin analytics ----------


# ---------- Personalized assessment from memory + recommended courses ----------

@app.get("/api/personalized/preview")
def personalized_preview(authorization: Optional[str] = Header(None)):
    """Weak areas from memory + the recommended course/module that targets them."""
    user_id = require_user(authorization)
    _, key = _user_department(user_id)
    gaps = ge.compute_gaps(user_id, key, _user_context(user_id)[2])
    weak = [g["area"] for g in gaps["top_gaps"][:3]]
    import roadmap_data
    best = None
    for c in roadmap_data.get_roadmap(key):
        for mi, m in enumerate(c["modules"], start=1):
            overlap = [a for a in c["areas"] if a in weak]
            if overlap and best is None:
                best = {"course_key": c["key"], "course_name": c["name"],
                        "module_no": mi, "module_title": m["title"],
                        "lessons": len(m["videos"]), "matched_areas": overlap}
    return {"weak_areas": weak, "explanations": gaps["explanations"][:3],
            "readiness_pct": gaps["readiness_pct"],
            "recommended_module": best,
            "llm_available": llm.llm_available()}


class PersonalizedGenerateBody(BaseModel):
    n: int = 5
    course_key: Optional[str] = None


@app.post("/api/personalized/generate")
def personalized_generate(body: PersonalizedGenerateBody, authorization: Optional[str] = Header(None)):
    """Generate a quiz targeting the user's weakest areas, grounded in the
    recommended course module's lecture transcripts. Falls back to the
    competency bank when transcripts/LLM are unavailable."""
    user_id = require_user(authorization)
    _, key = _user_department(user_id)
    gaps = ge.compute_gaps(user_id, key, _user_context(user_id)[2])
    weak = [g["area"] for g in gaps["top_gaps"][:3]]
    if not weak:
        raise HTTPException(400, "No competency data yet — take the assessment first")

    import roadmap_data
    context, fetched, chosen = "", [], None
    courses = roadmap_data.get_roadmap(key)
    if body.course_key:
        courses = [c for c in courses if c["key"] == body.course_key]
        if not courses:
            raise HTTPException(404, "Course not found in your roadmap")
    for c in courses:
        overlap = [a for a in c["areas"] if a in weak] or c["areas"]
        all_videos = [v for m in c["modules"] for v in m["videos"]]
        ctx, vids = transcript_context_for(
            f"Topics to assess: {', '.join(weak)}. Course: {c['name']}. {' '.join(c['areas'])}.", all_videos)
        if ctx:
            context, fetched = ctx, vids
            chosen = {"course_key": c["key"], "module_no": 0, "title": c["name"] + " — weak-area retrieval"}

    questions, generator = [], "fallback"
    if context and llm.llm_available():
        try:
            from ontology import COMPETENCY_TYPE
            course = next(cc for cc in roadmap_data.get_roadmap(key) if cc["key"] == chosen["course_key"])
            focused = [a for a in weak if a in course["areas"]] or course["areas"]
            allowed = ", ".join(sorted(set(course["areas"]) | set(COMPETENCY_TYPE)))
            prompt = MODULE_QUIZ_PROMPT.format(
                module_title=f"{chosen['title']} (focus: {', '.join(focused)})",
                course_name=chosen["course_key"], n=body.n, areas=allowed, context=context)
            raw = llm.generate(prompt, max_tokens=6000)
            questions = llm.parse_llm_quiz(raw)[:body.n]
            for q in questions:
                q.setdefault("level", "L2")
            generator = "llm-transcript"
        except Exception as e:
            print("personalized generation failed:", e)

    if not questions and llm.llm_available():
        try:
            from ontology import COMPETENCY_TYPE
            if chosen:
                course = next(cc for cc in roadmap_data.get_roadmap(key) if cc["key"] == chosen["course_key"])
            else:
                course = next(cc for cc in roadmap_data.get_roadmap(key))
            focused = [a for a in weak if a in course["areas"]] or course["areas"]
            allowed = ", ".join(sorted(set(course["areas"]) | set(COMPETENCY_TYPE)))
            meta_context = (f"Course: {course['name']}. Description: {course['description']}\n"
                            f"Competency areas: {', '.join(course['areas'])}.\n"
                            f"Generate questions that assess these focus areas: {', '.join(focused)}.")
            raw = llm.generate(KNOWLEDGE_QUIZ_PROMPT.format(
                n=body.n, areas=allowed, context=meta_context), max_tokens=6000)
            questions = llm.parse_llm_quiz(raw)[:body.n]
            for q in questions:
                q.setdefault("level", "L2")
            generator = "llm-knowledge"
        except Exception as e:
            print("personalized knowledge-based generation failed:", e)

    if not questions:
        bank_full = {q["id"]: q for q in QUESTION_BANK[key]}
        fallback_areas = weak
        if chosen:
            course = next(cc for cc in roadmap_data.get_roadmap(key) if cc["key"] == chosen["course_key"])
            fallback_areas = [a for a in weak if a in course["areas"]] or course["areas"]
        qs = ge.pick_questions(QUESTION_BANK[key], fallback_areas, n=body.n)
        questions = [{**q, **({"answer": bank_full[q["id"]]["answer"]} if q["id"] in bank_full else {}),
                      "question": q["text"], "level": "L2"} for q in qs]

    conn = get_db()
    cur = conn.execute(
        "INSERT INTO personalized_quizzes (user_id, focus_areas_json, course_key, module_no, questions_json, generator) VALUES (?,?,?,?,?,?)",
        (user_id, json.dumps(weak), chosen["course_key"] if chosen else None,
         chosen["module_no"] if chosen else None, json.dumps(questions), generator))
    conn.commit()
    quiz_id = cur.lastrowid
    conn.close()
    return {"quiz_id": quiz_id, "generator": generator, "focus_areas": weak,
            "grounded_in": chosen, "transcript_videos_used": len(fetched),
            "questions": [{k: q[k] for k in ("id", "question", "options", "area", "difficulty", "level") if k in q}
                          for q in questions]}


@app.post("/api/personalized/{quiz_id}/grade")
def personalized_grade(quiz_id: int, body: QuizSubmitBody, authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    conn = get_db()
    row = conn.execute("SELECT * FROM personalized_quizzes WHERE id=? AND user_id=?",
                       (quiz_id, user_id)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Quiz not found")
    bank = {q["id"]: q for q in json.loads(row["questions_json"])}
    per_area, correct, results = {}, 0, []
    for a in body.answers:
        q = bank.get(a.get("question_id"))
        if not q:
            continue
        ok = a.get("chosen") == q["answer"]
        correct += ok
        results.append({"question_id": q["id"], "correct": ok,
                        "explanation": q.get("explanation", ""),
                        "source_snippet": q.get("source_snippet", ""),
                        "level": q.get("level", "")})
        st = per_area.setdefault(q.get("area", "General"), {"correct": 0, "total": 0})
        st["total"] += 1
        st["correct"] += ok
    if not per_area:
        raise HTTPException(400, "No valid answers submitted")
    score = round(100 * correct / max(1, sum(v["total"] for v in per_area.values())))
    area_scores = {area: round(100 * v["correct"] / v["total"]) for area, v in per_area.items()}

    # straight into persistent memory — same EWMA merge as everything else
    ge.update_competency(user_id, area_scores)
    s_w = strength_weakness(area_scores)
    ge.log_event(user_id, "personalized_quiz_taken",
                 {"quiz_id": quiz_id, "score": score, "areas": list(area_scores),
                  "strength": s_w[0], "weakness": s_w[1]})
    _, key = _user_department(user_id)
    gaps = ge.compute_gaps(user_id, key, _user_context(user_id)[2])
    ge.build_roadmap(user_id, key, COURSES, gaps, completed_ids=_completed_ids(user_id))
    strength, weakness = strength_weakness(area_scores)
    return {"score": score, "area_scores": area_scores,
            "strength": strength, "weakness": weakness,
            "readiness_pct": gaps["readiness_pct"], "results": results}



# ---------- Per-lesson quizzes (transcript-grounded, 5 questions) ----------

@app.post("/api/roadmap/{course_key}/lesson/{module_no}/{video_no}/quiz")
def lesson_quiz(course_key: str, module_no: int, video_no: int,
                authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    import roadmap_data
    c = roadmap_data.get_course(course_key)
    if not c:
        raise HTTPException(404, "Course not found in your roadmap")
    if not 1 <= module_no <= len(c["modules"]):
        raise HTTPException(404, "Unknown module")
    module = c["modules"][module_no - 1]
    if not 1 <= video_no <= len(module["videos"]):
        raise HTTPException(404, "Unknown lesson")
    video = module["videos"][video_no - 1]

    conn = get_db()
    stored = conn.execute(
        "SELECT questions_json, generator FROM lesson_quizzes WHERE user_id=? AND course_key=? AND module_no=? AND video_no=?",
        (user_id, course_key, module_no, video_no)).fetchone()
    conn.close()
    if stored and stored["generator"] != "fallback":
        return {"lesson_title": video["title"], "generator": stored["generator"],
                "questions": json.loads(stored["questions_json"])}

    _, key = _user_department(user_id)
    questions, generator, context_ok = [], "fallback", False
    if not video.get("playlist"):
        try:
            import transcripts as ts
            vctx, vids = transcript_context_for(
                f"{video['title']}. {c['name']}. {' '.join(c['areas'])}", [video], total=20000)
            ctx = vctx
            context_ok = bool(ctx)
            if ctx and llm.llm_available():
                from ontology import COMPETENCY_TYPE
                allowed = ", ".join(sorted(set(c["areas"]) | set(COMPETENCY_TYPE)))
                prompt = MODULE_QUIZ_PROMPT.format(
                    module_title=f"{video['title']} (lesson quiz)", course_name=c["name"],
                    n=5, areas=allowed, context=ctx)
                questions = llm.parse_llm_quiz(llm.generate(prompt, max_tokens=6000))[:5]
                for q in questions:
                    q.setdefault("level", "L2")
                generator = "llm"
        except Exception as e:
            print("lesson quiz generation failed:", e)

    if not questions and llm.llm_available() and not context_ok:
        try:
            from ontology import COMPETENCY_TYPE
            allowed = ", ".join(sorted(set(c["areas"]) | set(COMPETENCY_TYPE)))
            meta_context = (f"Course: {c['name']}. Description: {c['description']}\n"
                            f"Lesson: {video['title']} (module: {module['title']}).\n"
                            f"Competency areas covered: {', '.join(c['areas'])}.")
            raw = llm.generate(KNOWLEDGE_QUIZ_PROMPT.format(
                n=5, areas=allowed, context=meta_context), max_tokens=6000)
            questions = llm.parse_llm_quiz(raw)[:5]
            for q in questions:
                q.setdefault("level", "L2")
            generator = "llm-knowledge"
        except Exception as e:
            print("lesson knowledge-based generation failed:", e)

    if not questions:
        _, bank_key = _user_department(user_id)
        qs = ge.pick_questions(QUESTION_BANK[bank_key], c["areas"], n=5)
        bank_full = {q["id"]: q for q in QUESTION_BANK[bank_key]}
        questions = [{**q, **({"answer": bank_full[q["id"]]["answer"]} if q["id"] in bank_full else {}),
                      "question": q["text"], "level": "L2"} for q in qs]

    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO lesson_quizzes (user_id, course_key, module_no, video_no, video_id, questions_json, generator) VALUES (?,?,?,?,?,?,?)",
                 (user_id, course_key, module_no, video_no, video["yt"], json.dumps(questions), generator))
    conn.commit()
    conn.close()
    return {"lesson_title": video["title"], "generator": generator,
            "questions": [{k: q[k] for k in ("id", "question", "options", "area", "level") if k in q}
                          for q in questions]}


@app.post("/api/roadmap/{course_key}/lesson/{module_no}/{video_no}/complete")
def lesson_quiz_complete(course_key: str, module_no: int, video_no: int, body: ChapterCompleteBody,
                         authorization: Optional[str] = Header(None)):
    user_id = require_user(authorization)
    conn = get_db()
    row = conn.execute(
        "SELECT questions_json FROM lesson_quizzes WHERE user_id=? AND course_key=? AND module_no=? AND video_no=?",
        (user_id, course_key, module_no, video_no)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(400, "Take the lesson quiz first")
    bank = {q["id"]: q for q in json.loads(row["questions_json"])}
    per_area, correct = {}, 0
    for a in body.answers:
        q = bank.get(a.get("question_id"))
        if not q:
            continue
        ok = a.get("chosen") == q["answer"]
        correct += ok
        st = per_area.setdefault(q.get("area", "General"), {"correct": 0, "total": 0})
        st["total"] += 1
        st["correct"] += ok
    if not per_area:
        raise HTTPException(400, "No valid answers submitted")
    score = round(100 * correct / max(1, sum(v["total"] for v in per_area.values())))
    area_scores = {area: round(100 * v["correct"] / v["total"]) for area, v in per_area.items()}

    ge.update_competency(user_id, area_scores)
    s_w = strength_weakness(area_scores)
    conn = get_db()
    conn.execute("UPDATE lesson_quizzes SET score=? WHERE user_id=? AND course_key=? AND module_no=? AND video_no=?",
                 (score, user_id, course_key, module_no, video_no))
    conn.commit()
    conn.close()
    ge.log_event(user_id, "lesson_quiz_completed",
                 {"course_key": course_key, "module_no": module_no, "video_no": video_no,
                  "score": score, "strength": s_w[0], "weakness": s_w[1]})
    _, key = _user_department(user_id)
    gaps = ge.compute_gaps(user_id, key, _user_context(user_id)[2])
    ge.build_roadmap(user_id, key, COURSES, gaps, completed_ids=_completed_ids(user_id))
    strength, weakness = strength_weakness(area_scores)
    return {"lesson_score": score, "area_scores": area_scores,
            "strength": strength, "weakness": weakness,
            "readiness_pct": gaps["readiness_pct"]}


@app.get("/api/admin/analytics")
def admin_analytics(authorization: Optional[str] = Header(None)):
    require_user(authorization)
    conn = get_db()
    area_stats = conn.execute(
        "SELECT area, ROUND(AVG(score),1) AS avg_score, COUNT(*) AS n FROM user_competency GROUP BY area ORDER BY avg_score"
    ).fetchall()
    dept_stats = conn.execute(
        "SELECT u.department, COUNT(DISTINCT u.id) AS users FROM users u LEFT JOIN enrollments e ON e.user_id=u.id GROUP BY u.department"
    ).fetchall()
    completions = conn.execute(
        "SELECT course_id, COUNT(*) AS completions FROM enrollments WHERE status='completed' GROUP BY course_id"
    ).fetchall()
    total_users = conn.execute("SELECT COUNT(*) AS n FROM users").fetchone()["n"]
    conn.close()
    return {
        "total_users": total_users,
        "competency_distribution": [dict(r) for r in area_stats],
        "department_sizes": [dict(r) for r in dept_stats],
        "course_completions": [{**dict(r), "course": COURSES_BY_ID[r["course_id"]]["name"]}
                               for r in completions if r["course_id"] in COURSES_BY_ID],
    }
