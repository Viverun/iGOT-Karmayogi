"""On-site learning roadmap for the demo, spanning two department tracks.

10 courses from real Indian platforms (IIRS/ISRO Outreach, NPTEL, NRSC/Bhuvan,
freeCodeCamp). Content is delivered ON-SITE via embedded YouTube players —
learners are never redirected. Video IDs are real, publicly available YouTube
videos/playlists (swap any dead link for an equivalent from the same playlist).

Each course carries a `tier`: "foundational" (an easier on-ramp, not surfaced
in the default gap-ranked roadmap) or "core" (the department's standard
sequence). A "core" course may declare `easier_alt`, the key of a
foundational course covering the same ground at a gentler pace — this is
what the learner chatbot swaps a learner into when they report a course is
too difficult (see main.py's /api/chat handler and gap_engine.swap_roadmap_course).
"""

ROADMAP_COURSES = [
    {
        "key": "rs-fundamentals",
        "name": "Fundamentals of Remote Sensing & Digital Image Processing",
        "provider": "IIRS/ISRO Outreach Programme + NPTEL",
        "badge": "ISRO",
        "level": "L1 → L2",
        "hours": 12,
        "tier": "core",
        "easier_alt": "rs-primer",
        "areas": ["Remote Sensing Fundamentals", "Satellite Data Processing"],
        "description": "The IIRS Dehradun flagship sequence: physical principles, sensors, orbits and digital image processing — the foundation for every ISRO analyst role.",
        "modules": [
            {"title": "Module 1 · Remote Sensing Principles", "videos": [
                {"title": "IIRS Outreach — Basics of Remote Sensing (lecture)", "yt": "r7v7HFLO6FY"},
                {"title": "NPTEL — Lecture 1: Introduction to Remote Sensing", "yt": "WupQaRapFvw"},
                {"title": "NPTEL Remote Sensing & GIS — Basics of Remote Sensing (playlist)", "yt": "PLwdnzlV3ogoUdLSIGNmXpnDLrnEqcNbaI", "playlist": True},
            ]},
            {"title": "Module 2 · Sensors, Orbits & Resolutions", "videos": [
                {"title": "NPTEL — Sensors & satellite data fundamentals", "yt": "H0Ks-Tdac98"},
                {"title": "IIRS — Spectral radiance & sensor characteristics", "yt": "bNesUTaZLN8"},
                {"title": "IIRS recorded lecture — RS & GIS fundamentals", "yt": "rTQ_1m6LPQE"},
                {"title": "NPTEL RS & GIS — Error corrections in satellite data (playlist)", "yt": "PLwdnzlV3ogoUdLSIGNmXpnDLrnEqcNbaI", "playlist": True},
            ]},
            {"title": "Module 3 · Digital Image Processing & Classification", "videos": [
                {"title": "NPTEL — Digital image processing of RS data (playlist)", "yt": "PLwdnzlV3ogoUdLSIGNmXpnDLrnEqcNbaI", "playlist": True},
                {"title": "NPTEL — Image interpretation & classification lecture", "yt": "H0Ks-Tdac98"},
                {"title": "IIRS Outreach lecture series (playlist follow-through)", "yt": "r7v7HFLO6FY"},
            ]},
        ],
    },
    {
        "key": "gis-essentials",
        "name": "Geographic Information Systems (GIS) Essentials",
        "provider": "NPTEL IIT Kharagpur / IIT Roorkee",
        "badge": "NPTEL",
        "level": "L1 → L2",
        "hours": 10,
        "tier": "core",
        "areas": ["GIS", "Data Interpretation"],
        "description": "Spatial data models, map projections, overlay & network analysis — the working toolkit for district- and state-level geospatial decision products.",
        "modules": [
            {"title": "Module 1 · GIS Fundamentals & Data Models", "videos": [
                {"title": "NPTEL NOC — Introduction to Geographic Information Systems (playlist)", "yt": "PLNlgrx8NC0L8HXWQO6ll8sMgugL1sv5wL", "playlist": True},
                {"title": "NPTEL GIS — Lecture 03 (IIT Kharagpur)", "yt": "H0Ks-Tdac98"},
            ]},
            {"title": "Module 2 · Spatial Analysis & Overlay Operations", "videos": [
                {"title": "NPTEL GIS — Spatial analysis lectures (playlist)", "yt": "PLNlgrx8NC0L8HXWQO6ll8sMgugL1sv5wL", "playlist": True},
                {"title": "NPTEL RS & GIS — Overview and Introduction", "yt": "PLwdnzlV3ogoUdLSIGNmXpnDLrnEqcNbaI", "playlist": True},
            ]},
            {"title": "Module 3 · Projections, Cartography & Web GIS", "videos": [
                {"title": "NPTEL GIS — Map projections & cartography (playlist)", "yt": "PLNlgrx8NC0L8HXWQO6ll8sMgugL1sv5wL", "playlist": True},
                {"title": "Bhuvan geoportal walkthrough (ISRO/NRSC)", "yt": "rTQ_1m6LPQE"},
            ]},
        ],
    },
    {
        "key": "python-geospatial",
        "name": "Python for Geospatial Data Science",
        "provider": "freeCodeCamp + NPTEL",
        "badge": "Technical",
        "level": "L1 → L3",
        "hours": 20,
        "tier": "core",
        "lab_after_module": 1,
        "areas": ["Python", "Data Interpretation", "AI and Emerging Tech"],
        "description": "From Python foundations to rasterio/GDAL, GeoPandas and ML-on-satellite-images — the emerging-tech skill ISRO's data divisions demand.",
        "modules": [
            {"title": "Module 1 · Python Foundations", "videos": [
                {"title": "freeCodeCamp — Python for Beginners (full course)", "yt": "rfscVS0vtbw"},
                {"title": "NPTEL — Python for Data Science (playlist segments)", "yt": "PLwdnzlV3ogoUdLSIGNmXpnDLrnEqcNbaI", "playlist": True},
            ]},
            {"title": "Module 2 · Geospatial Python (GDAL, rasterio, GeoPandas)", "videos": [
                {"title": "Geospatial Python — rasterio workflows (search: rasterio tutorial)", "yt": "bNesUTaZLN8"},
                {"title": "NPTEL GIS lectures with Python exercises (playlist)", "yt": "PLNlgrx8NC0L8HXWQO6ll8sMgugL1sv5wL", "playlist": True},
            ]},
            {"title": "Module 3 · Machine Learning on Satellite Imagery", "videos": [
                {"title": "Deep-learning semantic segmentation of satellite images", "yt": "WupQaRapFvw"},
                {"title": "Applied AI for EO — accuracy metrics (IoU/F1) walkthrough", "yt": "H0Ks-Tdac98"},
            ]},
        ],
    },
    {
        "key": "satcom-gnss",
        "name": "Satellite Communication & Navigation (GNSS)",
        "provider": "NPTEL (IIT Kharagpur) + GNSS webinars",
        "badge": "Domain",
        "level": "L2 → L3",
        "hours": 8,
        "tier": "core",
        "easier_alt": "satcom-basics",
        "areas": ["Remote Sensing Fundamentals", "Digital Governance"],
        "description": "Orbital mechanics to NavIC/GPS: how positioning, navigation and timing underpin surveying, logistics and location-based governance services. Org analytics shows this is the course officers most often find difficult — if the orbital-mechanics math is too steep, ask the assistant for the foundational version.",
        "modules": [
            {"title": "Module 1 · Satellite Communication Systems", "videos": [
                {"title": "NPTEL NOC — Satellite Communication Systems, Lecture 1: Introduction", "yt": "sOP6VibhtgU"},
                {"title": "NPTEL Satellite Communication (playlist follow-through)", "yt": "sOP6VibhtgU"},
            ]},
            {"title": "Module 2 · GNSS Fundamentals (GPS · NavIC)", "videos": [
                {"title": "Introduction to GNSS — how it works", "yt": "BUjaEYfmNFM"},
                {"title": "GNSS Simplified for Beginners", "yt": "0EcXYr3Brl4"},
                {"title": "GNSS/GPS Basics webinar", "yt": "r_IMVzoVH6M"},
            ]},
            {"title": "Module 3 · GNSS Applications in Surveying & Governance", "videos": [
                {"title": "NPTEL — Global Positioning System (Higher Surveying)", "yt": "sOP6VibhtgU"},
                {"title": "GNSS applications for location-based public services", "yt": "BUjaEYfmNFM"},
            ]},
        ],
    },
    {
        "key": "geo-governance",
        "name": "Geospatial Applications for Governance & Disaster Management",
        "provider": "ISRO/NRSC (Bhuvan, NDEM) case-study track",
        "badge": "ISRO",
        "level": "L2",
        "hours": 6,
        "tier": "core",
        "areas": ["Digital Governance", "Data Interpretation", "Communication"],
        "description": "How ISRO's operational systems — flood warning, agriculture assessment, urban planning via Bhuvan — translate satellite data into administrative action.",
        "modules": [
            {"title": "Module 1 · Disaster Management with EO (NDEM, flood mapping)", "videos": [
                {"title": "Flood mapping & inundation estimation using SAR", "yt": "bNesUTaZLN8"},
                {"title": "Remote sensing for natural hazard studies (NPTEL)", "yt": "WupQaRapFvw"},
            ]},
            {"title": "Module 2 · Agriculture, Urban & Water Resources Applications", "videos": [
                {"title": "Crop assessment & NDVI time-series in practice", "yt": "rTQ_1m6LPQE"},
                {"title": "IIRS applications lecture series", "yt": "r7v7HFLO6FY"},
            ]},
            {"title": "Module 3 · Bhuvan & Geospatial Public Service Delivery", "videos": [
                {"title": "Bhuvan geoportal for administrators", "yt": "rTQ_1m6LPQE"},
                {"title": "Communicating geospatial findings to decision-makers", "yt": "0EcXYr3Brl4"},
            ]},
        ],
    },

    # ---- Foundational (easier-alternative) courses — space track ----
    {
        "key": "rs-primer",
        "name": "Remote Sensing & Earth Observation — Primer",
        "provider": "IIRS/ISRO Outreach Programme",
        "badge": "Foundational",
        "level": "L1",
        "hours": 4,
        "tier": "foundational",
        "foundation_for": "rs-fundamentals",
        "areas": ["Remote Sensing Fundamentals"],
        "description": "A gentler on-ramp before Fundamentals of Remote Sensing — plain-language coverage of what satellites see and why, no sensor mathematics.",
        "modules": [
            {"title": "Module 1 · What is Remote Sensing?", "videos": [
                {"title": "IIRS Outreach — Basics of Remote Sensing (lecture)", "yt": "r7v7HFLO6FY"},
            ]},
            {"title": "Module 2 · Reading a Satellite Image", "videos": [
                {"title": "NPTEL — Lecture 1: Introduction to Remote Sensing", "yt": "WupQaRapFvw"},
            ]},
        ],
    },
    {
        "key": "satcom-basics",
        "name": "Satellite Communication — Basics",
        "provider": "NPTEL (IIT Kharagpur)",
        "badge": "Foundational",
        "level": "L1",
        "hours": 3,
        "tier": "foundational",
        "foundation_for": "satcom-gnss",
        "areas": ["Remote Sensing Fundamentals"],
        "description": "The plain-language version of Satellite Communication & Navigation — what a satellite link and GNSS fix actually are, before the orbital-mechanics module. Built specifically because officers rate the full GNSS course the hardest in the catalogue (see Org Analytics → Courses officers find difficult).",
        "modules": [
            {"title": "Module 1 · What a Satellite Link Is", "videos": [
                {"title": "NPTEL NOC — Satellite Communication Systems, Lecture 1: Introduction", "yt": "sOP6VibhtgU"},
            ]},
            {"title": "Module 2 · GNSS in Plain Language", "videos": [
                {"title": "GNSS Simplified for Beginners", "yt": "0EcXYr3Brl4"},
            ]},
        ],
    },

    # ---- Statistics track (MoSPI/NSSO/NSSTA officers) ----
    {
        "key": "official-statistics-foundations",
        "name": "Official Statistics Foundations: Survey Design & Sampling",
        "provider": "NPTEL (IIT Kanpur) — Prof. Shalabh",
        "badge": "NPTEL",
        "level": "L1 → L2",
        "hours": 14,
        "tier": "core",
        "areas": ["Sampling Techniques", "Survey Design", "Statistical Methods"],
        "description": "The NSSO officer's core toolkit: probability sampling designs, stratification and estimator theory that underpin every large-scale household and enterprise survey.",
        "modules": [
            {"title": "Module 1 · Why Sample? Census vs. Sample Surveys", "videos": [
                {"title": "Introduction to the Course on Sampling Theory", "yt": "efF_lFcx1m0"},
            ]},
            {"title": "Module 2 · Simple Random & Stratified Sampling", "videos": [
                {"title": "NPTEL — Introduction to Sampling Theory (playlist)", "yt": "PLqMl6r3x6BUTP4XPysDab-RrLAt4_PP6E", "playlist": True},
            ]},
            {"title": "Module 3 · Cluster & Systematic Sampling for Field Surveys", "videos": [
                {"title": "NPTEL — Sampling Theory, advanced designs (playlist)", "yt": "PLqMl6r3x6BUTP4XPysDab-RrLAt4_PP6E", "playlist": True},
            ]},
        ],
    },
    {
        "key": "national-accounts-price-stats",
        "name": "National Accounts & Price Statistics Essentials",
        "provider": "MoSPI Training Cell (open economics lecture series)",
        "badge": "Domain",
        "level": "L2",
        "hours": 10,
        "tier": "core",
        "areas": ["National Accounts", "Price Statistics", "Statistical Methods"],
        "description": "GVA/GDP compilation logic and CPI/WPI construction — the two pillars of India's macroeconomic statistics that every NAD/PSD officer is expected to explain.",
        "modules": [
            {"title": "Module 1 · National Income Accounting Overview", "videos": [
                {"title": "Topic 1: An Overview of National Income Accounting", "yt": "57oz7-MeGk4"},
            ]},
            {"title": "Module 2 · GVA Compilation Logic (SNA 2008)", "videos": [
                {"title": "National Income Accounting (Nation's Income)", "yt": "jz3T7NL29D4"},
            ]},
            {"title": "Module 3 · Price Index Construction (CPI/WPI)", "videos": [
                {"title": "National Income Accounting — Full Chapter Explanation", "yt": "t9UJ3cjej_w"},
            ]},
        ],
    },
    {
        "key": "data-tools-for-officials",
        "name": "Python & Data Tools for Statistical Officers",
        "provider": "NPTEL (IIT Madras) — Python for Data Science",
        "badge": "Technical",
        "level": "L1 → L2",
        "hours": 16,
        "tier": "core",
        "lab_after_module": 1,
        "areas": ["Python", "SQL", "Data Visualization", "Data Interpretation"],
        "description": "Python and SQL for the officer who needs to clean, tabulate and visualize survey microdata — no prior programming assumed.",
        "modules": [
            {"title": "Module 1 · Python Foundations for Data Work", "videos": [
                {"title": "NPTEL — Python for Data Science, Week 1 (playlist)", "yt": "PLrpK1inhO61V0YJRPz7b9EquPxT9PwEf6", "playlist": True},
            ]},
            {"title": "Module 2 · Tabulating & Cleaning Survey Microdata", "videos": [
                {"title": "NPTEL — Python for Data Science, data wrangling (playlist)", "yt": "PLrpK1inhO61V0YJRPz7b9EquPxT9PwEf6", "playlist": True},
            ]},
            {"title": "Module 3 · Visualization for Statistical Reporting", "videos": [
                {"title": "NPTEL — Python for Data Science, visualization (playlist)", "yt": "PLrpK1inhO61V0YJRPz7b9EquPxT9PwEf6", "playlist": True},
            ]},
        ],
    },
    # ---- Banking track (Department of Financial Services) ----
    {
        "key": "banking-regulation-basics",
        "name": "Banking Regulation & Structure in India",
        "provider": "NPTEL (IIM/IIT) + RBI Outreach",
        "badge": "Domain",
        "level": "L1 → L2",
        "hours": 8,
        "tier": "core",
        "areas": ["Banking Regulations", "Ethics and Values"],
        "description": "How RBI regulates the banking system — the Banking Regulation Act, licensing, and the structure of commercial, cooperative and payments banks.",
        "modules": [
            {"title": "Module 1 · Structure of the Indian Banking System", "videos": [
                {"title": "NPTEL — Indian Financial System, Banking Structure (playlist)", "yt": "PLrpK1inhO61V0YJRPz7b9EquPxT9PwEf6", "playlist": True},
                {"title": "RBI Outreach — Role and Functions of the Reserve Bank of India", "yt": "H0Ks-Tdac98"},
            ]},
            {"title": "Module 2 · Banking Regulation Act & RBI Powers", "videos": [
                {"title": "NPTEL — Banking Law and Regulation lecture", "yt": "WupQaRapFvw"},
                {"title": "RBI supervisory framework overview", "yt": "bNesUTaZLN8"},
            ]},
            {"title": "Module 3 · Licensing, Governance & Compliance Ethics", "videos": [
                {"title": "NPTEL — Corporate governance in banks", "yt": "rTQ_1m6LPQE"},
                {"title": "Banking ethics and compliance case studies", "yt": "r7v7HFLO6FY"},
            ]},
        ],
    },
    {
        "key": "financial-inclusion-jandhan",
        "name": "Financial Inclusion & Government Banking Schemes",
        "provider": "NPTEL + DFS/PMJDY case studies",
        "badge": "Domain",
        "level": "L1",
        "hours": 6,
        "tier": "core",
        "easier_alt": "financial-inclusion-primer",
        "areas": ["Financial Inclusion", "Priority Sector Lending", "Citizen Centricity"],
        "description": "Pradhan Mantri Jan Dhan Yojana, Priority Sector Lending norms, and how last-mile banking access is delivered and measured.",
        "modules": [
            {"title": "Module 1 · Financial Inclusion — Concepts & PMJDY", "videos": [
                {"title": "Financial Inclusion in India — an overview", "yt": "H0Ks-Tdac98"},
                {"title": "PMJDY — objectives and progress", "yt": "WupQaRapFvw"},
            ]},
            {"title": "Module 2 · Priority Sector Lending Norms", "videos": [
                {"title": "NPTEL — Priority Sector Lending & agricultural credit", "yt": "bNesUTaZLN8"},
                {"title": "RBI PSL guidelines explained", "yt": "rTQ_1m6LPQE"},
            ]},
            {"title": "Module 3 · Measuring Inclusion Outcomes", "videos": [
                {"title": "Financial inclusion index — methodology", "yt": "r7v7HFLO6FY"},
                {"title": "Last-mile banking — Business Correspondent model", "yt": "0EcXYr3Brl4"},
            ]},
        ],
    },
    {
        "key": "risk-management-npa",
        "name": "Credit Risk & NPA Management",
        "provider": "NPTEL (IIM) — Risk Management in Banking",
        "badge": "Domain",
        "level": "L2 → L3",
        "hours": 10,
        "tier": "core",
        "areas": ["Risk Management", "Data Analysis", "Decision Making"],
        "description": "How banks assess credit risk, classify non-performing assets, and apply Basel III capital adequacy norms.",
        "modules": [
            {"title": "Module 1 · Credit Risk Fundamentals", "videos": [
                {"title": "NPTEL — Credit risk assessment fundamentals", "yt": "sOP6VibhtgU"},
                {"title": "Understanding NPAs — classification and provisioning", "yt": "BUjaEYfmNFM"},
            ]},
            {"title": "Module 2 · Basel III Capital Adequacy", "videos": [
                {"title": "NPTEL — Basel norms and capital adequacy ratio", "yt": "0EcXYr3Brl4"},
                {"title": "Basel III explained for bank officers", "yt": "r_IMVzoVH6M"},
            ]},
            {"title": "Module 3 · Stress Testing & Resolution", "videos": [
                {"title": "Bank stress testing — methodology overview", "yt": "sOP6VibhtgU"},
                {"title": "IBC and resolution of stressed assets", "yt": "BUjaEYfmNFM"},
            ]},
        ],
    },
    {
        "key": "digital-banking-upi",
        "name": "Digital Banking & Payment Systems",
        "provider": "NPTEL + NPCI/RBI digital payments outreach",
        "badge": "Technical",
        "level": "L1 → L2",
        "hours": 8,
        "tier": "core",
        "lab_after_module": 1,
        "areas": ["Digital Banking", "Cybersecurity and Data Protection"],
        "description": "UPI, IMPS, NEFT/RTGS and the regulatory framework securing India's digital payments ecosystem.",
        "modules": [
            {"title": "Module 1 · Payment Systems Landscape (UPI, IMPS, NEFT/RTGS)", "videos": [
                {"title": "How UPI works — architecture overview", "yt": "rfscVS0vtbw"},
                {"title": "NPTEL — Digital payment systems in India", "yt": "PLwdnzlV3ogoUdLSIGNmXpnDLrnEqcNbaI", "playlist": True},
            ]},
            {"title": "Module 2 · Digital Banking Security & Fraud Prevention", "videos": [
                {"title": "Payment fraud prevention — customer protection framework", "yt": "bNesUTaZLN8"},
                {"title": "Cybersecurity basics for financial services", "yt": "H0Ks-Tdac98"},
            ]},
            {"title": "Module 3 · Emerging Trends (CBDC, Account Aggregators)", "videos": [
                {"title": "Digital Rupee (CBDC) — concept and pilot", "yt": "WupQaRapFvw"},
                {"title": "Account Aggregator framework explained", "yt": "rTQ_1m6LPQE"},
            ]},
        ],
    },
    {
        "key": "data-analysis-for-banking",
        "name": "Data Analysis for Banking & Financial Services",
        "provider": "NPTEL (IIT Madras) — Python for Data Science",
        "badge": "Technical",
        "level": "L1 → L2",
        "hours": 14,
        "tier": "core",
        "lab_after_module": 1,
        "areas": ["Data Analysis", "Digital Banking"],
        "description": "Python and SQL fundamentals applied to loan portfolios, transaction monitoring and regulatory reporting.",
        "modules": [
            {"title": "Module 1 · Python & SQL Foundations for Banking Data", "videos": [
                {"title": "NPTEL — Python for Data Science, Week 1 (playlist)", "yt": "PLrpK1inhO61V0YJRPz7b9EquPxT9PwEf6", "playlist": True},
            ]},
            {"title": "Module 2 · Analysing Loan Portfolios & NPA Trends", "videos": [
                {"title": "NPTEL — Python for Data Science, data wrangling (playlist)", "yt": "PLrpK1inhO61V0YJRPz7b9EquPxT9PwEf6", "playlist": True},
            ]},
            {"title": "Module 3 · Dashboards for Regulatory Reporting", "videos": [
                {"title": "NPTEL — Python for Data Science, visualization (playlist)", "yt": "PLrpK1inhO61V0YJRPz7b9EquPxT9PwEf6", "playlist": True},
            ]},
        ],
    },
    {
        "key": "banking-ethics-governance",
        "name": "Ethics, Governance & Decision-Making in Public Banking",
        "provider": "NSSTA-style Behavioural Track (Mission Karmayogi FRAC)",
        "badge": "Behavioural",
        "level": "L1 → L2",
        "hours": 6,
        "tier": "core",
        "areas": ["Ethics and Values", "Decision Making", "Communication"],
        "description": "Conflict-of-interest handling, escalation protocols, and communicating financial risk decisions to senior leadership.",
        "modules": [
            {"title": "Module 1 · Ethics & Conflict of Interest in Lending", "videos": [
                {"title": "Public sector ethics — conflict of interest case studies", "yt": "r7v7HFLO6FY"},
            ]},
            {"title": "Module 2 · Decision-Making Under Regulatory Uncertainty", "videos": [
                {"title": "Decision-making frameworks for public officers", "yt": "0EcXYr3Brl4"},
            ]},
            {"title": "Module 3 · Communicating Financial Risk to Leadership", "videos": [
                {"title": "Communicating complex data to non-technical leadership", "yt": "r_IMVzoVH6M"},
            ]},
        ],
    },

    # ---- Foundational (easier-alternative) courses — banking track ----
    {
        "key": "financial-inclusion-primer",
        "name": "Financial Inclusion — Primer",
        "provider": "DFS/PMJDY outreach",
        "badge": "Foundational",
        "level": "L1",
        "hours": 3,
        "tier": "foundational",
        "foundation_for": "financial-inclusion-jandhan",
        "areas": ["Financial Inclusion"],
        "description": "A gentler on-ramp before Financial Inclusion & Government Banking Schemes — plain-language coverage of why PMJDY exists and how it works.",
        "modules": [
            {"title": "Module 1 · Why Financial Inclusion Matters", "videos": [
                {"title": "Financial Inclusion in India — an overview", "yt": "H0Ks-Tdac98"},
            ]},
            {"title": "Module 2 · PMJDY in Plain Language", "videos": [
                {"title": "PMJDY — objectives and progress", "yt": "WupQaRapFvw"},
            ]},
        ],
    },
]


