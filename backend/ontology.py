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


def target_profile(department_key: str) -> dict:
    return TARGET_PROFILES.get(department_key, TARGET_PROFILES["general"])


def area_type(area: str) -> str:
    return COMPETENCY_TYPE.get(area, "Functional")


CHAPTER_TITLES = ["Foundations", "Core Concepts & Methods", "Applied Practice & Review"]
