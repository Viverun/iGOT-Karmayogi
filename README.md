# SAKSHAM-STAT — AI Skill Intelligence & Learning Platform 

AI-enabled learning platform for capacity building across India's civil services, built as a
Mission Karmayogi-style skill-intelligence layer and integrated with the iGOT Karmayogi ecosystem
(replicated as a local "dummy iGOT" for the demo). Ships with three ready-to-use demo personas
spanning two ministries — see [Demo logins](#demo-logins).

## What's inside

```
dummy-igot/       Frontend (static HTML/Tailwind): landing, login/register, dashboard,
                  course player (embedded YouTube + Monaco/Pyodide coding labs),
                  quiz + assessment flows, Sahitya chatbot, admin analytics
backend/          FastAPI app: auth, Sunbird-shaped catalogue, PII-safe competency
                  memory, gap engine, roadmap recommender, transcript-grounded quiz
                  generation (Claude/OpenAI), Pinecone vector store
docs/             Solution blueprint + research/plan of action
```

## Key features

- **Two department tracks, on-site YouTube learning** — Space/ISRO (5 courses: IIRS/ISRO, NPTEL, NRSC,
  freeCodeCamp) and Banking/DFS (6 courses: RBI regulation, PMJDY, NPA/credit risk, UPI/CBDC, ethics),
  each with 3 modules of real, verified lecture videos — never redirected off-platform
- **Department-tailored diagnostic assessment** (L1 easy / L2 medium / L3 hard), auto-routed by ministry
- **Persistent, PII-minimized competency memory** — `user_competency` EWMA-merged from assessments,
  module/lesson quizzes, and course completions. The AI layer (chat, quiz generation) only ever sees
  department, competency scores and course keys — never name/email; free-text chat input is PII-redacted
  before it reaches the LLM (`backend/privacy.py`)
- **Gap engine + personalized roadmap**, sequenced Foundations → Core → Advanced, with a chatbot-driven
  swap to an easier alternative when a learner reports a course is too hard
- **Transcript-grounded quizzes** at both module and per-lesson granularity — MCQs generated strictly
  from the lecture's actual YouTube transcript, idempotent under concurrent requests (a double-click
  can never produce a quiz whose rendered questions don't match what gets graded)
- **Hands-on coding labs** — in-browser Python via Monaco editor + Pyodide, graded against test cases
- **Sahitya**, the learner chatbot — answers progress/roadmap questions and can swap a course for its
  foundational alternative on request
- **Trainer Studio** — priority mode: quiz from memory's weak areas + recommended course transcripts;
  upload mode: PDF/TXT → chunked + embedded into Pinecone → retrieved chunks ground the MCQs
- **Read-only accounts** (`role='readonly'`) — 9 state-mutating endpoints (enroll, submit, complete,
  chat, …) reject writes server-side; used for the pre-onboarded Banking persona below
- **Org analytics** — competency distribution, completions, predictive capacity-building needs

## Demo logins

Three personas, seeded automatically on first run (no manual setup):

| Persona | Email | Password | Notes |
|---|---|---|---|
| Officer / Analyst (ISRO) | `demo@gov.in` | `demo123` | Fresh learner — assessment unlocks the roadmap |
| Training Administrator (NSSTA) | `admin.nssta@mospi.gov.in` | `demo123` | Org Analytics dashboard, not the learner view |
| Deputy Advisor (Banking) — **read-only** | `deputyadvisor@banking.gov.in` | `demo123` | Pre-seeded assessment + course history; login shows a "we found your existing records" popup instead of the first-time assessment prompt |

Officer/Admin personas are pickable on `register.html`; the read-only Banking persona logs in
directly via `login.html` (its history is meant to already exist, not be created at registration).

## Run it

```bash
# 1. backend deps (Python 3.12+)
cd backend && pip install -r requirements.txt

# 2. configure keys (backend/.env — never commit)
ANTHROPIC_API_KEY=...          # or OPENAI_API_KEY / OPENAI_BASE_URL for Azure OpenAI
LLM_MODEL=claude-sonnet-4-20250514
PINECONE_API_KEY=...
PINECONE_INDEX=setu-stat
# Without any LLM key, everything still works via the deterministic fallback generator.

# 3. start backend (port 8001; 8000 is taken by unrelated apps on some machines)
python3 -m uvicorn main:app --port 8001

# 4. start frontend
cd ../dummy-igot && python3 -m http.server 8090

# open http://localhost:8090 → Login or Register with one of the demo personas above
```

## API map (backend, port 8001)

| Area | Endpoints |
|---|---|
| Auth (dummy) | `POST /api/auth/register`, `POST /api/auth/login`, `POST /api/auth/logout`, `GET /api/auth/me`, `POST /api/auth/reset-demo` |
| Catalogue (Sunbird-shaped) | `POST /api/v1/content/search`, `GET /api/v1/content/read/{id}`, `GET /api/courses/search/semantic` |
| Enrollments | `POST /api/enrollments`, `GET /api/enrollments` |
| Assessment | `GET /api/assessment/questions`, `POST /api/assessment/submit` |
| Memory + gaps + roadmap | `GET /api/dashboard`, `GET /api/roadmap`, `GET /api/roadmap/{course}` |
| Module & lesson learning | `POST /api/roadmap/{c}/module/{n}/quiz`, `POST /api/roadmap/{c}/module/{n}/complete`, `POST /api/roadmap/{c}/lesson/{m}/{v}/quiz`, `POST /api/roadmap/{c}/lesson/{m}/{v}/complete` |
| Coding labs | `GET /api/roadmap/{c}/lab/{n}`, `GET /api/roadmap/{c}/lab/{n}/status`, `POST /api/roadmap/{c}/lab/{n}/complete` |
| Personalized quizzes | `GET /api/quiz/personalized`, `POST /api/quiz/personalized/submit`, `GET /api/personalized/preview`, `POST /api/personalized/generate`, `POST /api/personalized/{id}/grade` |
| Trainer materials | `POST /api/materials/upload`, `POST /api/materials/{id}/generate-quiz`, `POST /api/materials/quizzes/{id}/grade` |
| Sahitya (chatbot) | `POST /api/chat`, `GET /api/chat/history` |
| Reference data | `GET /api/tpac/pathways`, `GET /api/taxonomy`, `GET /api/roles` |
| Admin | `GET /api/admin/analytics`, `POST /api/admin/seed-demo-data`, `GET /api/health` |

Endpoints that mutate learner state (enroll, submit, complete, chat, …) require a *writable* account —
readonly accounts get a 403.

## Demo notes

- Demo DB: `backend/igot.db` (SQLite, auto-created; delete for a fresh start — all three demo
  personas above, including the Banking account's pre-seeded history, reseed automatically).
- Ports: frontend 8090, backend 8001 (8000 is commonly occupied).
- Keys live in `backend/.env` — never commit. Pinecone index auto-creates on first run.
- For judges: reset with `rm backend/igot.db`, log in with any persona above, and the whole loop
  runs live (no manual seeding needed).

## Deployment (Vercel frontend + Render backend)

The frontend resolves its API base automatically: `localhost` → `http://localhost:8001`,
any other hostname → the deployed Render URL (override by setting `window.IGOT_API_BASE`
before page scripts).

### Backend → Render
1. Render dashboard → New → Blueprint → point at this repo (`render.yaml` is at the root).
2. Fill in the `sync: false` env vars when prompted: your LLM key(s), `PINECONE_API_KEY`.
3. Render builds with `requirements.txt`, starts `uvicorn main:app --host 0.0.0.0 --port $PORT`,
   and health-checks `/api/health`. Auto-deploys on every push to `main`.
   (If you use a different service name, update the fallback URL in `dummy-igot/common.js`.)

### Frontend → Vercel
1. Vercel → Add New Project → import the repo.
2. Set **Root Directory** to `dummy-igot` (framework preset: Other — it's static).
3. Deploy — `vercel.json` handles clean URLs + security headers. Auto-deploys on push to `main`.

### CI/CD
`.github/workflows/ci.yml` runs on every push/PR to `main`:
- **backend job** — installs `requirements.txt` on Python 3.12, imports the app (catches route/model
  definition errors), boots uvicorn and smoke-tests `/api/health` + catalogue search.
- **frontend job** — verifies every page uses the `IGOT_API_BASE` resolver (no hardcoded localhost),
  and all pages exist.
- **deploy jobs** — trigger the Render deploy and run `vercel deploy --prod` after CI passes.

Also included: `backend/check_roadmap_integrity.py` — a standalone script (not wired into CI) that
flags a video ID reused across courses with no shared competency area, the exact bug class behind a
course silently playing another department's lecture.

### Production caveat (intentional for the demo)
Render's free tier has an **ephemeral disk** — `igot.db` (SQLite) resets on redeploy/restart, so
demo user/assessment data lives only between restarts. For a persistent demo, attach a Render Disk
at `/opt/render/project/src/backend` or point `DB_PATH` at Postgres later
