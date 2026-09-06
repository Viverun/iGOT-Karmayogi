"""FRAC-flavoured competency ontology for the platform.

Every competency AREA the system scores, grouped by FRAC competency type, plus
role/department target proficiency profiles (0-100). The gap engine compares a
user's current vector against their department target to produce gap scores.
"""

# area -> FRAC competency type
COMPETENCY_TYPE = {
    # Domain
    "Sampling Techniques": "Domain",
    "Survey Design": "Domain",
    "Statistical Methods": "Domain",
    "National Accounts": "Domain",
    "Price Statistics": "Domain",
    "Labour Statistics": "Domain",
    "Agricultural Statistics": "Domain",
    "Industrial Statistics": "Domain",
    "SDG Indicators": "Domain",
    "Metadata Standards": "Domain",
    "Data Quality Frameworks": "Domain",
    "Remote Sensing Fundamentals": "Domain",
    "Satellite Data Processing": "Domain",
    "Legal and Regulatory Knowledge": "Domain",
    "Disaster Management": "Domain",
    "National Priorities": "Domain",
    # Functional / Technical
    "Python": "Functional",
    "SQL": "Functional",
    "Data Interpretation": "Functional",
    "Data Analysis": "Functional",
    "GIS": "Functional",
    "AI and Emerging Tech": "Functional",
    "Digital Governance": "Functional",
    "Cybersecurity and Data Protection": "Functional",
    "Policy Formulation": "Functional",
    "Data Visualization": "Functional",
    "Cloud Computing": "Functional",
    # Behavioural / Managerial
    "Communication": "Behavioural",
    "Ethics and Values": "Behavioural",
    "Decision Making": "Behavioural",
    "Problem Solving": "Behavioural",
    "Citizen Centricity": "Behavioural",
    "Leadership": "Behavioural",
    "Project Management": "Behavioural",
}

# department_key -> {area: target proficiency 0-100}
# Modelled on role expectations for a mid-junior technical officer (Analyst/US level).
TARGET_PROFILES = {
    "space": {
        "Remote Sensing Fundamentals": 75,
        "Satellite Data Processing": 75,
        "GIS": 70,
        "Data Interpretation": 70,
        "Python": 65,
        "Digital Governance": 60,
        "Cybersecurity and Data Protection": 60,
        "Communication": 60,
        "Problem Solving": 65,
        "Data Visualization": 55,
        "AI and Emerging Tech": 55,
        "Decision Making": 55,
    },
    "statistics": {
        "Sampling Techniques": 75,
        "Survey Design": 75,
        "Statistical Methods": 75,
        "Data Interpretation": 70,
        "Python": 65,
        "SQL": 60,
        "Digital Governance": 60,
        "Cybersecurity and Data Protection": 60,
        "Communication": 60,
        "Ethics and Values": 65,
        "Data Visualization": 55,
        "Policy Formulation": 60,
    },
    "general": {
        "National Priorities": 60,
        "Digital Governance": 60,
        "AI and Emerging Tech": 55,
        "Citizen Centricity": 60,
        "Decision Making": 60,
        "Policy Formulation": 60,
        "Communication": 60,
        "Ethics and Values": 60,
    },
}

DEFAULT_TARGET = 60  # for areas a user has scores in but the target profile omits