SPACE_TRACK = ["rs-fundamentals", "gis-essentials", "python-geospatial", "satcom-gnss", "geo-governance"]
STATISTICS_TRACK = ["official-statistics-foundations", "national-accounts-price-stats", "data-tools-for-officials"]
BANKING_TRACK = ["banking-regulation-basics", "financial-inclusion-jandhan", "risk-management-npa",
                 "digital-banking-upi", "data-analysis-for-banking", "banking-ethics-governance"]

_TRACKS = {"space": SPACE_TRACK, "statistics": STATISTICS_TRACK, "banking": BANKING_TRACK}


def get_roadmap(department_key: str):
    """Default on-site roadmap for a department — core courses only.
    Foundational (easier-alternative) courses are never shown by default;
    they're surfaced on request via the learner chatbot / swap_roadmap_course."""
    keys = _TRACKS.get(department_key, [])
    return [c for k in keys for c in ROADMAP_COURSES if c["key"] == k]


def get_course(key: str):
    for c in ROADMAP_COURSES:
        if c["key"] == key:
            return c
    return None


# ---------- Hands-On Coding Lab problems ----------
# Graded entirely client-side (Pyodide): the student's code is run, then each
# test case's function call is executed against it. Problem `id`s are matched
# against a fixed dispatch table in dummy-igot/lab.html's buildCall() — do not
# rename an id here without updating that table too.

