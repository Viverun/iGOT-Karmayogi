# SIH PS 26101 — AI-Enabled Skill Intelligence & Learning Platform (MoSPI/DIID)

## Context

This is a fresh project directory (no existing code) for a Smart India Hackathon submission against
problem statement **26101** (MoSPI / Data Informatics & Innovation Division). The ask: an AI platform
that (1) builds a competency profile for officials in India's Official Statistical System, (2) finds
skill gaps against a competency framework, (3) recommends personalized learning by integrating with
**iGOT Karmayogi**, and (4) auto-generates MCQs/quizzes from uploaded learning material. The user asked
for research before building: domain/competitor landscape, a concrete solution architecture, and a
feasibility read on the two hardest AI features. This document is that research output plus a
recommended build plan — no code has been written yet.

## Domain research findings

**iGOT Karmayogi is built on Sunbird, which is open source.** This is the single most important fact
for this PS: iGOT is not a closed black box. It runs on the **Sunbird Ed** stack (Sunbird RC for
registries/credentials), which is open-source (Apache/MIT-licensed components) with public developer
docs and a public API reference:
- https://ed.sunbird.org/use/source-code/apis (Sunbird ED APIs)
- https://project-sunbird.github.io/apis/ (Sunbird API reference)
- https://lern.sunbird.org/learn/product-and-developer-guide/batch-service/api-documentation (batch/enrollment APIs)
- https://github.com/Sunbird-Ed (source)

Sunbird APIs are REST, JSON-over-HTTPS, versioned (`/{module}/{version}/{api_name}`), and cover: content
search, course/content read, batch creation & enrollment, user progress/assessment tracking. For a
hackathon, the realistic "iGOT integration" is: build against the **public Sunbird API contract**
(content search + enrollment + progress) and, if possible, stand up a local Sunbird ED sandbox for a
live demo — rather than assuming production MoSPI credentials will be issued. Judges will know this
platform is Sunbird-based, so citing this explicitly (rather than hand-waving "we'll call iGOT's API")
is a credibility signal.

**Competency framework — FRAC (Framework of Roles, Activities and Competencies).** Mission Karmayogi
already defines the competency model to reuse rather than invent:
- Competency types: **Behavioural**, **Functional**, **Domain** — matches almost exactly the PS's own
  four buckets (Statistical / Technical / Digital Governance / Behavioural-Managerial competencies).
- Reference docs: https://www.istm.gov.in/uploads/mission_karmayogi/Introduction.pdf (FRAC intro pack),
  https://dopt.gov.in/schemes/national-programme-civil-services-and-capacity-building-npcscb-mission-karmayogi
- Recommendation: model the competency taxonomy as FRAC-compatible (role → activity → competency →
  proficiency level) so scores could plausibly feed back into the real FRAC dictionary later. This is
  a strong differentiator to call out in the pitch.

**No existing "AI skill-gap + iGOT" product found** in public search — this specific combination
(FRAC-aware competency engine + iGOT/Sunbird course recommendation + LLM MCQ generation) doesn't appear
to exist as an off-the-shelf tool. Adjacent pieces exist separately and can be reused as reference
implementations:
- Resume/competency-gap analyzers using NLP + skill taxonomies (e.g. FastAPI + sentence-transformers
  semantic matching pattern) — same technique applies to matching an official's profile against FRAC
  competencies instead of a job description.
- RAG-based quiz/MCQ generators are a well-trodden pattern (see below).

## AI feature feasibility

**1. Competency/skill-gap mapping (NLP + LLM).** Feasible at hackathon scope using a **semantic
similarity, not classification-from-scratch** approach:
- Define the competency taxonomy as structured data (FRAC-style: domain → competency → proficiency
  descriptors 1–5), seeded from the PS's own listed competencies (Survey Design, Sampling, Python/R/SQL,
  Cybersecurity, Leadership, etc.).
- Embed each competency description and each piece of evidence about the official (designation, past
  courses completed, self-declared skills, course completion history from iGOT) using a sentence
  embedding model; score current proficiency via cosine similarity + a small LLM pass to resolve
  ambiguous cases and produce a human-readable gap explanation.
