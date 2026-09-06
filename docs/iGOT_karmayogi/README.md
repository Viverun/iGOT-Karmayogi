# MoSPI - iGOT Karmayogi AI Skill Intelligence Platform
### *AI Skill Intelligence & Learning Layer for India's Official Statistical System*
**Ministry of Statistics and Programme Implementation (MoSPI) & National Statistical Systems Training Academy (NSSTA)**  
*Problem Statement 26101 (Smart India Hackathon 2026)*

---

## 🏛️ Executive Domain Overview
India's Official Statistical System under **MoSPI** and training organizations like the **NSSTA** is transitioning toward Big Data Analytics, GIS, cloud computing (MeghRaj), and AI. While the Government of India's **iGOT Karmayogi** portal provides extensive training content, it previously lacked a domain-tailored competency intelligence layer capable of mapping specialized statistical roles, conducting automated target-actual gap analyses, and dynamically generating Bloom's-level assessments from internal statistical manuals.

This platform bridges this gap with an autonomous AI Skill Intelligence Layer providing:
1. **Dynamic MoSPI Competency Taxonomy** spanning 4 pillars (Statistical, Technical, Digital Governance, Behavioural/Managerial).
2. **Vectorized Skill Gap Assessment Engine** calculating Target vs. Actual matrices, cosine similarity, and natural language explainable recommendations.
3. **Dual Integration with iGOT Karmayogi & NSSTA TPAC Pathways** with simulated bidirectional REST APIs and automated competency accreditation.
4. **AI-Powered RAG Assessment & MCQ Engine** with Bloom's Taxonomy, robust statistical distractors, citation tracing, and a Trainer Enablement Studio.
5. **Workforce Macro Analytics & Predictive Capacity Modeling** visualizing regional heatmaps across 6 NSSO FOD zones and forecasting modernization velocity through 2028.

---

## 🚀 Key System Capabilities & Architecture

```
                       ┌─────────────────────────────────────────────────┐
                       │    MoSPI / iGOT Skill Intelligence Platform     │
                       └────────────────────────┬────────────────────────┘
                                                │
       ┌───────────────────┬────────────────────┼────────────────────┬──────────────────┐
       ▼                   ▼                    ▼                    ▼                  ▼
┌──────────────┐   ┌───────────────┐   ┌──────────────────┐   ┌──────────────┐   ┌──────────────┐
│  Competency  │   │   Skill Gap   │   │ Recommendations  │   │ Quiz & MCQ   │   │  Analytics   │
│ Framework &  │   │  Assessment   │   │ (iGOT + NSSTA    │   │ Engine (LLM  │   │ Dashboards   │
│ Profiling    │   │    Engine     │   │     TPAC)        │   │    + RAG)    │   │ (Learner/Adm)│
└──────────────┘   └───────────────┘   └──────────────────┘   └──────────────┘   └──────────────┘
```

### 1. Dynamic Competency Framework & Profiling
- **4 Core Pillars**:
  - **Statistical Competencies**: Survey Design, Sampling Techniques, National Accounts, Price/Labour/Agricultural/Industrial Statistics, SDG Indicators, Metadata Standards, Data Quality Frameworks.
  - **Technical Competencies**: Python, R Programming, SQL, Stata, SPSS, SAS, GIS & Spatial Analytics, Data Visualization, AI/ML, Cloud Infrastructure, APIs, Open Data.
  - **Digital Governance**: Cybersecurity & CERT-In, Data Privacy & DPDP Act 2023, Digital Signatures / e-Office, MeghRaj Cloud, Digital Public Infrastructure (DPI).
  - **Behavioural & Managerial**: Public Leadership, Ethics & Integrity, Project Management, Evidence-Based Decision Making, Change Management.
- **Realistic MoSPI Job Roles**: Pre-configured baselines for:
  - *Director - National Accounts Division (NAD)*
  - *Field Officer (JSO) - NSSO Field Operations Division (FOD)*
  - *Senior Statistical Officer / Data Analyst - Price Statistics Division (PSD)*
  - *Joint Director - Survey Design & Research Division (SDRD)*
  - *Deputy Director - Computer Centre (IT & AI Directorate)*
  - *Statistical Officer - Labour Bureau & Social Statistics*
- **Role Progression Simulator**: Allows an officer to preview how their competency radar and skill gaps shift upon promotion or departmental transfer.

