# SIH 26101 — SETU-STAT: Project Context & Work Log

**Repo:** github.com/Viverun/iGOT-Karmayogi (branch `main`)
**Live:** https://igot-karmayogi.vercel.app (frontend) · https://igot-karmayogi-zs8h.onrender.com (backend)
**Period covered:** Sep 5 (yesterday) – Sep 6 (today)
**Purpose:** context handoff — everything built, decided, fixed, and why.

---

## 1. What this project is

An AI-enabled Skill Intelligence & Learning Platform for India's Official Statistical
System (SIH PS 26101, MoSPI/DIID), built as **SETU-STAT** (Statistical Training &
Evaluation Unified platform). It sits **alongside** iGOT Karmayogi (not a fork):

- **Dummy iGOT** (`dummy-igot/`) — a faithful replica of the iGOT portal as the demo
  entry point: landing page, read-only registration, dashboards, course player,
  trainer studio, analytics.
- **AI backend** (`backend/`) — FastAPI service implementing persistent competency
  memory, skill-gap analysis, personalized roadmaps, transcript-grounded quiz
  generation, and org analytics.
- The two talk over a **Sunbird-shaped API contract**, so the dummy iGOT connector is
  a drop-in replacement for the real iGOT APIs on day one of access.

Full research/architecture: `docs/plan-of-action.md` and
`docs/SETU-STAT_SIH26101_Solution_Blueprint.pdf`.

---

## 2. Timeline of work

### Yesterday (Sep 5)

1. **Dummy iGOT landing page** (`dummy-igot/index.html`) — replica of the official
   portal: floating pill navbar, peach hero with "1.7 Crore+ Users Onboarded" confetti
   card, blue stats band (official counters), analytics cards (Rule-to-Role CBPs,
   Courses-by-Competency pie, Democratised Learning bars, eHRMS), **India choropleth**
   (D3 + TopoJSON in `assets/india.topo.json`), course carousels, Amrit Gyaan Kosh.
   5-second "demo landing page" popup pointing to Register (once per session, with
   "Explore on my own" opt-out).
2. **Tech decisions** — FastAPI backend (Python), static Tailwind frontend (no build
   step), SQLite for demo storage (pgvector-style embeddings moved to Pinecone),
   provider-agnostic LLM adapter (Azure OpenAI `gpt-5-mini` + `text-embedding-3-small`),
   Pinecone vector DB, Sunbird-shaped mock catalogue with 14 real iGOT courses.
3. **Read the SETU-STAT solution blueprint** (docs PDF) and aligned the build to it
   (three pillars: Diagnose / Prescribe / Assess).
4. **Registration** — replicated the real iGOT Register screen from a reference
   screenshot: Center/State radios, Ministry "Department of Space and ISRO HQ",
   Organisation "Advanced Data Processing Research Institute (ADRIN)", Designation
   "Analyst", Email `analyst@adrin.gov.in` — all **read-only**, single **Register**
   button (no OTP), which creates the account, logs in, and lands on the dashboard.
   Navbar shows Register only for guests; "Go to Dashboard + Log out" when signed in.
5. **Welcome popup** on the dashboard (not the landing page): slide 1 "Welcome, {name}"
   → Next → slide 2 "Take Assessment". "Maybe later"/"Later" dismiss it; it never
   appears again once the assessment is done (gated on `assessment_done` from the DB,
   plus once-per-session via sessionStorage).
6. **Backend built end-to-end** (verified for the ISRO user):
   - Dummy auth (register/login/logout/me), SQLite at `backend/igot.db`.
   - Sunbird-shaped catalogue: `POST /api/v1/content/search`,
     `GET /api/v1/content/read/{id}` — 14 seeded real courses (`data/courses.json`).
   - Enrollments with progress + completion.
   - Department-aware assessment: 25 questions for the space track
     (9×L1, 9×L2, 9×L3 → totals 25; statistics and general sets exist too), graded
     server-side, stored in `assessment_results`.
   - **Persistent memory**: `user_competency` (EWMA: 60% history + 40% new evidence),
     `chapter_progress`, `lesson_quizzes`, `personalized_quizzes`, `learning_events`
     (full audit trail), `roadmaps` (JSON), `materials`, `generated_quizzes`,
     `transcripts` (cached YT transcripts with an `indexed` flag).
   - **Gap engine**: per-area `Gap = max(0, target − current)` against department
     target profiles (`ontology.py`), with explainable reasons.
   - **Roadmap recommender**: phases Foundations→Core→Advanced, gap-severity ranked,
     prerequisite-aware, stored and auto-refreshed on every score change.
   - **Readiness metric** (final form): per-area contribution clamped at the role
     target; assessments alone cap readiness at **30%**; each **verified completion**
     (course finished + avg quiz score ≥ 60) raises the cap by **+14%** up to 100.
   - Dashboard + admin analytics endpoints.

