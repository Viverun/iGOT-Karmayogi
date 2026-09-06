"""One-off seed for DEMO/PRESENTATION purposes only.

Populates the local igot.db with ~10 synthetic MoSPI/NSSTA officer accounts
carrying realistic-looking competency scores, assessment results and lesson
completions, so the Admin Analytics dashboard has enough spread to demo
(org-wide distributions, department breakdowns, readiness spread) without
waiting for real officers to use the platform.

This does NOT touch the API layer — /api/admin/analytics still computes
everything live from these rows exactly as it would for real users. Re-run
is safe (INSERT OR IGNORE on users by email); scores are upserted.

Usage: python3 seed_demo_analytics.py
"""
import random
import sqlite3
import sys

sys.path.insert(0, ".")
from db import DB_PATH, init_db

random.seed(42)

DEMO_OFFICERS = [
    ("Priya Sharma", "priya.sharma@nssta.mospi.gov.in", "Senior Statistical Officer",
     "Price Statistics Division (PSD), MoSPI", "statistics", 78),
    ("Rajesh Kumar", "rajesh.kumar@nssta.mospi.gov.in", "Field Officer (JSO)",
     "Field Operations Division (FOD), NSSO", "statistics", 55),
    ("Anjali Nair", "anjali.nair@nssta.mospi.gov.in", "Deputy Director",
     "Computer Centre (IT & AI Directorate), MoSPI", "general", 82),
    ("Vikram Singh", "vikram.singh@nssta.mospi.gov.in", "Statistical Officer",
     "Labour Bureau & Social Statistics", "statistics", 61),
    ("Sunita Reddy", "sunita.reddy@nssta.mospi.gov.in", "Joint Director",
     "Survey Design & Research Division (SDRD), MoSPI", "statistics", 70),
    ("Arvind Menon", "arvind.menon@isro.gov.in", "Analyst",
     "Department of Space and ISRO HQ", "space", 48),
    ("Kavita Iyer", "kavita.iyer@isro.gov.in", "Scientist/Engineer",
     "Department of Space and ISRO HQ", "space", 66),
    ("Mohammed Faizal", "faizal@nssta.mospi.gov.in", "Director",
     "National Accounts Division (NAD), MoSPI", "statistics", 74),
    ("Deepa Krishnan", "deepa.krishnan@nssta.mospi.gov.in", "Under Secretary",
     "Ministry of Statistics and Programme Implementation (MoSPI)", "general", 58),
    ("Ramesh Chandra", "ramesh.chandra@nssta.mospi.gov.in", "Field Officer (JSO)",
     "Field Operations Division (FOD), NSSO", "statistics", 39),
]

# competency areas per department key (mirrors ontology.TARGET_PROFILES)
AREAS_BY_KEY = {
    "statistics": ["Sampling Techniques", "Survey Design", "Statistical Methods",
                   "Data Interpretation", "Python", "SQL", "Digital Governance",
                   "Cybersecurity and Data Protection", "Communication",
                   "Ethics and Values", "Data Visualization", "Policy Formulation"],
    "space": ["Remote Sensing Fundamentals", "Satellite Data Processing", "GIS",
              "Data Interpretation", "Python", "Digital Governance",
              "Cybersecurity and Data Protection", "Communication",
              "Problem Solving", "Data Visualization", "AI and Emerging Tech",
              "Decision Making"],
    "general": ["National Priorities", "Digital Governance", "AI and Emerging Tech",
                "Citizen Centricity", "Decision Making", "Policy Formulation",
                "Communication", "Ethics and Values"],
}


def seed():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    for name, email, designation, department, dept_key, base_pct in DEMO_OFFICERS:
        conn.execute(
            "INSERT OR IGNORE INTO users (name, email, password, designation, department) "
            "VALUES (?,?,?,?,?)",
            (name, email, "demo123", designation, department),
        )
        uid = conn.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()["id"]

        areas = AREAS_BY_KEY[dept_key]
        scores = {}
        for area in areas:
            noise = random.randint(-15, 15)
            scores[area] = max(0, min(100, base_pct + noise))
            conn.execute(
                "INSERT INTO user_competency (user_id, area, score, updated_at) "
                "VALUES (?, ?, ?, datetime('now')) "
                "ON CONFLICT(user_id, area) DO UPDATE SET score=excluded.score, updated_at=excluded.updated_at",
                (uid, area, scores[area]),
            )

        import json
        conn.execute(
            "INSERT INTO assessment_results (user_id, department_key, answers_json, scores_json, submitted_at) "
            "VALUES (?, ?, ?, ?, datetime('now'))",
            (uid, dept_key, "[]", json.dumps(scores)),
        )

        # a plausible spread of lesson-quiz activity so "active learners" and
        # "avg lesson quiz score" have real, varied numbers to aggregate.
        # rs-fundamentals has 3 modules of {3,4,3} videos = 10 lessons total.
        module_layout = [3, 4, 3]
        lessons_done = random.choice([0, 2, 4, 6, 10, 10])  # some finish the whole course
        n_placed = 0
        for m_no, video_count in enumerate(module_layout, start=1):
            for v_no in range(1, video_count + 1):
                if n_placed >= lessons_done:
                    break
                quiz_score = max(40, min(100, base_pct + random.randint(-10, 20)))
                conn.execute(
                    "INSERT OR REPLACE INTO lesson_quizzes "
                    "(user_id, course_key, module_no, video_no, video_id, questions_json, generator, score) "
                    "VALUES (?, 'rs-fundamentals', ?, ?, 'demo', '[]', 'llm', ?)",
                    (uid, m_no, v_no, quiz_score),
                )
                n_placed += 1
        if lessons_done >= 10:
            for m_no in range(1, 4):
                conn.execute(
                    "INSERT OR REPLACE INTO module_quizzes "
                    "(user_id, course_key, module_no, questions_json, generator) "
                    "VALUES (?, 'rs-fundamentals', ?, '[]', 'llm')",
                    (uid, m_no),
                )
                mod_score = max(60, min(100, base_pct + random.randint(-5, 15)))
                conn.execute(
                    "INSERT INTO chapter_progress (user_id, course_id, chapter_no, quiz_score) "
                    "VALUES (?, 'roadmap:rs-fundamentals', ?, ?) "
                    "ON CONFLICT(user_id, course_id, chapter_no) DO UPDATE SET quiz_score=excluded.quiz_score",
                    (uid, m_no, mod_score),
                )

    conn.commit()
    n = conn.execute("SELECT COUNT(*) AS n FROM users WHERE id != 0").fetchone()["n"]
    conn.close()
    print(f"Seeded demo officers. Total users now: {n}")


if __name__ == "__main__":
    seed()
