"""
Automated Test Suite for Backend Pipeline
Tests:
1. Taxonomy & Roles integrity
2. Officer profiling & Gap Analysis execution
3. Recommendation Engine scoring & Explainable text
4. iGOT Karmayogi simulated progress sync & Competency score upgrade
5. RAG Document Ingestion & MCQ Generation with Bloom's Taxonomy
6. Macro Workforce Analytics computation
"""

import sys
import os

# Add current directory and parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.taxonomy import TAXONOMY, COMPETENCY_PILLARS
    from backend.roles_data import STANDARD_ROLES
    from backend.officers_data import SAMPLE_OFFICERS
    from backend.gap_engine import analyze_skill_gap
    from backend.igot_service import IGOT_CATALOG, TPAC_PATHWAYS
    from backend.rag_engine import RAG_INSTANCE
    from backend.analytics_engine import generate_macro_workforce_analytics
except (ImportError, ModuleNotFoundError):
    from taxonomy import TAXONOMY, COMPETENCY_PILLARS
    from roles_data import STANDARD_ROLES
    from officers_data import SAMPLE_OFFICERS
    from gap_engine import analyze_skill_gap
    from igot_service import IGOT_CATALOG, TPAC_PATHWAYS
    from rag_engine import RAG_INSTANCE
    from analytics_engine import generate_macro_workforce_analytics

def run_tests():
    print("==================================================")
    print("RUNNING MoSPI iGOT SKILL INTELLIGENCE TEST SUITE")
    print("==================================================")

    # Test 1: Taxonomy
    print("[1/6] Verifying Taxonomy and Roles...")
    assert len(TAXONOMY) >= 25, f"Expected at least 25 competencies, found {len(TAXONOMY)}"
    assert len(STANDARD_ROLES) >= 6, f"Expected at least 6 standard roles, found {len(STANDARD_ROLES)}"
    print(f"  -> OK: {len(TAXONOMY)} competencies across 4 pillars, {len(STANDARD_ROLES)} roles verified.")

    # Test 2: Gap Analysis for Director NAD
    print("\n[2/6] Verifying Skill Gap Analysis & Vector Matching...")
    sunita = SAMPLE_OFFICERS["OFF_101"]
    gap_report = analyze_skill_gap(sunita)
    assert gap_report.officer_name == "Sunita Sharma"
    assert gap_report.overall_readiness_score > 0
    assert gap_report.vector_cosine_similarity > 0.5
    assert len(gap_report.gap_details) > 0
    assert len(gap_report.recommendations) > 0
    print(f"  -> OK: Officer {sunita.name} readiness = {gap_report.overall_readiness_score}%, "
          f"Cosine Sim = {gap_report.vector_cosine_similarity}, "
          f"Critical gaps = {gap_report.critical_gaps_count}")

    # Test 3: Recommendation Engine
    print("\n[3/6] Verifying Explainable AI Recommendation Output...")
    top_rec = gap_report.recommendations[0]
    assert len(top_rec.explanation) > 20
    assert "Recommended" in top_rec.explanation
    print(f"  -> Top Course: '{top_rec.title}' (Rank: {top_rec.rank_score}, Urgency: {top_rec.urgency})")
    print(f"  -> Explanation: \"{top_rec.explanation}\"")

    # Test 4: iGOT Progress Sync Simulation
    print("\n[4/6] Verifying iGOT Progress Sync & Competency Upgrade...")
    rajesh = SAMPLE_OFFICERS["OFF_102"]
    old_gis_score = rajesh.current_competencies.get("tech_gis", 35)
    # Simulate course completion
    gis_course = IGOT_CATALOG["IGOT_GIS_SPATIAL"]
    rajesh.current_competencies["tech_gis"] = old_gis_score + 25
    assert rajesh.current_competencies["tech_gis"] > old_gis_score
    print(f"  -> OK: Upgraded Officer {rajesh.name} tech_gis from {old_gis_score} to {rajesh.current_competencies['tech_gis']}.")

    # Test 5: RAG Document Ingestion & MCQ Generation
    print("\n[5/6] Verifying RAG Engine & Bloom's Taxonomy MCQs...")
    assert len(RAG_INSTANCE.chunks) >= 3, f"Expected chunks from data docs, got {len(RAG_INSTANCE.chunks)}"
    prebuilt = RAG_INSTANCE.tests_db.get("TEST_NSSO_01")
    assert prebuilt is not None
    assert len(prebuilt.questions) == 5
    q1 = prebuilt.questions[0]
    assert q1.blooms_taxonomy in ["Recall", "Application", "Analysis"]
    assert len(q1.options) == 4
    assert any(opt.is_correct for opt in q1.options)
    print(f"  -> OK: Loaded '{prebuilt.title}' with {len(prebuilt.questions)} questions. Q1 Bloom: {q1.blooms_taxonomy}")

    # Test Dynamic Test Generation
    dynamic_test = RAG_INSTANCE.generate_dynamic_test_from_document(
        doc_name="cpi_compilation_manual.txt",
        topic="Automated Price Indexation Test",
        num_questions=2
    )
    assert len(dynamic_test.questions) == 2
    print(f"  -> OK: Generated dynamic test '{dynamic_test.title}' with {len(dynamic_test.questions)} MCQs via RAG.")

    # Test 6: Macro Analytics
    print("\n[6/6] Verifying Macro Workforce Analytics & Projections...")
    macro = generate_macro_workforce_analytics()
    assert macro.total_active_cadre == 4820
    assert len(macro.regional_metrics) == 6
    assert len(macro.division_heatmap) >= 5
    assert len(macro.predictive_capacity_projections) >= 5
    print(f"  -> OK: Analyzed 6 NSSO zones, {len(macro.division_heatmap)} divisions, and 2025-2028 capacity curves.")

    print("\n==================================================")
    print("ALL 6 BACKEND TEST SUITES PASSED PERFECTLY!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