### Today (Sep 6)

7. **LLM + vector layer wired**:
   - `backend/.env` (gitignored) holds keys: `OPENAI_API_KEY`,
     `OPENAI_BASE_URL=https://khanjamilahmed202-3046-resource.openai.azure.com/openai/v1`,
     `LLM_MODEL=gpt-5-mini`, `EMBEDDING_MODEL=text-embedding-3-small`,
     `PINECONE_API_KEY`, `PINECONE_INDEX=setu-stat`, `TRANSCRIPT_PROXY`,
     `SUPADATA_API_KEY`. Loaded by `env_config.py` (setdefault → real env wins).
   - **Pinecone** serverless index `setu-stat` (aws us-east-1), namespaces:
     `courses` (catalogue embedded at startup), `materials` (uploaded docs),
     `transcripts` (lecture transcripts, indexed at fetch time).
   - Personalized MCQ generation: user's weakest areas → embedded query → top
     transcript/material chunks → gpt-5-mini with a strict "only from context" prompt.
8. **Frontend app pages** (all share `common.js`: API resolver, auth guard, header,
   footer): `dashboard.html` (readiness ring, radar, gap bars, roadmap,
   continue-learning, catalogue), `learn.html` (iGOT-course chapter flow),
   `course_player.html` (roadmap course player with embedded YouTube), `quiz.html`
   (personalized practice), `studio.html` (trainer), `admin.html` (org analytics).
   Fixed a class of bug where inline `onclick` couldn't see block-scoped functions
   (exported to `window`).
9. **ISRO roadmap** (`roadmap_data.py`): 5 courses from real platforms (IIRS/ISRO
   Outreach, NPTEL IIT Kharagpur, freeCodeCamp+NPTEL, NPTEL satcom/GNSS,
   ISRO/NRSC Bhuvan-NDEM track), each with 3 modules of real YouTube videos,
   delivered via an **on-site embedded player** (`course_player.html`) — learners
   never leave the site.
10. **Sequential progression**: lesson N+1 unlocks only after lesson N's quiz is
    **passed with ≥ 60**; module quiz gated on all lessons marked complete + previous
    module quiz passed. Failed quizzes get a **🔄 Retry** button (same stored
    questions, unlimited attempts).
11. **Transcript-grounded quizzes**: module (5 Qs) and lesson (5 Qs) quizzes generated
    by gpt-5-mini strictly from the lecture transcripts (fetched via
    `youtube-transcript-api`, cached in SQLite, **indexed into Pinecone at fetch
    time** with an `indexed` flag). Quiz generation retrieves semantically from
    Pinecone — no re-fetching, ever. Stored per user for fair retakes; fallback
    quizzes **self-upgrade** to transcript-grounded once available.
12. **Residential proxy + Supadata**: YouTube blocks cloud IPs (Render), so
    `TRANSCRIPT_PROXY` (IPFoxy residential, works) and `SUPADATA_API_KEY`
    (transcript API service, works) are both supported as fetch paths. All roadmap
    transcripts were fetched through the proxy and indexed into Pinecone.
13. **Trainer Studio** final form: (1) priority card — personalized assessment from
    memory's weak areas + recommended course, (2) course-scoped assessment — pick a
    roadmap course + 5/10/15/25/30 questions, (3) upload PDF/TXT → Pinecone-indexed →
    MCQs weighted toward weak areas. All AI/tooling mentions removed from the UI
    (no "gpt-5-mini/transcript/Pinecone" text shown to users).
14. **Deployment**: frontend on **Vercel**, backend on **Render** (Blueprint-style,
    `render.yaml` + `requirements.txt`), **GitHub Actions CI/CD** (`.github/workflows/ci.yml`):
    backend CI (install, import check, boot + smoke test), frontend CI (API-wiring and
    page checks), then CD → Vercel deploy (CLI from `dummy-igot/`) + Render deploy
    trigger (API). Plus **keep-alive cron** (`.github/workflows/keep-alive.yml`,
    every 5 min) so Render never sleeps.
