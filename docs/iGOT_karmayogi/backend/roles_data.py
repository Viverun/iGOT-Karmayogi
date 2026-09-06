"""
Standard MoSPI Job Roles & Target Competency Baselines
Each role defines the required target baseline score (0-100) across relevant competencies.
"""

from typing import Dict, List
from pydantic import BaseModel

class RoleDefinition(BaseModel):
    role_id: str
    title: str
    department: str
    grade: str
    description: str
    target_competencies: Dict[str, int] # competency_id -> target score (0-100)
    primary_focus: List[str]

STANDARD_ROLES: Dict[str, RoleDefinition] = {
    "director_nad": RoleDefinition(
        role_id="director_nad",
        title="Director - National Accounts Division (NAD)",
        department="National Accounts Division, MoSPI",
        grade="SAG / Senior Administrative Grade (Level 14)",
        description="Oversees macroeconomic aggregates compilation, GDP/GVA estimation, quarterly national accounts, and inter-sectoral reconciliations under SNA 2008.",
        primary_focus=["stat_national_accounts", "tech_stata", "mgt_public_leadership", "gov_data_privacy"],
        target_competencies={
            "stat_national_accounts": 95,
            "stat_industrial_statistics": 85,
            "stat_agricultural_statistics": 80,
            "stat_price_statistics": 85,
            "stat_metadata_standards": 90,
            "stat_data_quality_frameworks": 90,
            "tech_stata": 85,
            "tech_r": 75,
            "tech_sql": 70,
            "tech_data_visualization": 80,
            "tech_ai_ml": 60,
            "gov_data_privacy": 85,
            "gov_meghraj_cloud": 70,
            "gov_cybersecurity": 75,
            "mgt_public_leadership": 90,
            "mgt_decision_making": 95,
            "mgt_ethics": 95,
            "mgt_project_management": 85,
        }
    ),
    "field_officer_nsso": RoleDefinition(
        role_id="field_officer_nsso",
        title="Field Officer (JSO) - NSSO Field Operations Division",
        department="Field Operations Division (FOD), NSSO",
        grade="Junior Statistical Officer (Level 7)",
        description="Conducts primary socio-economic surveys, PLFS field interviews, CAPI tablet administration, household listing, and multi-stage sampling frame validation.",
        primary_focus=["stat_survey_design", "stat_sampling_techniques", "tech_gis", "gov_digital_signatures"],
        target_competencies={
            "stat_survey_design": 85,
            "stat_sampling_techniques": 85,
            "stat_labour_statistics": 80,
            "stat_data_quality_frameworks": 75,
            "tech_gis": 75,
            "tech_data_visualization": 60,
            "tech_python": 50,
            "tech_sql": 50,
            "gov_digital_signatures": 85,
            "gov_cybersecurity": 75,
            "gov_data_privacy": 80,
            "mgt_ethics": 90,
            "mgt_decision_making": 70,
            "mgt_change_management": 75,
        }
    ),
    "data_analyst_psd": RoleDefinition(
        role_id="data_analyst_psd",
        title="Data Analyst / SSO - Price Statistics Division",
        department="Price Statistics Division (PSD), MoSPI",
        grade="Senior Statistical Officer (Level 8)",
        description="Validates weekly CPI retail and wholesale price quotations across urban/rural markets, detects pricing outliers, and calculates index numbers using Laspeyres formulas.",
        primary_focus=["stat_price_statistics", "tech_python", "tech_r", "tech_ai_ml"],
        target_competencies={
            "stat_price_statistics": 95,
            "stat_sampling_techniques": 80,
            "stat_data_quality_frameworks": 90,
            "stat_metadata_standards": 80,
            "tech_python": 85,
            "tech_r": 80,
            "tech_sql": 85,
            "tech_ai_ml": 75,
            "tech_data_visualization": 80,
            "gov_data_privacy": 80,
            "gov_meghraj_cloud": 65,
            "mgt_project_management": 70,
            "mgt_ethics": 85,
            "mgt_decision_making": 80,
        }
    ),
    "joint_director_sdrd": RoleDefinition(
        role_id="joint_director_sdrd",
        title="Joint Director - Survey Design & Research Division (SDRD)",
        department="Survey Design & Research Division, MoSPI",
        grade="Junior Administrative Grade (Level 12)",
        description="Leads sampling design for nationwide socio-economic rounds, concepts & definitions standardization, survey schedule formulation, and estimation procedures.",
        primary_focus=["stat_survey_design", "stat_sampling_techniques", "stat_sdg_indicators", "tech_r"],
        target_competencies={
            "stat_survey_design": 95,
            "stat_sampling_techniques": 95,
            "stat_sdg_indicators": 90,
            "stat_metadata_standards": 90,
            "stat_data_quality_frameworks": 95,
            "tech_r": 90,
            "tech_stata": 85,
            "tech_python": 75,
            "tech_gis": 70,
            "gov_data_privacy": 85,
            "mgt_public_leadership": 85,
            "mgt_project_management": 90,
            "mgt_decision_making": 90,
            "mgt_ethics": 95,
        }
    ),
    "deputy_director_computer_centre": RoleDefinition(
        role_id="deputy_director_computer_centre",
        title="Deputy Director - Computer Centre (IT & AI Directorate)",
        department="Computer Centre, MoSPI, East Block, R.K. Puram",
        grade="Senior Time Scale (Level 11)",
        description="Manages national statistical cloud infrastructure (MeghRaj), Open Data dissemination portals, API bridges, AI-assisted anomaly detection, and data lakes.",
        primary_focus=["tech_cloud_infrastructure", "tech_ai_ml", "tech_apis", "gov_cybersecurity"],
        target_competencies={
            "tech_cloud_infrastructure": 95,
            "tech_ai_ml": 90,
            "tech_apis": 95,
            "tech_python": 90,
            "tech_sql": 90,
            "tech_open_data": 90,
            "gov_cybersecurity": 95,
            "gov_meghraj_cloud": 95,
            "gov_data_privacy": 90,
            "gov_dpi": 85,
            "stat_metadata_standards": 80,
            "stat_data_quality_frameworks": 80,
            "mgt_project_management": 85,
            "mgt_leadership": 80,
        }
    ),
    "statistical_officer_labour": RoleDefinition(
        role_id="statistical_officer_labour",
        title="Statistical Officer - Labour Bureau & Social Statistics",
        department="Labour Bureau / Social Statistics Division",
        grade="Assistant Director / SSO (Level 8/10)",
        description="Compiles CPI for Industrial Workers (CPI-IW), conducts Annual Survey of Unincorporated Sector Enterprises (ASUSE), and tracks SDG labour benchmarks.",
        primary_focus=["stat_labour_statistics", "stat_price_statistics", "tech_spss", "stat_sdg_indicators"],
        target_competencies={
            "stat_labour_statistics": 90,
            "stat_price_statistics": 85,
            "stat_sdg_indicators": 85,
            "stat_data_quality_frameworks": 80,
            "tech_spss": 85,
            "tech_r": 70,
            "tech_sql": 70,
            "tech_data_visualization": 75,
            "gov_data_privacy": 80,
            "gov_digital_signatures": 80,
            "mgt_ethics": 85,
            "mgt_project_management": 75,
        }
    )
}