- This is the same pattern used by open-source resume/skill-gap tools (e.g. `ai-resume-analyzer` on
  GitHub) — reusable technique, not reusable code (different domain data).
- Realistic scope for a hackathon demo: rules + embeddings for scoring, LLM only for explaining gaps
  and drafting the recommendation rationale — full custom ML training is not needed and would be
  over-engineering for the timeline.

**2. MCQ/quiz generation from uploaded material.** This is the most mature part of the ask — a standard
RAG pattern with many public references (Databricks "Generating Quizzes with RAG and LLMs", academic
work on concept-map-based MCQ generation with distractor quality, Kaggle RAG-MCQ notebooks):
- Pipeline: chunk uploaded doc (PDF/PPTX/video transcript) → embed chunks into a vector store → per
  chunk/topic, prompt an LLM for question + correct answer + plausible distractors + explanation →
  validator pass (second LLM call or rule-based check) to filter low-quality items.
- Key risk callouts to design around: distractor quality (a known weak point — plausible-but-wrong
  options are harder to generate than the question itself) and hallucinated "facts" not present in the
  source doc — mitigate by grounding every generated question in a cited source chunk and rejecting
  ungrounded ones.
- This is buildable end-to-end in the hackathon window; it's the safest AI feature to demo live.

## Architecture decision: separate AI system + dummy iGOT (not a fork of iGOT itself)

Three options were considered:
1. **Integrated** — build all AI features directly into iGOT Karmayogi's own dashboard end-to-end.
2. **Separate** — a standalone AI system (competency engine, recommendations, MCQ generation, both
   dashboards) that talks to iGOT purely over its API contract.
3. **Mixed** — some components folded into iGOT's UI, some standalone.

**Decision: option 2**, plus building a **thin dummy iGOT** to demo the integration against, rather than
the real platform. Reasoning:
- Option 1 isn't actually buildable: the team has no access to MoSPI's deployed iGOT codebase or the
  ability to change its live dashboard — only the documented Sunbird API surface. So "integrated"
  architecture would be integrated in name only.
- A separate service is also the realistic *production* integration pattern for a platform at iGOT's
  scale — third-party capability is bolted on as a companion service via API, not merged into the core
  LMS codebase. This makes option 2 defensible as "how this would actually ship," not just a hackathon
  shortcut.
- It cleanly separates what's being judged (the AI product) from scaffolding (the dummy iGOT exists only
  to prove the integration contract is real).
- Option 3 has no separate "main site" of the team's own to partially merge into, so it doesn't apply
  here — there's only the dummy iGOT (kept minimal) and the product (the full build).

**Dummy iGOT scope — deliberately thin:** course catalogue listing, an enrollment action, and a
completion/progress status that can be toggled (manually, or via a mock webhook) to simulate a learner
finishing a course. Its only job is to (a) look credible to judges as "the platform we integrate with"
and (b) give the connector real Sunbird-shaped API responses (catalogue search, enrollment, progress) to
work against — see the Sunbird API references above for the schemas to mirror.

**Integration touchpoint (avoid "two disconnected apps" feel):** the dummy iGOT's employee dashboard
should carry a visible widget/button — e.g. "View my skill gaps & recommendations" — that deep-links
(ideally via shared SSO session) into the AI system. The dummy iGOT stays content/enrollment-only; the
AI system owns all competency scoring, gap analysis, recommendations, MCQ generation, and both the
employee and admin analytics dashboards.

## Recommended solution architecture