15. **Final verification sweep**: 24/24 API end-to-end checks green on production;
    all 10 pages 200 with no JS errors/overflow; CI/CD green; favicon + logo live.

---

## 3. Key bugs found & fixed (learning notes)

- **Python 3.14 lazy annotations**: `ChapterCompleteBody` defined after the route that
  used it → FastAPI silently treated the body as a query param → 422. Fix: define
  request models before routes.
- **Inline `onclick` vs block scope**: handlers inside `if (requireAuth()) {}` blocks
  couldn't see page functions → exported via `Object.assign(window, {...})`.
- **Fallback quizzes stripped of answers**: `pick_questions` sanitizes answers for
  clients; the bank-fallback path stored stripped questions → grading KeyError 500.
  Fix: store answers server-side, strip only in responses.
- **Lesson-quiz regeneration**: unique-constraint crash on re-insert → `INSERT OR
  REPLACE`; fallback quizzes self-upgrade to LLM-grounded when available.
- **Transcript chunker**: transcripts are one continuous line → the old chunker made
  a single 49k-char chunk → embedding API 400 (8k-token input cap). Fix: split
  oversized paragraphs by word boundaries; embed in batches of 16 with 429
  retry/backoff.
- **Strength/weakness rule**: 100% score showed "weakness: Python". Fix:
  weakness only if some area < 100; strength only if some area > 0; UI handles
  empty cases ("Perfect score — no weaknesses detected 🎉").
- **Mark-complete popup**: auto-advance auto-clicked the next (locked) lesson →
  lock alert popup. Fix: removed auto-advance; scrolls to the unlocked Quiz button.
- **Vercel deploys**: two failure modes fixed — deploys from the wrong directory
  (always deploy from `dummy-igot/`; project Root Directory setting kept **unset**
  because CLI uploads root=dir contents), and a missing `actions/checkout` step in
  the CD job. Also: Vercel CLI OAuth tokens **expire/rotate** — if CI's Vercel job
  fails with "token not valid", refresh the `VERCEL_TOKEN` secret from
  `~/.local/share/com.vercel.cli/auth.json`.
- **Render deploy trigger**: returns HTTP 202 with an empty body — the CI check
  accepts 200/201/202.
- **Readiness > 100%**: clamped per-area at target + verified-completion cap
  (see §2.6).

---

## 4. File map (what lives where)

```
backend/
  main.py            FastAPI app — all routes (37), startup Pinecone indexing
  db.py              SQLite schema (12 tables) + init/migrations
  assessment.py      Question banks (space 25Q L1/L2/L3, statistics, general) + dept keywords
  ontology.py        Competency areas, dept target profiles, chapter titles
  gap_engine.py      EWMA memory, competency vector, gap scoring, roadmap builder,
                     chapter/lesson helpers, readiness metric
  roadmap_data.py    5 ISRO roadmap courses (modules + YouTube video IDs)
  transcripts.py     YT transcript fetch (direct → TRANSCRIPT_PROXY → Supadata),
                     SQLite cache, fetch-time Pinecone indexing
  materials.py       PDF/TXT extraction, chunking, MCQ generation (LLM or fallback)
  llm.py             Azure OpenAI adapter (gpt-5-mini reasoning-safe), prompts, JSON parsing
  vector_store.py    Pinecone (namespaces: courses, materials, transcripts)
  vector index of course catalogue at startup
  env_config.py      Loads backend/.env (setdefault; real env wins)
  data/courses.json  14 real iGOT courses (Sunbird-shaped seed)
  igot.db            SQLite (runtime, gitignored; delete for fresh demo)
  .env               KEYS — gitignored, never commit
dummy-igot/
  index.html         Public landing replica (Register-only CTA, 5s demo popup)
  register.html      Read-only registration → reset-demo → auto-login → dashboard
  dashboard.html     Employee dashboard (popup, readiness, radar, gated roadmap, catalogue)
  assessment.html    25Q assessment (L1/L2/L3 chips, progress bar, result breakdown)
  learn.html         iGOT catalogue course player (3 chapters + quizzes)
  course_player.html Roadmap course player (embedded YT, sequential locks, lesson/module quizzes)
  quiz.html          Personalized practice quiz
  studio.html        Trainer Studio (personalized / course-scoped / upload modes)
  admin.html         Org analytics (charts + predictive needs table)
  common.js          API base resolver, auth, header/footer, helpers
  assets/            logo.svg, favicon.svg, india.topo.json
.github/workflows/
  ci.yml             CI (backend+frontend) and CD (Vercel + Render) on push/PR to main
  keep-alive.yml     Cron */5 * * * * → ping /api/health (Render warm)
docs/                Blueprint PDF + research plan
README.md, start.sh, render.yaml, .gitignore
```