# Standard MoSPI job roles with role-level target baselines (0-100 per area).
# A role profile, when assigned to a user, overrides the department-level
# target profile — mirrors FRAC's role -> competency mapping.
ROLE_PROFILES = {
    "field_officer_nsso": {
        "title": "Field Officer (JSO) — NSSO Field Operations Division",
        "department": "Field Operations Division (FOD), NSSO",
        "grade": "Junior Statistical Officer (Level 7)",
        "targets": {
            "Survey Design": 85, "Sampling Techniques": 85, "Labour Statistics": 80,
            "Data Quality Frameworks": 75, "GIS": 75, "Data Visualization": 60,
            "Python": 50, "SQL": 50, "Cybersecurity and Data Protection": 75,
            "Ethics and Values": 90, "Decision Making": 70, "Communication": 70,
        },
    },
    "sso_price_statistics": {
        "title": "Senior Statistical Officer — Price Statistics Division",
        "department": "Price Statistics Division (PSD), MoSPI",
        "grade": "Senior Statistical Officer (Level 8-10)",
        "targets": {
            "Price Statistics": 90, "Statistical Methods": 80, "Survey Design": 70,
            "Data Quality Frameworks": 80, "Python": 65, "SQL": 70,
            "Data Visualization": 70, "AI and Emerging Tech": 60,
            "Metadata Standards": 70, "Ethics and Values": 85, "Decision Making": 80,
        },
    },
    "director_nad": {
        "title": "Director — National Accounts Division",
        "department": "National Accounts Division (NAD), MoSPI",
        "grade": "SAG (Level 14)",
        "targets": {
            "National Accounts": 95, "Industrial Statistics": 85,
            "Agricultural Statistics": 80, "Price Statistics": 85,
            "Metadata Standards": 90, "Data Quality Frameworks": 90,
            "SQL": 70, "Data Visualization": 80, "AI and Emerging Tech": 60,
            "Cybersecurity and Data Protection": 75, "Leadership": 90,
            "Decision Making": 95, "Ethics and Values": 95, "Project Management": 85,
        },
    },
    "jd_sdrd": {
        "title": "Joint Director — Survey Design & Research Division",
        "department": "Survey Design & Research Division (SDRD), NSSO",
        "grade": "JD (Level 11-12)",
        "targets": {
            "Survey Design": 90, "Sampling Techniques": 90, "Statistical Methods": 80,
            "Labour Statistics": 70, "Data Quality Frameworks": 85,
            "Python": 70, "SQL": 65, "Metadata Standards": 75,
            "Decision Making": 85, "Project Management": 80, "Communication": 80,
        },
    },
    "dd_computer_centre": {
        "title": "Deputy Director — Computer Centre (IT & AI Directorate)",
        "department": "Computer Centre, MoSPI",
        "grade": "Deputy Director (Level 11-12)",
        "targets": {
            "Python": 90, "SQL": 85, "AI and Emerging Tech": 85,
            "Cloud Computing": 80, "Cybersecurity and Data Protection": 85,
            "Data Visualization": 75, "Metadata Standards": 70,
            "Statistical Methods": 65, "Decision Making": 80, "Project Management": 85,
        },
    },
    "so_labour_bureau": {
        "title": "Statistical Officer — Labour Bureau & Social Statistics",
        "department": "Labour Bureau, Shimla/Chandigarh",
        "grade": "Statistical Officer (Level 7-8)",
        "targets": {
            "Labour Statistics": 90, "Survey Design": 75, "Sampling Techniques": 75,
            "Statistical Methods": 75, "SDG Indicators": 70, "SQL": 65,
            "Data Visualization": 70, "Ethics and Values": 80, "Communication": 75,
        },
    },
}

# designation/department keywords -> role_id (checked in order)
_ROLE_KEYWORDS = [
    ("computer centre", "dd_computer_centre"),
    ("national accounts", "director_nad"),
    ("survey design", "jd_sdrd"),
    ("price", "sso_price_statistics"),
    ("labour", "so_labour_bureau"),
    ("field operations", "field_officer_nsso"),
    ("jso", "field_officer_nsso"),
    ("field officer", "field_officer_nsso"),
    ("analyst", "sso_price_statistics"),
]


def role_profile(role_id: str) -> dict | None:
    return ROLE_PROFILES.get(role_id)


def resolve_role_id(designation: str = "", department: str = "") -> str | None:
    """Best-effort mapping of a user's designation/department to a standard MoSPI role."""
    hay = f"{designation} {department}".lower()
    if "space" in hay or "isro" in hay or "adrin" in hay:
        return None  # space profiles keep the department-level target
    for kw, role_id in _ROLE_KEYWORDS:
        if kw in hay:
            return role_id
    return None


def target_profile(department_key: str, role_id: str | None = None) -> dict:
    if role_id and role_id in ROLE_PROFILES:
        return ROLE_PROFILES[role_id]["targets"]
    return TARGET_PROFILES.get(department_key, TARGET_PROFILES["general"])


def area_type(area: str) -> str:
    return COMPETENCY_TYPE.get(area, "Functional")


CHAPTER_TITLES = ["Foundations", "Core Concepts & Methods", "Applied Practice & Review"]
