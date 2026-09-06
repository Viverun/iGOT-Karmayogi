"""SQLite storage for the dummy iGOT backend. Stdlib sqlite3, no ORM."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "igot.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    designation TEXT DEFAULT '',
    department TEXT DEFAULT '',
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS tokens (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS enrollments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'enrolled',  -- enrolled | in_progress | completed
    progress_pct INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT DEFAULT (datetime('now')),
    UNIQUE(user_id, course_id)
);
CREATE TABLE IF NOT EXISTS assessment_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    department_key TEXT NOT NULL,
    answers_json TEXT NOT NULL,   -- [{question_id, area, qtype, chosen, correct}]
    scores_json TEXT NOT NULL,    -- {area: pct} computed server-side
    submitted_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS user_competency (
    user_id INTEGER NOT NULL REFERENCES users(id),
    area TEXT NOT NULL,
    score REAL NOT NULL,          -- 0-100, EWMA-updated persistent skill level
    updated_at TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, area)
);
CREATE TABLE IF NOT EXISTS chapter_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id TEXT NOT NULL,
    chapter_no INTEGER NOT NULL,
    quiz_score REAL NOT NULL,
    completed_at TEXT DEFAULT (datetime('now')),
    UNIQUE(user_id, course_id, chapter_no)
);
CREATE TABLE IF NOT EXISTS learning_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    etype TEXT NOT NULL,          -- registered | assessed | chapter_completed | course_completed | quiz_taken | roadmap_updated
    detail_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS roadmaps (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    data_json TEXT NOT NULL,
    updated_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS materials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    filename TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS generated_quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    material_id INTEGER NOT NULL REFERENCES materials(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    questions_json TEXT NOT NULL,
    generator TEXT NOT NULL,      -- llm | fallback
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS transcripts (
    video_id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    chars INTEGER NOT NULL,
    indexed INTEGER NOT NULL DEFAULT 0,   -- 1 once chunks are in the vector DB
    fetched_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS module_quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_key TEXT NOT NULL,
    module_no INTEGER NOT NULL,
    questions_json TEXT NOT NULL,   -- LLM questions grounded in the module's video transcripts
    generator TEXT NOT NULL,
    UNIQUE(user_id, course_key, module_no)
);
CREATE TABLE IF NOT EXISTS lesson_quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_key TEXT NOT NULL,
    module_no INTEGER NOT NULL,
    video_no INTEGER NOT NULL,
    video_id TEXT NOT NULL,
    questions_json TEXT NOT NULL,
    generator TEXT NOT NULL,
    score REAL,
    UNIQUE(user_id, course_key, module_no, video_no)
);
CREATE TABLE IF NOT EXISTS personalized_quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    focus_areas_json TEXT NOT NULL,  -- weak areas this quiz targets
    course_key TEXT,                 -- recommended course whose transcripts grounded it
    module_no INTEGER,
    questions_json TEXT NOT NULL,
    generator TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
CREATE TABLE IF NOT EXISTS course_swaps (
    user_id INTEGER NOT NULL REFERENCES users(id),
    original_key TEXT NOT NULL,     -- the core course the learner found difficult
    replacement_key TEXT NOT NULL,  -- the foundational course now shown in its place
    reason TEXT,                    -- learner's own words, from the chat
    created_at TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (user_id, original_key)
);
CREATE TABLE IF NOT EXISTS chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    role TEXT NOT NULL,   -- 'user' | 'assistant'
    content TEXT NOT NULL,
    action_json TEXT,     -- structured action the assistant took, if any (e.g. a roadmap swap)
    created_at TEXT DEFAULT (datetime('now'))
);
"""

# Single demo user for the presentation (no real authentication by design).
DEMO_USER = {
    "name": "Demo Karmayogi",
    "email": "demo@gov.in",
    "password": "demo123",
    "designation": "Under Secretary",
    "department": "Ministry of Statistics and Programme Implementation (MoSPI)",
}

ADMIN_USER = {
    "name": "NSSTA Training Administrator",
    "email": "admin.nssta@mospi.gov.in",
    "password": "demo123",
    "designation": "Training Administrator (TPAC Cell)",
    "department": "National Statistical Systems Training Academy (NSSTA), MoSPI",
}


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    # lightweight migrations
    cols = [r[1] for r in conn.execute("PRAGMA table_info(transcripts)")]
    if "indexed" not in cols:
        conn.execute("ALTER TABLE transcripts ADD COLUMN indexed INTEGER NOT NULL DEFAULT 0")
    lcols = [r[1] for r in conn.execute("PRAGMA table_info(lesson_quizzes)")]
    if "score" not in lcols:
        conn.execute("ALTER TABLE lesson_quizzes ADD COLUMN score REAL")
    ucols = [r[1] for r in conn.execute("PRAGMA table_info(users)")]
    if "role" not in ucols:
        conn.execute("ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'official'")
    conn.execute(
        "INSERT OR IGNORE INTO users (name, email, password, designation, department) VALUES (?,?,?,?,?)",
        (DEMO_USER["name"], DEMO_USER["email"], DEMO_USER["password"],
         DEMO_USER["designation"], DEMO_USER["department"]),
    )
    conn.execute(
        "INSERT OR IGNORE INTO users (name, email, password, designation, department, role) VALUES (?,?,?,?,?,'admin')",
        (ADMIN_USER["name"], ADMIN_USER["email"], ADMIN_USER["password"],
         ADMIN_USER["designation"], ADMIN_USER["department"]),
    )
    conn.commit()
    conn.close()
