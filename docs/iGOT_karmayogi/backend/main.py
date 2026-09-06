"""
FastAPI Application: AI Skill Intelligence & Learning Platform for MoSPI / iGOT Karmayogi / NSSTA
Exposes complete REST API suite for competency profiling, skill gap evaluation,
RAG-based assessment generation, iGOT simulated endpoints, and workforce macro analytics.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import datetime
import os

try:
    from .taxonomy import TAXONOMY, COMPETENCY_PILLARS, get_taxonomy_by_pillar
    from .roles_data import STANDARD_ROLES, RoleDefinition
    from .officers_data import SAMPLE_OFFICERS, OfficerProfile, TrainingLog
    from .igot_service import (
        IGOT_CATALOG, TPAC_PATHWAYS, AUDIT_LOGS,
        log_api_call, fetch_courses_by_competency, IGOTCourse
    )
    from .gap_engine import analyze_skill_gap, GapAnalysisReport
    from .rag_engine import RAG_INSTANCE, AssessmentTest
    from .analytics_engine import generate_macro_workforce_analytics, MacroWorkforceReport
except (ImportError, ValueError):
    from taxonomy import TAXONOMY, COMPETENCY_PILLARS, get_taxonomy_by_pillar
    from roles_data import STANDARD_ROLES, RoleDefinition
    from officers_data import SAMPLE_OFFICERS, OfficerProfile, TrainingLog
    from igot_service import (
        IGOT_CATALOG, TPAC_PATHWAYS, AUDIT_LOGS,
        log_api_call, fetch_courses_by_competency, IGOTCourse
    )
    from gap_engine import analyze_skill_gap, GapAnalysisReport
    from rag_engine import RAG_INSTANCE, AssessmentTest
    from analytics_engine import generate_macro_workforce_analytics, MacroWorkforceReport

app = FastAPI(
    title="MoSPI - iGOT Karmayogi AI Skill Intelligence Platform",
    description="AI Skill Intelligence Layer for official statistical capacity building, gap analysis, and RAG assessments under MoSPI & NSSTA.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- 1. Taxonomy & Roles Endpoints -----------------

@app.get("/api/taxonomy")
def get_taxonomy():
    """Retrieve full MoSPI competency taxonomy across 4 pillars"""
    return {
        "pillars": COMPETENCY_PILLARS,
        "taxonomy": {k: v.model_dump() for k, v in TAXONOMY.items()},
        "by_pillar": get_taxonomy_by_pillar()
    }

@app.get("/api/roles")
def get_roles():
    """List all official MoSPI job roles with baseline requirements"""
    return {k: v.model_dump() for k, v in STANDARD_ROLES.items()}

# ----------------- 2. Officer Profiling & Gap Assessment -----------------

@app.get("/api/officers")
def list_officers():
    """List sample officers across ISS and SSS cadres"""
    return [o.model_dump() for o in SAMPLE_OFFICERS.values()]

@app.get("/api/officer/{officer_id}")
def get_officer(officer_id: str):
    """Retrieve profile and competency records for a specific officer"""
    officer = SAMPLE_OFFICERS.get(officer_id)
    if not officer:
        raise HTTPException(status_code=404, detail="Officer profile not found")
    return officer.model_dump()

@app.get("/api/gap-analysis/{officer_id}", response_model=GapAnalysisReport)
def get_gap_analysis(officer_id: str):
    """Execute dynamic Target vs. Actual skill gap assessment and explainable recommendations"""
    officer = SAMPLE_OFFICERS.get(officer_id)
    if not officer:
        raise HTTPException(status_code=404, detail="Officer profile not found")
    report = analyze_skill_gap(officer)
    return report

class RoleSwitchRequest(BaseModel):
    new_role_id: str

@app.post("/api/officer/{officer_id}/switch-role")
def switch_officer_role(officer_id: str, req: RoleSwitchRequest):
    """Simulate promotion or career transfer to evaluate career progression gap delta"""
    officer = SAMPLE_OFFICERS.get(officer_id)
    if not officer:
        raise HTTPException(status_code=404, detail="Officer profile not found")
    if req.new_role_id not in STANDARD_ROLES:
        raise HTTPException(status_code=400, detail="Invalid target role ID")
    
    officer.role_id = req.new_role_id
    role = STANDARD_ROLES[req.new_role_id]
    officer.designation = role.title.split(" - ")[0]
    return {"message": f"Officer role updated to {role.title}", "profile": officer.model_dump()}

# ----------------- 3. iGOT Karmayogi Simulated Interoperability Endpoints -----------------

@app.get("/api/igot/courses")
def get_igot_catalog(competency_id: Optional[str] = None):
    """Fetch iGOT Karmayogi Course Catalog (with simulated REST logging)"""
    courses = list(IGOT_CATALOG.values())
    if competency_id:
        courses = [c for c in courses if c.competency_id == competency_id]

    log_api_call(
        endpoint="/api/igot/courses",
        method="GET",
        status_code=200,
        request_payload={"filter_competency": competency_id},
        response_payload={"count": len(courses), "status": "SUCCESS"}
    )
    return [c.model_dump() for c in courses]

@app.get("/api/igot/tpac-pathways")
def get_tpac_pathways():
    """Retrieve official NSSTA Training Programme Advisory Committee (TPAC) tracks"""
    return TPAC_PATHWAYS

class SyncProgressRequest(BaseModel):
    officer_id: str
    course_id: str
    progress_percentage: int
    hours_logged: int
    score_achieved: Optional[int] = 85

@app.post("/api/igot/sync-progress")
def sync_course_progress(req: SyncProgressRequest):
    """
    Simulated iGOT Karmayogi Webhook: Synchronizes course completion,
    increments training hours, and automatically upgrades competency scores.
    """
    officer = SAMPLE_OFFICERS.get(req.officer_id)
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")
    
    course = IGOT_CATALOG.get(req.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found in iGOT catalog")

    # If course is completed (100%), add to training logs and boost competency score
    score_boost = 0
    if req.progress_percentage >= 100:
        existing_log = next((t for t in officer.training_history if t.course_id == req.course_id), None)
        if not existing_log:
            officer.training_history.append(
                TrainingLog(
                    course_id=course.course_id,
                    course_title=course.title,
                    source=course.provider,
                    completion_date=datetime.date.today().strftime("%Y-%m-%d"),
                    hours_spent=req.hours_logged or course.duration_hours,
                    score_achieved=req.score_achieved or 88
                )
            )
        
        # Upgrade competency score by course points award (capped at 98)
        current = officer.current_competencies.get(course.competency_id, 30)
        score_boost = min(course.points_award, 98 - current)
        officer.current_competencies[course.competency_id] = current + max(5, score_boost)

    log_api_call(
        endpoint="/api/igot/sync-progress",
        method="POST",
        status_code=200,
        request_payload=req.model_dump(),
        response_payload={
            "status": "PROCESSED",
            "competency_upgraded": course.competency_id,
            "new_score": officer.current_competencies.get(course.competency_id),
            "score_delta": f"+{max(5, score_boost)} points"
        }
    )

    return {
        "message": f"Progress synced for {course.title}. Competency score updated.",
        "new_score": officer.current_competencies.get(course.competency_id),
        "score_boost": max(5, score_boost),
        "officer": officer.model_dump()
    }

@app.get("/api/igot/audit-logs")
def get_audit_logs():
    """Retrieve simulated REST webhook transaction logs demonstrating interoperability"""
    return [l.model_dump() for l in AUDIT_LOGS]

# ----------------- 4. AI-Powered RAG Assessment & MCQ Engine -----------------

@app.get("/api/assessments")
def list_assessments():
    """List standard and generated MoSPI assessments"""
    return [
        {
            "test_id": t.test_id,
            "title": t.title,
            "description": t.description,
            "topic": t.topic,
            "document_source": t.document_source,
            "total_questions": t.total_questions,
            "duration_minutes": t.duration_minutes,
            "target_role": t.target_role,
            "created_by": t.created_by
        }
        for t in RAG_INSTANCE.tests_db.values()
    ]

@app.get("/api/assessment/{test_id}")
def get_assessment(test_id: str):
    """Fetch test with questions, Bloom's Taxonomy ratings, and option sets"""
    test = RAG_INSTANCE.tests_db.get(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return test.model_dump()

class SubmitTestRequest(BaseModel):
    officer_id: str
    answers: Dict[str, str] # question_id -> chosen_key (e.g. "Q1": "B")

@app.post("/api/assessment/{test_id}/submit")
def submit_assessment(test_id: str, req: SubmitTestRequest):
    """
    Submits user quiz answers, evaluates results, calculates Bloom's taxonomy performance,
    returns distractor explanations and citations, and updates officer competency score.
    """
    test = RAG_INSTANCE.tests_db.get(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    officer = SAMPLE_OFFICERS.get(req.officer_id)
    if not officer:
        raise HTTPException(status_code=404, detail="Officer not found")

    correct_count = 0
    feedback = []
    affected_competencies = set()

    for q in test.questions:
        user_ans = req.answers.get(q.id)
        is_correct = (user_ans == q.correct_key)
        if is_correct:
            correct_count += 1
        
        affected_competencies.add(q.competency_id)

        # Distractor analysis
        chosen_option = next((opt for opt in q.options if opt.key == user_ans), None)
        distractor_note = chosen_option.distractor_rationale if chosen_option else None

        feedback.append({
            "question_id": q.id,
            "question": q.question,
            "blooms_taxonomy": q.blooms_taxonomy,
            "user_answer": user_ans,
            "correct_answer": q.correct_key,
            "is_correct": is_correct,
            "explanation": q.explanation,
            "distractor_rationale": distractor_note,
            "source_citation": q.source_citation
        })

    score_pct = round((correct_count / len(test.questions)) * 100, 1) if test.questions else 0.0

    # If score >= 60%, reward officer profile with score upgrade
    upgraded_comps = {}
    if score_pct >= 60:
        boost = 8 if score_pct >= 80 else 4
        for comp_id in affected_competencies:
            cur = officer.current_competencies.get(comp_id, 50)
            new_val = min(98, cur + boost)
            officer.current_competencies[comp_id] = new_val
            upgraded_comps[comp_id] = new_val

    return {
        "test_id": test_id,
        "score_percentage": score_pct,
        "passed": score_pct >= 60,
        "correct_answers": correct_count,
        "total_questions": len(test.questions),
        "feedback": feedback,
        "competency_upgrades": upgraded_comps
    }

class GenerateTestRequest(BaseModel):
    document_source: str
    topic: str
    num_questions: int = 3
    target_role: Optional[str] = None

@app.post("/api/assessment/generate")
def generate_custom_test(req: GenerateTestRequest):
    """Trainer Enablement Tool: Auto-generate MCQs from source documents using RAG"""
    test = RAG_INSTANCE.generate_dynamic_test_from_document(
        doc_name=req.document_source,
        topic=req.topic,
        num_questions=req.num_questions,
        target_role=req.target_role
    )
    return test.model_dump()

@app.post("/api/assessment/upload-doc")
async def upload_document(
    file: UploadFile = File(...),
    topic: str = Form("MoSPI Guideline Document")
):
    """Upload custom PDF or TXT guideline document to expand RAG assessment pool"""
    content = ""
    filename = file.filename or "uploaded_guideline.txt"
    
    if filename.endswith(".pdf"):
        from pypdf import PdfReader
        reader = PdfReader(file.file)
        for page in reader.pages:
            content += page.extract_text() or ""
    else:
        raw_bytes = await file.read()
        content = raw_bytes.decode("utf-8", errors="ignore")

    chunks_added = RAG_INSTANCE.ingest_custom_text(filename, content)
    
    # Auto-generate a test from this new document
    generated_test = RAG_INSTANCE.generate_dynamic_test_from_document(
        doc_name=filename,
        topic=topic,
        num_questions=3
    )

    return {
        "filename": filename,
        "chunks_indexed": chunks_added,
        "generated_test_id": generated_test.test_id,
        "message": f"Successfully ingested {filename} ({chunks_added} chunks) and generated assessment '{generated_test.title}'."
    }

# ----------------- 5. Admin & Macro Workforce Analytics -----------------

@app.get("/api/admin/analytics", response_model=MacroWorkforceReport)
def get_workforce_analytics():
    """Macro workforce analytics, regional heatmaps, and predictive AI capacity projections"""
    return generate_macro_workforce_analytics()

@app.get("/api/health")
def health_check():
    return {
        "status": "HEALTHY",
        "service": "MoSPI iGOT AI Skill Intelligence Platform",
        "timestamp": datetime.datetime.now().isoformat()
    }
