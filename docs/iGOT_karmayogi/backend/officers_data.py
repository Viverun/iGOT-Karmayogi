"""
Realistic MoSPI Officer Profiles and Workforce Pool
Includes diverse officers across Indian Statistical Service (ISS) and Subordinate Statistical Service (SSS).
"""

from typing import Dict, List, Optional
from pydantic import BaseModel

class TrainingLog(BaseModel):
    course_id: str
    course_title: str
    source: str # "iGOT Karmayogi" | "NSSTA Residential" | "UNSD e-Learning"
    completion_date: str
    hours_spent: int
    score_achieved: int

class OfficerProfile(BaseModel):
    officer_id: str
    name: str
    designation: str
    role_id: str
    department: str
    cadre: str # "ISS (Indian Statistical Service)" | "SSS (Subordinate Statistical Service)"
    zone: str # "North", "South", "East", "West", "Central", "North-East"
    office_location: str
    education: str
    years_experience: int
    avatar_initials: str
    training_history: List[TrainingLog]
    current_competencies: Dict[str, int] # competency_id -> actual score (0-100)
    self_assessments: Dict[str, int]

SAMPLE_OFFICERS: Dict[str, OfficerProfile] = {
    "OFF_101": OfficerProfile(
        officer_id="OFF_101",
        name="Sunita Sharma",
        designation="Director",
        role_id="director_nad",
        department="National Accounts Division, New Delhi",
        cadre="ISS (Indian Statistical Service) - 2008 Batch",
        zone="North",
        office_location="Khurshid Lal Bhawan, Janpath, New Delhi",
        education="M.Stat (Indian Statistical Institute, Kolkata), M.Phil Economics",
        years_experience=16,
        avatar_initials="SS",
        training_history=[
            TrainingLog(
                course_id="IGOT_SNA_2008",
                course_title="System of National Accounts (SNA 2008) Advanced Compilation",
                source="iGOT Karmayogi",
                completion_date="2025-11-14",
                hours_spent=28,
                score_achieved=92
            ),
            TrainingLog(
                course_id="NSSTA_MACRO_01",
                course_title="NSSTA Residential Workshop on GVA Base Revision",
                source="NSSTA Residential",
                completion_date="2025-06-20",
                hours_spent=40,
                score_achieved=88
            )
        ],
        current_competencies={
            "stat_national_accounts": 90,
            "stat_industrial_statistics": 82,
            "stat_agricultural_statistics": 75,
            "stat_price_statistics": 80,
            "stat_metadata_standards": 85,
            "stat_data_quality_frameworks": 85,
            "tech_stata": 50, # Gap: target is 85 (gap = 35)
            "tech_r": 45,     # Gap: target is 75 (gap = 30)
            "tech_sql": 40,
            "tech_data_visualization": 70,
            "tech_ai_ml": 30, # Gap: target is 60 (gap = 30)
            "gov_data_privacy": 80,
            "gov_meghraj_cloud": 50,
            "gov_cybersecurity": 65,
            "mgt_public_leadership": 88,
            "mgt_decision_making": 92,
            "mgt_ethics": 94,
            "mgt_project_management": 82,
        },
        self_assessments={
            "stat_national_accounts": 90,
            "tech_stata": 55,
            "tech_ai_ml": 35,
            "gov_data_privacy": 80
        }
    ),
    "OFF_102": OfficerProfile(
        officer_id="OFF_102",
        name="Rajesh Kumar Verma",
        designation="Junior Statistical Officer",
        role_id="field_officer_nsso",
        department="NSSO Field Operations Division (FOD)",
        cadre="SSS (Subordinate Statistical Service)",
        zone="Central",
        office_location="Regional Office Bhopal, Madhya Pradesh",
        education="B.Sc Statistics & Mathematics (Barkatullah University)",
        years_experience=4,
        avatar_initials="RV",
        training_history=[
            TrainingLog(
                course_id="IGOT_PLFS_01",
                course_title="Periodic Labour Force Survey (PLFS) CAPI Administration",
                source="iGOT Karmayogi",
                completion_date="2025-09-02",
                hours_spent=16,
                score_achieved=85
            )
        ],
        current_competencies={
            "stat_survey_design": 65, # Target 85 (gap 20)
            "stat_sampling_techniques": 60, # Target 85 (gap 25)
            "stat_labour_statistics": 75,
            "stat_data_quality_frameworks": 55, # Target 75 (gap 20)
            "tech_gis": 35, # Target 75 (gap 40) - high gap
            "tech_data_visualization": 40,
            "tech_python": 25,
            "tech_sql": 20,
            "gov_digital_signatures": 80,
            "gov_cybersecurity": 60,
            "gov_data_privacy": 65,
            "mgt_ethics": 85,
            "mgt_decision_making": 60,
            "mgt_change_management": 55,
        },
        self_assessments={
            "stat_sampling_techniques": 65,
            "tech_gis": 40,
            "gov_digital_signatures": 85
        }
    ),
    "OFF_103": OfficerProfile(
        officer_id="OFF_103",
        name="Priya Ananthakrishnan",
        designation="Senior Statistical Officer",
        role_id="data_analyst_psd",
        department="Price Statistics Division, MoSPI",
        cadre="SSS (Subordinate Statistical Service)",
        zone="South",
        office_location="Regional Office Chennai, Tamil Nadu",
        education="M.Sc Applied Statistics (Madras Christian College)",
        years_experience=7,
        avatar_initials="PA",
        training_history=[
            TrainingLog(
                course_id="IGOT_PY_01",
                course_title="Python for Data Analysis and Outlier Detection",
                source="iGOT Karmayogi",
                completion_date="2026-01-10",
                hours_spent=24,
                score_achieved=88
            ),
            TrainingLog(
                course_id="NSSTA_CPI_02",
                course_title="NSSTA Advanced Price Index Methodology",
                source="NSSTA Residential",
                completion_date="2025-08-15",
                hours_spent=35,
                score_achieved=94
            )
        ],
        current_competencies={
            "stat_price_statistics": 92,
            "stat_sampling_techniques": 75,
            "stat_data_quality_frameworks": 85,
            "stat_metadata_standards": 70,
            "tech_python": 80,
            "tech_r": 50, # Target 80 (gap 30)
            "tech_sql": 70,
            "tech_ai_ml": 45, # Target 75 (gap 30)
            "tech_data_visualization": 75,
            "gov_data_privacy": 75,
            "gov_meghraj_cloud": 45, # Target 65 (gap 20)
            "mgt_project_management": 65,
            "mgt_ethics": 85,
            "mgt_decision_making": 75,
        },
        self_assessments={
            "stat_price_statistics": 95,
            "tech_python": 85,
            "tech_ai_ml": 50
        }
    ),
    "OFF_104": OfficerProfile(
        officer_id="OFF_104",
        name="Dr. Arindam Mukherjee",
        designation="Joint Director",
        role_id="joint_director_sdrd",
        department="Survey Design & Research Division (SDRD)",
        cadre="ISS (Indian Statistical Service) - 2012 Batch",
        zone="East",
        office_location="Mahalanobis Bhavan, Kolkata, West Bengal",
        education="Ph.D Statistics (University of Calcutta)",
        years_experience=13,
        avatar_initials="AM",
        training_history=[
            TrainingLog(
                course_id="NSSTA_SURV_01",
                course_title="Multi-stage Complex Survey Estimation Masterclass",
                source="NSSTA Residential",
                completion_date="2025-04-12",
                hours_spent=42,
                score_achieved=96
            )
        ],
        current_competencies={
            "stat_survey_design": 92,
            "stat_sampling_techniques": 94,
            "stat_sdg_indicators": 85,
            "stat_metadata_standards": 88,
            "stat_data_quality_frameworks": 90,
            "tech_r": 85,
            "tech_stata": 82,
            "tech_python": 55, # Target 75 (gap 20)
            "tech_gis": 45,    # Target 70 (gap 25)
            "gov_data_privacy": 80,
            "mgt_public_leadership": 82,
            "mgt_project_management": 86,
            "mgt_decision_making": 88,
            "mgt_ethics": 92,
        },
        self_assessments={
            "stat_survey_design": 95,
            "stat_sampling_techniques": 95,
            "tech_gis": 50
        }
    ),
    "OFF_105": OfficerProfile(
        officer_id="OFF_105",
        name="Vikramaditya Rao",
        designation="Deputy Director",
        role_id="deputy_director_computer_centre",
        department="Computer Centre, MoSPI",
        cadre="ISS (Indian Statistical Service) - 2016 Batch",
        zone="North",
        office_location="East Block 10, R.K. Puram, New Delhi",
        education="B.Tech Computer Science + M.Sc Statistics (IIT Kanpur)",
        years_experience=9,
        avatar_initials="VR",
        training_history=[
            TrainingLog(
                course_id="IGOT_CLOUD_01",
                course_title="MeghRaj Architecture & Secure API Engineering",
                source="iGOT Karmayogi",
                completion_date="2025-10-18",
                hours_spent=32,
                score_achieved=95
            )
        ],
        current_competencies={
            "tech_cloud_infrastructure": 90,
            "tech_ai_ml": 82,
            "tech_apis": 92,
            "tech_python": 88,
            "tech_sql": 88,
            "tech_open_data": 85,
            "gov_cybersecurity": 90,
            "gov_meghraj_cloud": 90,
            "gov_data_privacy": 85,
            "gov_dpi": 80,
            "stat_metadata_standards": 70, # Target 80 (gap 10)
            "stat_data_quality_frameworks": 75,
            "mgt_project_management": 82,
            "mgt_leadership": 78,
        },
        self_assessments={
            "tech_ai_ml": 85,
            "tech_apis": 95,
            "gov_cybersecurity": 92
        }
    )
}
