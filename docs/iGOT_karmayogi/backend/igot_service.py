"""
iGOT Karmayogi & NSSTA TPAC Interoperability Service
Simulates official iGOT Karmayogi API endpoints, course catalog metadata, and NSSTA TPAC pathways.
Includes simulated OAuth2 token exchange and audit logging for hackathon demonstration.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel
import datetime

class IGOTCourse(BaseModel):
    course_id: str
    title: str
    provider: str # e.g., "NSSTA / MoSPI", "DoPT / iGOT", "C-DAC", "NIC"
    competency_id: str
    competency_name: str
    duration_hours: int
    level: str # "Beginner", "Intermediate", "Advanced"
    is_tpac_recommended: bool
    tpac_cadre: Optional[str] = None # "ISS", "SSS", "Both"
    description: str
    syllabus: List[str]
    points_award: int
    badge_name: str

class APICallLog(BaseModel):
    timestamp: str
    endpoint: str
    method: str
    status_code: int
    request_payload: dict
    response_payload: dict

# Simulated Course Catalog
IGOT_CATALOG: Dict[str, IGOTCourse] = {
    "IGOT_STATA_ADV": IGOTCourse(
        course_id="IGOT_STATA_ADV",
        title="Econometric Modeling & Panel Data Estimation in Stata",
        provider="NSSTA / MoSPI",
        competency_id="tech_stata",
        competency_name="Stata",
        duration_hours=24,
        level="Intermediate",
        is_tpac_recommended=True,
        tpac_cadre="ISS",
        description="Comprehensive training on do-files, panel regression, complex survey weights, and National Accounts macro-reconciliations in Stata.",
        syllabus=["Do-file best practices", "svyset and survey weighting", "Fixed & Random Effects in Panel Data", "Macroeconomic time series modeling"],
        points_award=25,
        badge_name="Stata Certified Macro-Econometrician"
    ),
    "IGOT_GIS_SPATIAL": IGOTCourse(
        course_id="IGOT_GIS_SPATIAL",
        title="Applied QGIS & Spatial Analysis for Field Survey Operations",
        provider="NSSTA / Survey of India",
        competency_id="tech_gis",
        competency_name="GIS & Spatial Analytics",
        duration_hours=30,
        level="Intermediate",
        is_tpac_recommended=True,
        tpac_cadre="Both",
        description="Master geographic information systems for boundary delineation, geo-tagging primary sampling units (PSUs), and satellite crop overlay.",
        syllabus=["QGIS workspace setup", "Vector & Raster layers", "Geo-tagging PSUs in NSSO rounds", "Remote sensing NDVI vegetation indexing"],
        points_award=30,
        badge_name="NSSTA Certified Spatial Analyst"
    ),
    "IGOT_R_SURVEY": IGOTCourse(
        course_id="IGOT_R_SURVEY",
        title="R for Official Statistics: Survey Weighting & Microdata Analysis",
        provider="MoSPI Training Cell / IIT Kanpur",
        competency_id="tech_r",
        competency_name="R Programming",
        duration_hours=36,
        level="Advanced",
        is_tpac_recommended=True,
        tpac_cadre="ISS",
        description="Advanced microdata analysis using tidyverse and the survey package for NSSO 78th/79th round estimation and variance calculations.",
        syllabus=["Tidyverse data pipelines", "The R 'survey' package", "Post-stratification weighting", "Replicate weights (Jackknife & Bootstrap)"],
        points_award=35,
        badge_name="Official Statistics R Specialist"
    ),
    "IGOT_AI_ANOMALY": IGOTCourse(
        course_id="IGOT_AI_ANOMALY",
        title="AI/ML Applications in Price Statistics & Anomaly Detection",
        provider="Computer Centre MoSPI / IIIT Hyderabad",
        competency_id="tech_ai_ml",
        competency_name="AI & Machine Learning",
        duration_hours=20,
        level="Intermediate",
        is_tpac_recommended=True,
        tpac_cadre="Both",
        description="Machine learning workflows for automated outlier detection in weekly retail price quotations and automated item classification.",
        syllabus=["Isolation Forests & DBSCAN for price quotes", "NLP for product description standardization", "Predictive imputation of missing prices", "LLM-driven metadata QA"],
        points_award=25,
        badge_name="AI Statistical Innovator"
    ),
    "IGOT_SNA_CORE": IGOTCourse(
        course_id="IGOT_SNA_CORE",
        title="System of National Accounts (SNA 2008): GVA and Base Revision",
        provider="NSSTA / National Accounts Division",
        competency_id="stat_national_accounts",
        competency_name="National Accounts",
        duration_hours=40,
        level="Advanced",
        is_tpac_recommended=True,
        tpac_cadre="ISS",
        description="In-depth breakdown of institutional sector accounts, supply-use tables (SUT), double deflation methodologies, and financial intermediation (FISIM).",
        syllabus=["SNA 2008 conceptual boundary", "Production account & GVA calculation", "Supply & Use Tables (SUT)", "Financial intermediation indirectly measured (FISIM)"],
        points_award=40,
        badge_name="National Accounts Master Practitioner"
    ),
    "IGOT_PLFS_CAPI": IGOTCourse(
        course_id="IGOT_PLFS_CAPI",
        title="CAPI Tablet Administration & Multi-Stage Sampling in NSSO",
        provider="NSSO FOD / NSSTA",
        competency_id="stat_survey_design",
        competency_name="Survey Design",
        duration_hours=18,
        level="Beginner",
        is_tpac_recommended=True,
        tpac_cadre="SSS",
        description="Field verification protocol, household selection procedures, response non-sampling error reduction, and CAPI synchronization.",
        syllabus=["Sampling frame preparation", "Circular systematic sampling in the field", "CAPI schedule 10.4 navigation", "Data validation checks before sync"],
        points_award=20,
        badge_name="NSSO Field Operations Specialist"
    ),
    "IGOT_DPDP_GOV": IGOTCourse(
        course_id="IGOT_DPDP_GOV",
        title="DPDP Act 2023 & Respondent Confidentiality in Official Statistics",
        provider="Ministry of Electronics and IT / MoSPI Legal",
        competency_id="gov_data_privacy",
        competency_name="Data Privacy & DPDP Act 2023",
        duration_hours=12,
        level="Intermediate",
        is_tpac_recommended=True,
        tpac_cadre="Both",
        description="Legal mandates of the Digital Personal Data Protection Act 2023, consent architectures, anonymization, and Collection of Statistics Act 2008 harmonisation.",
        syllabus=["Key provisions of DPDP Act 2023", "Collection of Statistics Act 2008 alignment", "k-anonymity & l-diversity in microdata release", "Handling respondent RTI exceptions"],
        points_award=15,
        badge_name="Gov Privacy & Ethics Champion"
    ),
    "IGOT_CLOUD_ARCH": IGOTCourse(
        course_id="IGOT_CLOUD_ARCH",
        title="MeghRaj Cloud Architecture & National Microdata Dissemination",
        provider="NIC / Computer Centre MoSPI",
        competency_id="gov_meghraj_cloud",
        competency_name="MeghRaj Cloud & NIC Standards",
        duration_hours=20,
        level="Intermediate",
        is_tpac_recommended=False,
        tpac_cadre="Both",
        description="Deployment and monitoring of statistical databases on MeghRaj (GI Cloud), container security, and high-availability API endpoints.",
        syllabus=["MeghRaj cloud primitives", "Containerizing analytical apps", "Automated backup & disaster recovery", "Microdata portal security auditing"],
        points_award=20,
        badge_name="MeghRaj Cloud Administrator"
    ),
    "IGOT_CPI_INDEX": IGOTCourse(
        course_id="IGOT_CPI_INDEX",
        title="Consumer Price Index (CPI): Laspeyres Formula & Basket Revision",
        provider="Price Statistics Division / NSSTA",
        competency_id="stat_price_statistics",
        competency_name="Price Statistics",
        duration_hours=22,
        level="Intermediate",
        is_tpac_recommended=True,
        tpac_cadre="Both",
        description="Step-by-step compilation of Rural, Urban, and Combined CPI series, price relative calculations, and household expenditure weighting.",
        syllabus=["Laspeyres and Paasche index theory", "Price quotation collection mechanisms", "Geometric mean aggregations", "Base revision and chain indexation"],
        points_award=25,
        badge_name="Price Statistics Specialist"
    ),
    "IGOT_PYTHON_DATA": IGOTCourse(
        course_id="IGOT_PYTHON_DATA",
        title="Python Data Wrangling & Automated Statistical Briefs",
        provider="C-DAC / MoSPI IT Cell",
        competency_id="tech_python",
        competency_name="Python",
        duration_hours=28,
        level="Intermediate",
        is_tpac_recommended=True,
        tpac_cadre="Both",
        description="Automate monthly statistical releases, validate large CSV/Parquet microdata, and create automated PDF briefs using Python and Pandas.",
        syllabus=["Pandas data manipulation", "Handling missing survey entries", "Automated report generation", "Building interactive web charts with Plotly"],
        points_award=30,
        badge_name="Python Automation Specialist"
    )
}

# NSSTA TPAC Pathways definitions
TPAC_PATHWAYS = [
    {
        "pathway_id": "TPAC_ISS_MIDCAREER",
        "title": "NSSTA TPAC Mid-Career Modernization Track (ISS)",
        "target_audience": "Directors & Joint Directors (ISS 5-15 Yrs)",
        "focus_areas": ["Big Data Analytics", "SNA 2008 Revisions", "AI Anomaly Detection", "Cloud Governance"],
        "recommended_courses": ["IGOT_STATA_ADV", "IGOT_SNA_CORE", "IGOT_AI_ANOMALY", "IGOT_DPDP_GOV"],
        "mandatory_credits": 100,
        "cadre": "ISS"
    },
    {
        "pathway_id": "TPAC_SSS_FOUNDATION",
        "title": "NSSTA TPAC Subordinate Statistical Service (SSS) Field Tech Track",
        "target_audience": "Junior & Senior Statistical Officers (SSS)",
        "focus_areas": ["CAPI Operations", "GIS Boundary Delineation", "Price Indexation", "Digital Signatures"],
        "recommended_courses": ["IGOT_PLFS_CAPI", "IGOT_GIS_SPATIAL", "IGOT_CPI_INDEX", "IGOT_PYTHON_DATA"],
        "mandatory_credits": 80,
        "cadre": "SSS"
    }
]

# API call logs to show live integration
AUDIT_LOGS: List[APICallLog] = []

def log_api_call(endpoint: str, method: str, status_code: int, request_payload: dict, response_payload: dict):
    entry = APICallLog(
        timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        endpoint=endpoint,
        method=method,
        status_code=status_code,
        request_payload=request_payload,
        response_payload=response_payload
    )
    AUDIT_LOGS.insert(0, entry)
    if len(AUDIT_LOGS) > 30:
        AUDIT_LOGS.pop()

def fetch_courses_by_competency(competency_id: str) -> List[IGOTCourse]:
    return [c for c in IGOT_CATALOG.values() if c.competency_id == competency_id]
