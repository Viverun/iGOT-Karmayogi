"""
Skill Gap Assessment & Explainable Recommendation Engine
Computes Target vs. Actual matrices, vector similarity, and generates prioritized,
explainable learning paths integrated with iGOT Karmayogi & NSSTA TPAC.
"""

from typing import Dict, List, Any
import numpy as np
from pydantic import BaseModel

try:
    from .taxonomy import TAXONOMY, COMPETENCY_PILLARS
    from .roles_data import STANDARD_ROLES, RoleDefinition
    from .officers_data import OfficerProfile
    from .igot_service import IGOT_CATALOG, TPAC_PATHWAYS, IGOTCourse
except (ImportError, ValueError):
    from taxonomy import TAXONOMY, COMPETENCY_PILLARS
    from roles_data import STANDARD_ROLES, RoleDefinition
    from officers_data import OfficerProfile
    from igot_service import IGOT_CATALOG, TPAC_PATHWAYS, IGOTCourse

class GapItem(BaseModel):
    competency_id: str
    competency_name: str
    pillar: str
    pillar_label: str
    target_score: int
    actual_score: int
    gap_score: int
    gap_percentage: float
    is_primary_focus: bool
    urgency_level: str # "Critical", "High", "Moderate", "Satisfied"

class RecommendationItem(BaseModel):
    course_id: str
    title: str
    provider: str
    competency_id: str
    competency_name: str
    duration_hours: int
    level: str
    is_tpac_recommended: bool
    points_award: int
    urgency: str
    rank_score: float
    explanation: str

class GapAnalysisReport(BaseModel):
    officer_id: str
    officer_name: str
    role_id: str
    role_title: str
    overall_readiness_score: float # 0 to 100%
    vector_cosine_similarity: float
    total_gaps_identified: int
    critical_gaps_count: int
    pillar_scores: Dict[str, Dict[str, float]] # pillar -> {target_avg, actual_avg, gap_avg}
    gap_details: List[GapItem]
    radar_data: List[Dict[str, Any]]
    recommendations: List[RecommendationItem]
    relevant_tpac_pathway: Dict[str, Any]

def compute_cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    a = np.array(vec_a, dtype=float)
    b = np.array(vec_b, dtype=float)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))