---

## 5. API surface (backend :8001; production behind the same paths)

| Area | Endpoints |
|---|---|
| Auth (dummy) | `POST /api/auth/register` · `POST /api/auth/login` · `POST /api/auth/logout` · `POST /api/auth/reset-demo` · `GET /api/auth/me` |
| Catalogue (Sunbird-shaped) | `POST /api/v1/content/search` · `GET /api/v1/content/read/{id}` · `GET /api/courses/search/semantic` |
| Enrollments | `POST/GET /api/enrollments` · `PATCH /api/enrollments/{id}` |
| Assessment | `GET /api/assessment/questions` · `POST /api/assessment/submit` |
| Roadmap | `GET /api/roadmap` · `GET /api/roadmap/{course}` |
| Module learning | `POST /api/roadmap/{c}/module/{n}/quiz` · `.../complete` |
| Lesson learning | `POST /api/roadmap/{c}/lesson/{m}/{v}/quiz` · `.../complete` |
| Personalized | `GET /api/quiz/personalized` · `POST /api/quiz/personalized/submit` · `GET /api/personalized/preview` · `POST /api/personalized/generate` · `POST /api/personalized/{id}/grade` |
| Trainer materials | `POST /api/materials/upload` · `POST /api/materials/{id}/generate-quiz` · `POST /api/materials/quizzes/{id}/grade` |
| Dashboards | `GET /api/dashboard` · `GET /api/admin/analytics` |
| Health | `GET /api/health` |

Demo credentials: `analyst@adrin.gov.in` / `demo123` (registration is one click and
auto-resets the demo session).

---

## 6. Demo script (judges)

1. Landing → 5s popup → **Register** (side note explains the demo user; all fields
   read-only; one click wipes prior memory and starts fresh).
2. Dashboard → welcome popup → "Take Assessment" (or "Later"; personalized section
   stays 🔒 locked until assessed).
3. **25-question assessment** (L1/L2/L3 chips) → roadmap unlocks (5 courses) and
   readiness shows a small number (≤ 30% cap — explainable).
4. Open **Fundamentals of Remote Sensing** → embedded IIRS/NPTEL lectures → mark
   lessons complete → **lesson quiz** (generated from that lecture's transcript) →
   pass ≥ 60 → next lesson unlocks → module quiz → readiness climbs.
5. **Trainer Studio** → generate a personalized quiz (weak areas) and a
   course-scoped 10-question quiz; or upload any PDF → instant grounded MCQs.
6. Back to dashboard: radar moved, gap explanations updated, readiness up (only via
   verified completions) → **Analytics** for the org view.

Reset for the next run: click Register again (auto-wipes), or
`POST /api/auth/reset-demo {"email":"analyst@adrin.gov.in"}`, or delete `igot.db`.

---

## 7. Known limitations (accepted, by design)

- Render free tier: **ephemeral disk** (memory resets on redeploy) and sleep after
  15 min idle (mitigated by the keep-alive cron; first hit after sleep is slow).
  Production-grade fix: Render Disk or Postgres.
- YouTube blocks cloud IPs: on Render, transcripts come via `TRANSCRIPT_PROXY`
  (IPFoxy residential) or `SUPADATA_API_KEY`; the 4 IIRS lectures have no captions
  anywhere → knowledge-based quiz fallback for those lessons.
- Auth is **dummy** (no hashing/JWT) — intentional for the demo; SSO is the
  production path per the blueprint.
- Azure embedding quota is small: large transcripts index slowly (retries built in).
- GitHub scheduled workflows auto-pause after ~60 days of repo inactivity — re-enable
  from the Actions tab if the keep-alive stops.
- Vercel CLI OAuth tokens expire; if CI's Vercel deploy fails with "token not valid",
  refresh `VERCEL_TOKEN` from `~/.local/share/com.vercel.cli/auth.json`.