### 2. Skill Gap Assessment & Recommendation Engine
- **Target vs. Actual Matrix**: Quantifies gap scores: `Gap = max(0, Target - Actual)`.
- **Cosine Similarity**: Vectorizes profile vectors against role baseline vectors.
- **Explainable AI Recommendations**: Explains *why* each course is recommended (e.g., *"Recommended with Critical priority because your designation 'Director' in NAD mandates a baseline of 85 for Stata, where a 35-point deficit was detected..."*).
- **1-Click iGOT Progress Sync**: Simulates completing an iGOT module via webhooks, adding verified training hours and automatically upgrading the officer's competency score.

### 3. AI-Powered RAG Assessment & MCQ Engine
- **Multimodal Document Ingestion**: Pre-loaded with official MoSPI manuals (NSSO 78th Round Survey Design, National Accounts GVA Methodology, Price Statistics CPI SOP) with support for custom PDF/TXT guideline uploads.
- **Bloom's Taxonomy Classification**: Recall, Application, and Analysis levels.
- **Robust Statistical Distractors**: Handcrafted to target real-world statistical pitfalls (e.g., confusing sampling bias with selection bias, Laspeyres vs Paasche index substitution bias, soft vs hard CAPI validation errors).
- **Citations**: Traces answers back to specific document sections and pages.
- **Trainer Enablement Studio**: Allows NSSTA and MoSPI instructors to dynamically synthesize, review, and deploy custom tests in minutes.

### 4. Dual Dashboards & Workforce Analytics
- **Learner Dashboard**: Interactive Competency Radar chart, 4-pillar progress bars, gap highlight table, explainable course recommendations, and certified training logs.
- **Admin / HR Dashboard**: Macro telemetry across 4,820 statistical officers, aggregate readiness distribution across 6 NSSO FOD field zones (North, South, East, West, Central, North-East), division deficiency heatmaps, training velocity curves, and predictive AI capacity projections for 2025–2028.
- **iGOT Interoperability Gateway**: Live inspector displaying simulated REST payloads, OAuth2 tokens, and webhook transactions.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, Vite, TypeScript, Tailwind CSS, Recharts (Radar, Area, Bar, Heatmap), Lucide Icons |
| **Backend API** | Python 3.13, FastAPI, Pydantic v2, Uvicorn |
| **Data & Vector Store** | Scikit-learn (TF-IDF & Cosine Vector Sim), In-Memory Vector Store, JSON Store |
| **RAG & NLP** | Semantic chunking, Bloom's Taxonomy Prompt Engine, PyMuPDF / pypdf document extractor |
| **Interoperability** | Simulated iGOT Karmayogi RESTful Webhook endpoints, OpenID Connect compliance |

---

## ⚡ Quick Start & Execution

### 1. Start Both Services via Launcher (Windows)
Double-click `start_platform.bat` in the project root, or execute:
```cmd
.\start_platform.bat
```

### 2. Manual Start

#### Backend:
```powershell
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation (Swagger UI): **http://127.0.0.1:8000/docs**

#### Frontend:
```powershell
cd frontend
npm run dev
```
Platform Web UI: **http://localhost:5173**

---

## 🧪 Verification & Automated Tests
Run the backend test suite:
```powershell
python backend/test_pipeline.py
```
This tests all 6 core subsystems:
1. Taxonomy & Roles integrity
2. Officer profiling & Gap Analysis execution
3. Recommendation Engine scoring & Explainable text
4. iGOT Karmayogi simulated progress sync & Competency score upgrade
5. RAG Document Ingestion & MCQ Generation with Bloom's Taxonomy
6. Macro Workforce Analytics computation

Verify Frontend Production Build:
```powershell
cd frontend
npm run build
```

---

## 🏆 Hackathon Winning Features (PS 26101 Differentiation)
- **Deep MoSPI Domain Fidelity**: Real official roles (ISS SAG, SSS JSO/SSO) and authentic statistical methodologies (PPSWR sampling, Laspeyres geometric mean CPI, SNA 2008 FISIM, CAPI validation rules).
- **Explainable AI**: Transparent natural language justifications for every recommended learning pathway.
- **No Paid API Dependency Required**: Runs immediately with rich offline statistical domain data, while also featuring dynamic ingestion for new PDFs and guideline documents.
- **Interoperability Inspector**: Dedicated gateway displaying raw simulated iGOT REST requests and webhooks to prove plug-and-play capability to jury evaluators.