def analyze_skill_gap(officer: OfficerProfile) -> GapAnalysisReport:
    role = STANDARD_ROLES.get(officer.role_id)
    if not role:
        # Fallback to first role if not found
        role = list(STANDARD_ROLES.values())[0]

    gap_items: List[GapItem] = []
    target_vec = []
    actual_vec = []

    # Map pillars for aggregation
    pillar_accum = {p: {"target": 0, "actual": 0, "count": 0} for p in COMPETENCY_PILLARS.keys()}

    radar_data = []

    for comp_id, comp_def in TAXONOMY.items():
        target = role.target_competencies.get(comp_id, 0)
        actual = officer.current_competencies.get(comp_id, 20) # default baseline
        gap = max(0, target - actual)
        is_primary = comp_id in role.primary_focus

        target_vec.append(float(target))
        actual_vec.append(float(actual))

        # Pillar tracking
        p = comp_def.pillar
        pillar_accum[p]["target"] += target
        pillar_accum[p]["actual"] += min(actual, target) # cap actual at target for readiness
        pillar_accum[p]["count"] += 1

        # Determine urgency
        if gap == 0:
            urgency = "Satisfied"
        elif gap >= 30 or (is_primary and gap >= 20):
            urgency = "Critical"
        elif gap >= 15:
            urgency = "High"
        else:
            urgency = "Moderate"

        gap_pct = round((gap / target * 100) if target > 0 else 0.0, 1)

        if target > 0: # Only report items relevant to this role
            gap_item = GapItem(
                competency_id=comp_id,
                competency_name=comp_def.name,
                pillar=comp_def.pillar,
                pillar_label=COMPETENCY_PILLARS.get(comp_def.pillar, comp_def.pillar),
                target_score=target,
                actual_score=actual,
                gap_score=gap,
                gap_percentage=gap_pct,
                is_primary_focus=is_primary,
                urgency_level=urgency
            )
            gap_items.append(gap_item)

            # Format for radar chart
            radar_data.append({
                "subject": comp_def.name,
                "competency_id": comp_id,
                "actual": actual,
                "target": target,
                "gap": gap,
                "pillar": comp_def.pillar
            })

    # Sort gaps descending by severity and primary focus
    gap_items.sort(key=lambda x: (x.is_primary_focus, x.gap_score), reverse=True)

    # Calculate overall readiness
    total_target = sum(target_vec)
    total_achieved = sum(min(a, t) for a, t in zip(actual_vec, target_vec))
    readiness_score = round((total_achieved / total_target * 100) if total_target > 0 else 100.0, 1)

    cosine_sim = round(compute_cosine_similarity(actual_vec, target_vec), 3)

    # Compute pillar summary
    pillar_summary = {}
    for p, stats in pillar_accum.items():
        t_avg = round(stats["target"] / stats["count"], 1) if stats["count"] > 0 else 0
        a_avg = round(stats["actual"] / stats["count"], 1) if stats["count"] > 0 else 0
        g_avg = round(max(0, t_avg - a_avg), 1)
        pillar_summary[p] = {
            "target_avg": t_avg,
            "actual_avg": a_avg,
            "gap_avg": g_avg
        }

    # Generate explainable recommendations
    recommendations: List[RecommendationItem] = []
    critical_gaps = [g for g in gap_items if g.gap_score > 0]

    for gap in critical_gaps:
        # Match courses from iGOT
        for course in IGOT_CATALOG.values():
            if course.competency_id == gap.competency_id:
                # Calculate composite rank score
                rank = (gap.gap_score * 0.5)
                if gap.is_primary_focus:
                    rank += 25
                if course.is_tpac_recommended:
                    rank += 15
                if gap.urgency_level == "Critical":
                    rank += 10

                # Formulate explainable AI text
                explanation = (
                    f"Recommended with {gap.urgency_level} priority because your designation '{officer.designation}' "
                    f"in {officer.department} mandates a baseline of {gap.target_score} for {gap.competency_name}. "
                    f"A {gap.gap_score}-point deficit was detected against role benchmarks. "
                )
                if course.is_tpac_recommended:
                    explanation += f"This module is officially endorsed by the NSSTA TPAC advisory framework for official statisticians."
                else:
                    explanation += f"Directly upgrades foundational skills required for modern MoSPI survey & analytics operations."

                rec_item = RecommendationItem(
                    course_id=course.course_id,
                    title=course.title,
                    provider=course.provider,
                    competency_id=course.competency_id,
                    competency_name=course.competency_name,
                    duration_hours=course.duration_hours,
                    level=course.level,
                    is_tpac_recommended=course.is_tpac_recommended,
                    points_award=course.points_award,
                    urgency=gap.urgency_level,
                    rank_score=round(rank, 1),
                    explanation=explanation
                )
                recommendations.append(rec_item)

    # Sort recommendations by rank score
    recommendations.sort(key=lambda x: x.rank_score, reverse=True)

    # Find relevant TPAC Pathway
    cadre_type = "ISS" if "ISS" in officer.cadre else "SSS"
    matched_tpac = next((p for p in TPAC_PATHWAYS if p["cadre"] == cadre_type), TPAC_PATHWAYS[0])

    return GapAnalysisReport(
        officer_id=officer.officer_id,
        officer_name=officer.name,
        role_id=role.role_id,
        role_title=role.title,
        overall_readiness_score=readiness_score,
        vector_cosine_similarity=cosine_sim,
        total_gaps_identified=len(critical_gaps),
        critical_gaps_count=len([g for g in critical_gaps if g.urgency_level == "Critical"]),
        pillar_scores=pillar_summary,
        gap_details=gap_items,
        radar_data=radar_data,
        recommendations=recommendations,
        relevant_tpac_pathway=matched_tpac
    )