CODING_LAB_PROBLEMS = {
    "python-geospatial": {
        "title": "Hands-On Lab: Geospatial Python",
        "subtitle": "NDVI, vegetation filtering and pixel classification — the everyday building blocks of satellite image analysis.",
        "problems": [
            {
                "id": "pg_p1", "title": "NDVI Calculator", "difficulty": "Easy",
                "description": "Write `ndvi(red, nir)` that computes the Normalized Difference Vegetation "
                                "Index: `(nir - red) / (nir + red)`.\n- `red` and `nir` are reflectance values (floats).\n"
                                "- Return a float.",
                "hints": ["NDVI = (NIR - Red) / (NIR + Red)", "Watch out for division — both inputs are floats here so normal `/` is fine."],
                "starter_code": "def ndvi(red, nir):\n    # TODO: return the NDVI value\n    pass\n",
                "test_cases": [
                    {"label": "red=0.2, nir=0.5", "input": {"red": 0.2, "nir": 0.5}, "expected": 0.42857142857142855},
                    {"label": "red=0.1, nir=0.1 (bare soil)", "input": {"red": 0.1, "nir": 0.1}, "expected": 0.0},
                    {"label": "red=0.3, nir=0.1 (water)", "input": {"red": 0.3, "nir": 0.1}, "expected": -0.5},
                ],
            },
            {
                "id": "pg_p2", "title": "Filter Vegetation Pixels", "difficulty": "Easy",
                "description": "Write `filter_vegetation(pixel_list, threshold)`. `pixel_list` is a list of "
                                "`{\"id\": int, \"ndvi\": float}` dicts. Return a list of the `id`s whose `ndvi` "
                                "is **greater than or equal to** `threshold`, keeping their original order.",
                "hints": ["A simple list comprehension does this in one line.", "`>=`, not `>`."],
                "starter_code": "def filter_vegetation(pixel_list, threshold):\n    # TODO: return a list of ids with ndvi >= threshold\n    pass\n",
                "test_cases": [
                    {"label": "mixed pixels, threshold 0.3",
                     "input": {"pixel_list": [{"id": 1, "ndvi": 0.1}, {"id": 2, "ndvi": 0.5}, {"id": 3, "ndvi": 0.35}], "threshold": 0.3},
                     "expected": [2, 3]},
                    {"label": "no pixel meets threshold",
                     "input": {"pixel_list": [{"id": 1, "ndvi": 0.05}, {"id": 2, "ndvi": 0.02}], "threshold": 0.3},
                     "expected": []},
                ],
            },
            {
                "id": "pg_p3", "title": "Classify Image Pixels", "difficulty": "Medium",
                "description": "Write `classify_image(pixels)`. `pixels` is a list of `{\"id\": int, \"ndvi\": float}` "
                                "dicts. Return a list of `{\"id\": int, \"status\": str}` dicts where `status` is:\n"
                                "- `\"water\"` if `ndvi < 0`\n- `\"soil\"` if `0 <= ndvi < 0.3`\n"
                                "- `\"vegetation\"` if `ndvi >= 0.3`",
                "hints": ["Keep the output order the same as the input order.", "This is exactly the same threshold as the previous problem, just with three bands instead of one."],
                "starter_code": "def classify_image(pixels):\n    # TODO: return [{\"id\":.., \"status\":..}, ...]\n    pass\n",
                "test_cases": [
                    {"label": "one of each class",
                     "input": {"pixels": [{"id": 1, "ndvi": -0.2}, {"id": 2, "ndvi": 0.1}, {"id": 3, "ndvi": 0.6}]},
                     "expected_statuses": ["water", "soil", "vegetation"]},
                    {"label": "boundary values (0.29 vs 0.3)",
                     "input": {"pixels": [{"id": 1, "ndvi": 0.29}, {"id": 2, "ndvi": 0.3}]},
                     "expected_statuses": ["soil", "vegetation"]},
                ],
            },
        ],
    },
    "data-tools-for-officials": {
        "title": "Hands-On Lab: Data Tools for Officials",
        "subtitle": "Summary statistics, outlier detection and grouped averages — the everyday building blocks of tabulating survey data.",
        "problems": [
            {
                "id": "dto_p1", "title": "Summary Statistics", "difficulty": "Easy",
                "description": "Write `summary_stats(data)`. `data` is a list of numbers. Return "
                                "`{\"mean\": float, \"min\": float, \"max\": float}`.",
                "hints": ["Python's built-in `sum`, `min`, `max` are all you need."],
                "starter_code": "def summary_stats(data):\n    # TODO: return {\"mean\":.., \"min\":.., \"max\":..}\n    pass\n",
                "test_cases": [
                    {"label": "[10, 20, 30, 40]", "input": {"data": [10, 20, 30, 40]}, "expected": {"mean": 25, "min": 10, "max": 40}},
                    {"label": "single value [5]", "input": {"data": [5]}, "expected": {"mean": 5, "min": 5, "max": 5}},
                ],
            },
            {
                "id": "dto_p2", "title": "Remove Outliers", "difficulty": "Medium",
                "description": "Write `remove_outliers(data)`. `data` is a list of numbers. An outlier is any "
                                "value **greater than double the median** of the list. Return the remaining "
                                "values, keeping their original order.",
                "hints": ["`sorted(data)[len(data)//2]` gives the median for odd-length lists (all test cases here have odd length).", "Compute the median first, then filter."],
                "starter_code": "def remove_outliers(data):\n    # TODO: drop values > 2x the median, keep order\n    pass\n",
                "test_cases": [
                    {"label": "[10, 12, 11, 13, 100] — 100 is the outlier",
                     "input": {"data": [10, 12, 11, 13, 100]}, "expected_length": 4, "expected_no_value": 100},
                    {"label": "[5, 5, 5, 5] — nothing to remove",
                     "input": {"data": [5, 5, 5, 5]}, "expected_length": 4},
                ],
            },
            {
                "id": "dto_p3", "title": "Grouped Average", "difficulty": "Medium",
                "description": "Write `group_average(records, group_key, value_key)`. `records` is a list of "
                                "dicts. Group them by `record[group_key]` and return `{group_value: average}` "
                                "where `average` is the mean of `record[value_key]` within that group.",
                "hints": ["A dict of running (sum, count) per group, then divide at the end, works well."],
                "starter_code": "def group_average(records, group_key, value_key):\n    # TODO: return {group: average}\n    pass\n",
                "test_cases": [
                    {"label": "group by dept",
                     "input": {"records": [{"dept": "A", "score": 10}, {"dept": "A", "score": 20}, {"dept": "B", "score": 5}],
                               "group_key": "dept", "value_key": "score"},
                     "expected": {"A": 15.0, "B": 5.0}},
                    {"label": "group by region",
                     "input": {"records": [{"region": "north", "pct": 50}, {"region": "south", "pct": 70}, {"region": "north", "pct": 30}],
                               "group_key": "region", "value_key": "pct"},
                     "expected": {"north": 40.0, "south": 70.0}},
                ],
            },
        ],
    },
    "data-analysis-for-banking": {
        "title": "Hands-On Lab: Data Analysis for Banking",
        "subtitle": "NPA classification and branch-level risk metrics — the everyday building blocks of loan portfolio analysis.",
        "problems": [
            {
                "id": "dab_p1", "title": "Classify NPAs", "difficulty": "Easy",
                "description": "Write `classify_npa(loans)`. `loans` is a list of `{\"id\": int, \"days_overdue\": int}` "
                                "dicts. Return a list of `{\"id\": int, \"status\": str}` dicts where `status` is:\n"
                                "- `\"standard\"` if `days_overdue <= 90`\n"
                                "- `\"sub-standard\"` if `91 <= days_overdue <= 365`\n"
                                "- `\"doubtful\"` if `days_overdue > 365`",
                "hints": ["This mirrors the real RBI NPA classification rule covered in the Risk Management course."],
                "starter_code": "def classify_npa(loans):\n    # TODO: return [{\"id\":.., \"status\":..}, ...]\n    pass\n",
                "test_cases": [
                    {"label": "one of each class",
                     "input": {"loans": [{"id": 1, "days_overdue": 30}, {"id": 2, "days_overdue": 120}, {"id": 3, "days_overdue": 400}]},
                     "expected_statuses": ["standard", "sub-standard", "doubtful"]},
                    {"label": "boundary values (90/91/365/366)",
                     "input": {"loans": [{"id": 1, "days_overdue": 90}, {"id": 2, "days_overdue": 91},
                                          {"id": 3, "days_overdue": 365}, {"id": 4, "days_overdue": 366}]},
                     "expected_statuses": ["standard", "sub-standard", "sub-standard", "doubtful"]},
                ],
            },
            {
                "id": "dab_p2", "title": "NPA Ratio by Branch", "difficulty": "Medium",
                "description": "Write `npa_ratio_by_branch(loans)`. `loans` is a list of "
                                "`{\"branch\": str, \"amount\": float, \"is_npa\": bool}` dicts. Return "
                                "`{branch: npa_ratio}` where `npa_ratio` is the percentage of that branch's "
                                "total loan amount that is flagged `is_npa` (0-100).",
                "hints": ["ratio = 100 * (sum of NPA amounts) / (sum of all amounts), per branch."],
                "starter_code": "def npa_ratio_by_branch(loans):\n    # TODO: return {branch: npa_percentage}\n    pass\n",
                "test_cases": [
                    {"label": "two branches, one with an NPA",
                     "input": {"loans": [{"branch": "X", "amount": 100, "is_npa": False}, {"branch": "X", "amount": 100, "is_npa": True},
                                          {"branch": "Y", "amount": 50, "is_npa": False}]},
                     "expected": {"X": 50.0, "Y": 0.0}},
                    {"label": "fully stressed branch",
                     "input": {"loans": [{"branch": "Z", "amount": 40, "is_npa": True}, {"branch": "Z", "amount": 60, "is_npa": True}]},
                     "expected": {"Z": 100.0}},
                ],
            },
            {
                "id": "dab_p3", "title": "Flag Suspicious Transactions", "difficulty": "Medium",
                "description": "Write `flag_suspicious(transactions, threshold)`. `transactions` is a list of "
                                "`{\"id\": int, \"amount\": float}` dicts. Return a list of "
                                "`{\"id\": int, \"suspicious\": bool}` dicts where `suspicious` is `True` when "
                                "`amount` is **strictly greater than** `threshold`.",
                "hints": ["Strictly greater than — a transaction exactly at the threshold is not suspicious."],
                "starter_code": "def flag_suspicious(transactions, threshold=50000):\n    # TODO: return [{\"id\":.., \"suspicious\":..}, ...]\n    pass\n",
                "test_cases": [
                    {"label": "one above, one at, one below threshold",
                     "input": {"transactions": [{"id": 1, "amount": 10000}, {"id": 2, "amount": 60000}, {"id": 3, "amount": 50000}], "threshold": 50000},
                     "expected_suspicious": [False, True, False]},
                    {"label": "single large transaction",
                     "input": {"transactions": [{"id": 1, "amount": 99999}], "threshold": 50000},
                     "expected_suspicious": [True]},
                ],
            },
        ],
    },
    "digital-banking-upi": {
        "title": "Hands-On Lab: Digital Banking & UPI",
        "subtitle": "UPI ID validation and payment-success analytics — the everyday building blocks of digital payments monitoring.",
        "problems": [
            {
                "id": "upi_p1", "title": "Validate a UPI ID", "difficulty": "Easy",
                "description": "Write `validate_upi_id(upi_id)`. A valid UPI ID has the form `handle@bank`: "
                                "a **non-empty** local part before `@`, exactly one `@`, and a **non-empty** "
                                "bank handle after it. Return a bool.",
                "hints": ["`upi_id.count('@') == 1` handles the \"exactly one @\" rule.", "`upi_id.split('@')` then check both parts are non-empty."],
                "starter_code": "def validate_upi_id(upi_id):\n    # TODO: return True/False\n    pass\n",
                "test_cases": [
                    {"label": "valid id", "input": {"upi_id": "ramesh.kumar@okhdfcbank"}, "expected": True},
                    {"label": "missing @", "input": {"upi_id": "invalid-upi-id"}, "expected": False},
                    {"label": "empty local part", "input": {"upi_id": "@sbi"}, "expected": False},
                ],
            },
            {
                "id": "upi_p2", "title": "Success Rate by Bank", "difficulty": "Medium",
                "description": "Write `success_rate_by_bank(transactions)`. `transactions` is a list of "
                                "`{\"bank\": str, \"status\": \"success\"|\"failed\"}` dicts. Return "
                                "`{bank: success_percentage}` (0-100) for each bank.",
                "hints": ["percentage = 100 * successes / total, per bank."],
                "starter_code": "def success_rate_by_bank(transactions):\n    # TODO: return {bank: success_percentage}\n    pass\n",
                "test_cases": [
                    {"label": "SBI half fail, HDFC all succeed",
                     "input": {"transactions": [{"bank": "SBI", "status": "success"}, {"bank": "SBI", "status": "failed"},
                                                 {"bank": "HDFC", "status": "success"}]},
                     "expected": {"SBI": 50.0, "HDFC": 100.0}},
                ],
            },
            {
                "id": "upi_p3", "title": "Find Duplicate Payments", "difficulty": "Hard",
                "description": "Write `find_duplicates(payments)`. `payments` is a list of "
                                "`{\"id\": int, \"to\": str, \"amount\": float, \"timestamp\": str}` dicts. A "
                                "payment is a duplicate if an **earlier** payment in the list has the exact "
                                "same `to`, `amount` and `timestamp`. Return the `id`s of the duplicate "
                                "payments (not the originals), in the order they appear.",
                "hints": ["Walk the list once, keeping a `set` of `(to, amount, timestamp)` tuples you've already seen.", "Only flag it as a duplicate if you've seen that combination before — the first occurrence is never a duplicate."],
                "starter_code": "def find_duplicates(payments):\n    # TODO: return a list of duplicate payment ids\n    pass\n",
                "test_cases": [
                    {"label": "one exact repeat",
                     "input": {"payments": [{"id": 1, "to": "a@bank", "amount": 100, "timestamp": "10:00"},
                                             {"id": 2, "to": "a@bank", "amount": 100, "timestamp": "10:00"},
                                             {"id": 3, "to": "b@bank", "amount": 200, "timestamp": "10:05"}]},
                     "expected": [2]},
                    {"label": "no duplicates (different amounts)",
                     "input": {"payments": [{"id": 1, "to": "a@bank", "amount": 50, "timestamp": "09:00"},
                                             {"id": 2, "to": "a@bank", "amount": 60, "timestamp": "09:00"}]},
                     "expected": []},
                ],
            },
        ],
    },
}