```
┌────────────────────────────┐        ┌───────────────────────────────────────────────────────────────┐
│  Dummy iGOT Karmayogi        │◄──────►│  AI System (the real product)                                   │
│  (thin, Sunbird-API-shaped) │  API    │                                                                   │
│  - Course catalogue          │  calls │  Frontend (Next.js)                                              │
│  - Enrollment action         │  both  │  - Employee dashboard (competency radar, gaps, recommendations)  │
│  - Completion/progress       │  ways  │  - Admin dashboard (org-wide analytics, predictive workforce)     │
│  - "View my skill gaps" →────┼───────►│  - Trainer console (upload material → generated quiz review)     │
└────────────────────────────┘        └───────────────┬───────────────────────────────────────────────--┘
                                                       │ REST/GraphQL, SSO (OAuth2/SAML) + RBAC
                                       ┌───────────────▼───────────────────────────────────────────────--┐
                                       │  Backend API (FastAPI or Node/NestJS)                            │
                                       │  - Auth & RBAC service                                            │
                                       │  - Competency Engine: FRAC-style taxonomy store + gap scoring     │
                                       │  - Recommendation Engine: embeddings + rules over iGOT catalogue  │
                                       │  - Assessment Engine: upload → chunk → RAG → MCQ/quiz generation  │
                                       │  - iGOT Connector: wraps Sunbird content/search/enrollment APIs   │
                                       └───────┬───────────────────────┬───────────────────┬─────────────┘
                                               │                       │                   │
                                       ┌───────▼──────┐     ┌──────────▼─────────┐  ┌──────▼───────────┐
                                       │ Postgres      │     │ Vector DB           │  │ Object storage    │
                                       │ (profiles,    │     │ (pgvector/Chroma/   │  │ (uploaded docs,   │
                                       │  competencies,│     │  FAISS) for course   │  │  slides, videos)  │
                                       │  scores,      │     │  + material          │  │                   │
                                       │  enrollments) │     │  embeddings          │  │                   │
                                       └───────────────┘     └─────────────────────┘  └───────────────────┘
                                               │
                                       ┌───────▼───────────────────────────────────────────────────────┐
                                       │  LLM layer (provider-agnostic: OpenAI/Anthropic/local via       │
                                       │  vLLM for offline-capable govt deployment) — used for:          │
                                       │  gap explanations, recommendation rationale, MCQ generation,     │
                                       │  virtual assistant chat                                          │
                                       └───────────────────────────────────────────────────────────────┘
```

Data flow: dummy iGOT → AI system for course catalogue, enrollment status, completion/progress (pull or
mock webhook); AI system → dummy iGOT only as deep-links/enrollment calls for recommended courses. MCQ
generation is entirely internal to the AI system (trainer uploads material, no iGOT involvement).

**Tech stack recommendation** (optimized for hackathon build speed + judge-legible "production-ready"
story):
- Backend: **FastAPI** (Python) — same language as the AI/NLP stack, avoids a service-boundary rewrite.
- Frontend: **Next.js + Tailwind**, charting via Recharts for dashboards.
- DB: **Postgres** (+ **pgvector** extension) so relational competency data and embeddings live in one
  store instead of standing up a separate vector DB — simpler ops story for a govt deployment pitch.
- LLM: provider-agnostic wrapper (LiteLLM or a thin adapter) so the pitch can say "works with any
  empanelled/GPU-hosted model," with an actual demo call to Claude/GPT for the working prototype.
- Auth: OAuth2/OIDC for SSO, RBAC middleware — mirrors the PS's explicit ask for SSO + RBAC.
- iGOT integration: a connector module against the **public Sunbird ED API contract**; for the demo,
  either mock responses shaped exactly like Sunbird's real schema, or run a local Sunbird ED sandbox
  seeded with sample courses.

## Suggested next steps (not yet executed)

1. Pull the FRAC intro pack and Sunbird API reference in detail to lock exact field names/schemas
   before writing the connector, the dummy iGOT's mock endpoints, and competency-taxonomy seed data.
2. Decide and scope an MVP slice for the hackathon demo (dummy iGOT + competency profile + gap scoring +
   recommendation + MCQ generation from one uploaded doc + both dashboards) vs. full PS scope.
3. Once scope is picked, come back for an implementation plan/build (this document is research +
   architecture only, per what was asked).

## Verification

No code exists yet, so nothing to run. When implementation starts: verify the Sunbird connector against
the public API reference with a mock/sandbox Sunbird instance, verify MCQ generation groundedness by
spot-checking generated questions cite real source-doc passages, and verify competency scoring by
manually checking a handful of official profiles against expected proficiency levels.
