
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    designation TEXT DEFAULT '',
    department TEXT DEFAULT '',
    role TEXT NOT NULL DEFAULT 'official',
    created_at TEXT DEFAULT (NOW()::text)
);
CREATE TABLE IF NOT EXISTS tokens (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    created_at TEXT DEFAULT (NOW()::text)
);
CREATE TABLE IF NOT EXISTS enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'enrolled',  -- enrolled | in_progress | completed
    progress_pct INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT DEFAULT (NOW()::text),
    UNIQUE(user_id, course_id)
);
CREATE TABLE IF NOT EXISTS assessment_results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    department_key TEXT NOT NULL,
    answers_json TEXT NOT NULL,   -- [{question_id, area, qtype, chosen, correct}]
    scores_json TEXT NOT NULL,    -- {area: pct} computed server-side
    submitted_at TEXT DEFAULT (NOW()::text)
);
CREATE TABLE IF NOT EXISTS user_competency (
    user_id INTEGER NOT NULL REFERENCES users(id),
    area TEXT NOT NULL,
    score REAL NOT NULL,          -- 0-100, EWMA-updated persistent skill level
    updated_at TEXT DEFAULT (NOW()::text),
    PRIMARY KEY (user_id, area)
);
CREATE TABLE IF NOT EXISTS chapter_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_id TEXT NOT NULL,
    chapter_no INTEGER NOT NULL,
    quiz_score REAL NOT NULL,
    completed_at TEXT DEFAULT (NOW()::text),
    UNIQUE(user_id, course_id, chapter_no)
);
CREATE TABLE IF NOT EXISTS learning_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    etype TEXT NOT NULL,          -- registered | assessed | chapter_completed | course_completed | quiz_taken | roadmap_updated
    detail_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT DEFAULT (NOW()::text)
);
CREATE TABLE IF NOT EXISTS roadmaps (
    user_id INTEGER PRIMARY KEY REFERENCES users(id),
    data_json TEXT NOT NULL,
    updated_at TEXT DEFAULT (NOW()::text)
);
CREATE TABLE IF NOT EXISTS materials (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    filename TEXT NOT NULL,
    text TEXT NOT NULL,
    created_at TEXT DEFAULT (NOW()::text)
);
CREATE TABLE IF NOT EXISTS generated_quizzes (
    id SERIAL PRIMARY KEY,
    material_id INTEGER NOT NULL REFERENCES materials(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    questions_json TEXT NOT NULL,
    generator TEXT NOT NULL,      -- llm | fallback
    created_at TEXT DEFAULT (NOW()::text)
);
CREATE TABLE IF NOT EXISTS transcripts (
    video_id TEXT PRIMARY KEY,
    text TEXT NOT NULL,
    chars INTEGER NOT NULL,
    indexed INTEGER NOT NULL DEFAULT 0,   -- 1 once chunks are in the vector DB
    fetched_at TEXT DEFAULT (NOW()::text)
);
CREATE TABLE IF NOT EXISTS module_quizzes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_key TEXT NOT NULL,
    module_no INTEGER NOT NULL,
    questions_json TEXT NOT NULL,   -- LLM questions grounded in the module's video transcripts
    generator TEXT NOT NULL,
    UNIQUE(user_id, course_key, module_no)
);
CREATE TABLE IF NOT EXISTS lesson_quizzes (
    id SERIAL PRIMARY KEY,
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
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    focus_areas_json TEXT NOT NULL,  -- weak areas this quiz targets
    course_key TEXT,                 -- recommended course whose transcripts grounded it
    module_no INTEGER,
    questions_json TEXT NOT NULL,
    generator TEXT NOT NULL,
    created_at TEXT DEFAULT (NOW()::text)
);
CREATE TABLE IF NOT EXISTS course_swaps (
    user_id INTEGER NOT NULL REFERENCES users(id),
    original_key TEXT NOT NULL,     -- the core course the learner found difficult
    replacement_key TEXT NOT NULL,  -- the foundational course now shown in its place
    reason TEXT,                    -- learner's own words, from the chat
    created_at TEXT DEFAULT (NOW()::text),
    PRIMARY KEY (user_id, original_key)
);
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    role TEXT NOT NULL,   -- 'user' | 'assistant'
    content TEXT NOT NULL,
    action_json TEXT,     -- structured action the assistant took, if any (e.g. a roadmap swap)
    created_at TEXT DEFAULT (NOW()::text)
);
CREATE TABLE IF NOT EXISTS coding_labs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    course_key TEXT NOT NULL,
    lab_no INTEGER NOT NULL DEFAULT 1,
    code_submitted TEXT,             -- last code the student submitted
    score REAL,                      -- 0-100: percentage of test cases passed
    passed INTEGER NOT NULL DEFAULT 0,  -- 1 if score >= 60
    submitted_at TEXT DEFAULT (NOW()::text),
    UNIQUE(user_id, course_key, lab_no)
);
