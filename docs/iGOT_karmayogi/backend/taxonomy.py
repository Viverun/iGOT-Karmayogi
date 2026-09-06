"""
Official MoSPI Competency Taxonomy for Official Statisticians and Staff
Mapped to 4 core pillars: Statistical, Technical, Digital Governance, Behavioural & Managerial.
"""

from typing import Dict, List
from pydantic import BaseModel

class CompetencyItem(BaseModel):
    id: str
    name: str
    pillar: str
    description: str
    keywords: List[str]

COMPETENCY_PILLARS = {
    "statistical": "Statistical Competencies",
    "technical": "Technical Competencies",
    "digital_governance": "Digital Governance",
    "behavioural_managerial": "Behavioural & Managerial"
}

TAXONOMY: Dict[str, CompetencyItem] = {
    # 1. Statistical Competencies
    "stat_survey_design": CompetencyItem(
        id="stat_survey_design",
        name="Survey Design",
        pillar="statistical",
        description="Formulation of survey schedules, sampling frames, response burden mitigation, and multi-stage field strategies.",
        keywords=["survey", "schedule", "questionnaire", "stratification", "sampling frame", "field operations"]
    ),
    "stat_sampling_techniques": CompetencyItem(
        id="stat_sampling_techniques",
        name="Sampling Techniques",
        pillar="statistical",
        description="Probability proportional to size (PPS), systematic random sampling, cluster sampling, design effects, and estimation weights.",
        keywords=["sampling", "pps", "srs", "cluster", "strata", "variance estimation", "design effect"]
    ),
    "stat_national_accounts": CompetencyItem(
        id="stat_national_accounts",
        name="National Accounts",
        pillar="statistical",
        description="SNA 2008 framework, Gross Value Added (GVA), Gross Domestic Product (GDP), Input-Output tables, and capital stock compilation.",
        keywords=["sna", "gdp", "gva", "national accounts", "input output", "constant prices", "nad"]
    ),
    "stat_price_statistics": CompetencyItem(
        id="stat_price_statistics",
        name="Price Statistics",
        pillar="statistical",
        description="Consumer Price Index (CPI), Wholesale Price Index (WPI), Laspeyres formula, geometric mean indexation, and basket revision.",
        keywords=["cpi", "wpi", "inflation", "laspeyres", "index numbers", "price quotation", "psd"]
    ),
    "stat_labour_statistics": CompetencyItem(
        id="stat_labour_statistics",
        name="Labour Statistics",
        pillar="statistical",
        description="Periodic Labour Force Survey (PLFS), Labour Force Participation Rate (LFPR), Worker Population Ratio (WPR), and informal sector metrics.",
        keywords=["plfs", "lfpr", "wpr", "unemployment", "labour bureau", "casual labour", "workforce"]
    ),
    "stat_agricultural_statistics": CompetencyItem(
        id="stat_agricultural_statistics",
        name="Agricultural Statistics",
        pillar="statistical",
        description="Crop area estimation, yield modeling, Agricultural Census, Land Use Statistics (LUS), and GCES methodology.",
        keywords=["agriculture", "crop yield", "land use", "census", "kharif", "rabi", "gces"]
    ),
    "stat_industrial_statistics": CompetencyItem(
        id="stat_industrial_statistics",
        name="Industrial Statistics",
        pillar="statistical",
        description="Index of Industrial Production (IIP), Annual Survey of Industries (ASI), NIC 2008 classification, and factory sector aggregates.",
        keywords=["iip", "asi", "factory sector", "nic classification", "manufacturing", "mining", "electricity"]
    ),
    "stat_sdg_indicators": CompetencyItem(
        id="stat_sdg_indicators",
        name="SDG Indicators",
        pillar="statistical",
        description="National Indicator Framework (NIF) for Sustainable Development Goals, baseline monitoring, metadata schemas, and MoSPI progress reports.",
        keywords=["sdg", "nif", "sustainable development", "agenda 2030", "indicator", "metadata"]
    ),
    "stat_metadata_standards": CompetencyItem(
        id="stat_metadata_standards",
        name="Metadata Standards",
        pillar="statistical",
        description="SDMX (Statistical Data and Metadata eXchange), DDI (Data Documentation Initiative), codebook management, and standard classifications.",
        keywords=["sdmx", "ddi", "metadata", "microdata", "cataloguing", "standard classification"]
    ),
    "stat_data_quality_frameworks": CompetencyItem(
        id="stat_data_quality_frameworks",
        name="Data Quality Frameworks",
        pillar="statistical",
        description="UN National Quality Assurance Frameworks (NQAF), data reconciliation, consistency checks, imputation, and audit trails.",
        keywords=["nqaf", "data quality", "imputation", "outlier detection", "reconciliation", "quality assurance"]
    ),

    # 2. Technical Competencies
    "tech_python": CompetencyItem(
        id="tech_python",
        name="Python",
        pillar="technical",
        description="Pandas, NumPy, SciPy, statistical modeling, data wrangling pipelines, and automated report generation.",
        keywords=["python", "pandas", "numpy", "scipy", "scripting", "automation"]
    ),
    "tech_r": CompetencyItem(
        id="tech_r",
        name="R Programming",
        pillar="technical",
        description="Tidyverse, survey package, weighted microdata analysis, econometric regression, and ggplot2 publication charts.",
        keywords=["r", "tidyverse", "survey package", "econometrics", "ggplot2", "cran"]
    ),
    "tech_sql": CompetencyItem(
        id="tech_sql",
        name="SQL & Database Querying",
        pillar="technical",
        description="Complex relational joins, window functions, analytical aggregation, and query optimization on large demographic datasets.",
        keywords=["sql", "postgresql", "queries", "window functions", "joins", "database"]
    ),
    "tech_stata": CompetencyItem(
        id="tech_stata",
        name="Stata",
        pillar="technical",
        description="Panel data econometrics, complex survey estimation (svyset), time-series analysis, and National Accounts econometric projections.",
        keywords=["stata", "svyset", "panel data", "time series", "do file"]
    ),
    "tech_spss": CompetencyItem(
        id="tech_spss",
        name="SPSS",
        pillar="technical",
        description="Cross-tabulations, hypothesis testing, multivariate analysis, and automated syntax scripting for social statistics.",
        keywords=["spss", "cross tabs", "anova", "chi square", "syntax"]
    ),
    "tech_sas": CompetencyItem(
        id="tech_sas",
        name="SAS",
        pillar="technical",
        description="Enterprise Guide, macro programming, enterprise data warehousing, and regulatory reporting.",
        keywords=["sas", "macro", "proc sql", "enterprise guide", "data step"]
    ),
    "tech_gis": CompetencyItem(
        id="tech_gis",
        name="GIS & Spatial Analytics",
        pillar="technical",
        description="QGIS, ArcGIS, geo-tagging field boundaries, satellite imagery integration for crop estimation, and spatial autocorrelation.",
        keywords=["gis", "qgis", "spatial", "shapefile", "geo-tagging", "remote sensing", "cartography"]
    ),
    "tech_data_visualization": CompetencyItem(
        id="tech_data_visualization",
        name="Data Visualization",
        pillar="technical",
        description="PowerBI, D3.js, interactive dashboards, infographics for parliamentary answers, and statistical charting best practices.",
        keywords=["powerbi", "visualization", "dashboard", "d3", "infographics", "charts"]
    ),
    "tech_ai_ml": CompetencyItem(
        id="tech_ai_ml",
        name="AI & Machine Learning",
        pillar="technical",
        description="Machine learning for automated text classification, anomaly detection in price quotes, predictive modeling, and RAG architectures.",
        keywords=["ai", "machine learning", "rag", "anomaly detection", "predictive modeling", "deep learning"]
    ),
    "tech_cloud_infrastructure": CompetencyItem(
        id="tech_cloud_infrastructure",
        name="Cloud Infrastructure",
        pillar="technical",
        description="MeghRaj (GI Cloud), containerization (Docker), virtual machines, distributed storage, and scalable big data clusters.",
        keywords=["cloud", "meghraj", "docker", "kubernetes", "virtual machine", "aws", "nic cloud"]
    ),
    "tech_apis": CompetencyItem(
        id="tech_apis",
        name="APIs & Integration",
        pillar="technical",
        description="RESTful API design, OpenAPI specifications, automated data exchange pipelines between line ministries and MoSPI.",
        keywords=["api", "rest", "json", "openapi", "integration", "endpoints"]
    ),
    "tech_open_data": CompetencyItem(
        id="tech_open_data",
        name="Open Data Platforms",
        pillar="technical",
        description="data.gov.in management, FAIR data principles, open data licensing, anonymization techniques, and public microdata dissemination.",
        keywords=["open data", "data.gov.in", "fair data", "microdata", "anonymization"]
    ),

    # 3. Digital Governance
    "gov_cybersecurity": CompetencyItem(
        id="gov_cybersecurity",
        name="Cybersecurity & CERT-In Compliance",
        pillar="digital_governance",
        description="Endpoint security, CERT-In compliance protocols, incident reporting, threat modeling, and secure code practices.",
        keywords=["cybersecurity", "cert-in", "security", "threat", "encryption", "vulnerability"]
    ),
    "gov_data_privacy": CompetencyItem(
        id="gov_data_privacy",
        name="Data Privacy & DPDP Act 2023",
        pillar="digital_governance",
        description="Digital Personal Data Protection Act compliance, respondent confidentiality, synthetic data generation, and disclosure control.",
        keywords=["dpdp act", "privacy", "confidentiality", "anonymization", "consent", "gdpr"]
    ),
    "gov_digital_signatures": CompetencyItem(
        id="gov_digital_signatures",
        name="Digital Signatures & e-Office",
        pillar="digital_governance",
        description="DSC integration, e-Sign, PKI infrastructure, official e-Office workflow processing, and document immutability.",
        keywords=["digital signature", "dsc", "e-office", "pki", "e-sign"]
    ),
    "gov_meghraj_cloud": CompetencyItem(
        id="gov_meghraj_cloud",
        name="MeghRaj Cloud & NIC Standards",
        pillar="digital_governance",
        description="Government cloud architecture guidelines, NIC datacenter integration, security auditing, and SLA management.",
        keywords=["meghraj", "nic", "gi cloud", "empanelled csp", "government cloud"]
    ),
    "gov_dpi": CompetencyItem(
        id="gov_dpi",
        name="Digital Public Infrastructure (DPI)",
        pillar="digital_governance",
        description="India Stack integration, Aadhaar authentication standards, DigiLocker integration, and Unified Data Exchange.",
        keywords=["dpi", "india stack", "digilocker", "aadhaar", "upi", "public infrastructure"]
    ),

    # 4. Behavioural & Managerial
    "mgt_public_leadership": CompetencyItem(
        id="mgt_public_leadership",
        name="Public Leadership",
        pillar="behavioural_managerial",
        description="Mission-oriented leadership, institutional stewardship, cross-ministerial alignment, and high-impact policy advisory.",
        keywords=["leadership", "public administration", "stewardship", "governance", "policy"]
    ),
    "mgt_ethics": CompetencyItem(
        id="mgt_ethics",
        name="Ethics & Integrity in Official Statistics",
        pillar="behavioural_managerial",
        description="UN Fundamental Principles of Official Statistics, conflict of interest mitigation, impartiality, and public trust maintenance.",
        keywords=["ethics", "integrity", "impartiality", "un principles", "transparency", "trust"]
    ),
    "mgt_project_management": CompetencyItem(
        id="mgt_project_management",
        name="Project Management & Monitoring",
        pillar="behavioural_managerial",
        description="Agile project delivery, MoSPI milestone tracking, budget allocation, resource scheduling, and Gantt tracking.",
        keywords=["project management", "monitoring", "milestones", "agile", "budgeting", "timeline"]
    ),
    "mgt_decision_making": CompetencyItem(
        id="mgt_decision_making",
        name="Evidence-Based Decision Making",
        pillar="behavioural_managerial",
        description="Synthesizing empirical findings for senior civil service briefings, cabinet notes, and rapid policy interventions.",
        keywords=["decision making", "evidence based", "briefings", "cabinet notes", "analysis"]
    ),
    "mgt_change_management": CompetencyItem(
        id="mgt_change_management",
        name="Change Management & Digital Transition",
        pillar="behavioural_managerial",
        description="Guiding field and ministerial cadres through digital transformation, CAPI adoption, and culture shifts.",
        keywords=["change management", "transformation", "digital adoption", "capi", "stakeholders"]
    )
}

def get_taxonomy_by_pillar() -> Dict[str, List[Dict]]:
    res = {k: [] for k in COMPETENCY_PILLARS.keys()}
    for comp in TAXONOMY.values():
        res[comp.pillar].append(comp.model_dump())
    return res
