"""One-off seed for DEMO/PRESENTATION purposes only.

Populates the local igot.db with a synthetic org-scale roster of MoSPI/NSSTA
officers (~60 by default) carrying realistic-looking competency scores,
assessment results and lesson completions, so the Admin Analytics dashboard
reads like a real departmental rollout instead of 1-2 test accounts.

This does NOT touch the API layer — /api/admin/analytics still computes
everything live from these rows exactly as it would for real users; only the
underlying rows are synthetic. Re-run is safe (INSERT OR IGNORE on users by
email); scores are upserted per user/area.

Usage: python3 seed_demo_analytics.py [count]   (default count: 60)
"""
import json
import random
import sys

sys.path.insert(0, ".")
from db import get_db, init_db

random.seed(42)

FIRST_NAMES = [
    "Priya", "Rajesh", "Anjali", "Vikram", "Sunita", "Arvind", "Kavita", "Mohammed",
    "Deepa", "Ramesh", "Neha", "Suresh", "Pooja", "Anand", "Lakshmi", "Sanjay",
    "Meera", "Vivek", "Divya", "Ashok", "Ritu", "Manoj", "Swati", "Rahul",
    "Geeta", "Kiran", "Nandini", "Prakash", "Shobha", "Alok", "Uma", "Naveen",
    "Radhika", "Sandeep", "Kalpana", "Yogesh", "Bhavna", "Ajay", "Sarita", "Dinesh",
]
LAST_NAMES = [
    "Sharma", "Kumar", "Nair", "Singh", "Reddy", "Menon", "Iyer", "Faizal",
    "Krishnan", "Chandra", "Gupta", "Verma", "Joshi", "Rao", "Pillai", "Mishra",
    "Bose", "Desai", "Chatterjee", "Bhatt", "Kapoor", "Trivedi", "Pandey", "Shetty",
]

# (title, department, dept_key, base_readiness_pct) — mirrors ontology.ROLE_PROFILES
ROLES = [
    ("Field Officer (JSO)", "Field Operations Division (FOD), NSSO", "statistics", 42),
    ("Senior Statistical Officer", "Price Statistics Division (PSD), MoSPI", "statistics", 68),
    ("Director", "National Accounts Division (NAD), MoSPI", "statistics", 79),
    ("Joint Director", "Survey Design & Research Division (SDRD), MoSPI", "statistics", 72),
    ("Deputy Director", "Computer Centre (IT & AI Directorate), MoSPI", "general", 75),
    ("Statistical Officer", "Labour Bureau & Social Statistics", "statistics", 54),
    ("Analyst", "Department of Space and ISRO HQ", "space", 47),
    ("Scientist/Engineer", "Department of Space and ISRO HQ", "space", 63),
    ("Under Secretary", "Ministry of Statistics and Programme Implementation (MoSPI)", "general", 57),
]

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

# (course_key, module_layout, popularity_weight, difficulty_penalty)
# popularity_weight biases how often officers land in this course (trending);
# difficulty_penalty is subtracted from their quiz scores (makes a course
# show up as "officers find this difficult" in admin analytics).
COURSE_PROFILES = [
    ("rs-fundamentals", [3, 4, 3], 5, 0),
    ("gis-essentials", [2, 2, 2], 4, 8),
    ("python-geospatial", [2, 2, 2], 3, 5),
    ("satcom-gnss", [2, 3, 2], 3, 24),   # hardest — GNSS math trips people up
    ("geo-governance", [2, 2, 2], 4, 3),
]
COURSE_WEIGHTS = [p[2] for p in COURSE_PROFILES]


def make_roster(n: int):
    used_emails = set()
    roster = []
    for i in range(n):
        first, last = random.choice(FIRST_NAMES), random.choice(LAST_NAMES)
        name = f"{first} {last}"
        title, department, dept_key, base_pct = random.choice(ROLES)
        slug = f"{first}.{last}".lower()
        email = f"{slug}@nssta.mospi.gov.in"
        n_dup = 1
        while email in used_emails:
            n_dup += 1
            email = f"{slug}{n_dup}@nssta.mospi.gov.in"
        used_emails.add(email)
        noise = random.randint(-12, 12)
        roster.append((name, email, title, department, dept_key, max(15, min(95, base_pct + noise))))
    return roster


def seed(n: int = 60):
    init_db()
    conn = get_db()

    for name, email, designation, department, dept_key, base_pct in make_roster(n):
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

        # ~85% of the roster has taken the diagnostic assessment
        if random.random() < 0.85:
            conn.execute(
                "INSERT INTO assessment_results (user_id, department_key, answers_json, scores_json, submitted_at) "
                "VALUES (?, ?, ?, ?, datetime('now'))",
                (uid, dept_key, "[]", json.dumps(scores)),
            )

        # a plausible spread of lesson-quiz activity, spread across all 5
        # roadmap courses (each with its own popularity/difficulty bias) so
        # "trending courses" and "courses officers find difficult" have real
        # numbers to compare instead of a single course carrying all the data.
        n_courses_touched = random.choice([0, 1, 1, 1, 2, 2])
        touched = random.choices(COURSE_PROFILES, weights=COURSE_WEIGHTS, k=n_courses_touched)
        for course_key, module_layout, _weight, difficulty in {c[0]: c for c in touched}.values():
            total_lessons = sum(module_layout)
            lessons_done = random.choice([2, 4, total_lessons, total_lessons, total_lessons])
            lessons_done = min(lessons_done, total_lessons)
            n_placed = 0
            for m_no, video_count in enumerate(module_layout, start=1):
                for v_no in range(1, video_count + 1):
                    if n_placed >= lessons_done:
                        break
                    quiz_score = max(15, min(100, base_pct - difficulty + random.randint(-10, 15)))
                    conn.execute(
                        "INSERT INTO lesson_quizzes "
                        "(user_id, course_key, module_no, video_no, video_id, questions_json, generator, score) "
                        "VALUES (?, ?, ?, ?, 'demo', '[]', 'llm', ?) "
                        "ON CONFLICT (user_id, course_key, module_no, video_no) DO UPDATE SET "
                        "video_id=excluded.video_id, questions_json=excluded.questions_json, "
                        "generator=excluded.generator, score=excluded.score",
                        (uid, course_key, m_no, v_no, quiz_score),
                    )
                    n_placed += 1
            if lessons_done >= total_lessons:
                for m_no in range(1, len(module_layout) + 1):
                    conn.execute(
                        "INSERT INTO module_quizzes "
                        "(user_id, course_key, module_no, questions_json, generator) "
                        "VALUES (?, ?, ?, '[]', 'llm') "
                        "ON CONFLICT (user_id, course_key, module_no) DO UPDATE SET "
                        "questions_json=excluded.questions_json, generator=excluded.generator",
                        (uid, course_key, m_no),
                    )
                    mod_score = max(15, min(100, base_pct - difficulty + random.randint(-5, 10)))
                    conn.execute(
                        "INSERT INTO chapter_progress (user_id, course_id, chapter_no, quiz_score) "
                        "VALUES (?, ?, ?, ?) "
                        "ON CONFLICT(user_id, course_id, chapter_no) DO UPDATE SET quiz_score=excluded.quiz_score",
                        (uid, f"roadmap:{course_key}", m_no, mod_score),
                    )

    conn.commit()
    total = conn.execute("SELECT COUNT(*) AS n FROM users WHERE id != 0").fetchone()["n"]
    conn.close()
    print(f"Seeded {n} synthetic officers. Total users now: {total}")


if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    seed(count)
