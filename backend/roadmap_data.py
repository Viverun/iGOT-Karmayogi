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
            {"title": "Module 1 · Role, Structure & Functions of the RBI", "videos": [
                {"title": "Role and Functions of the RBI", "yt": "Bqyek4dnycM"},
                {"title": "Reserve Bank of India — Structure & Functions", "yt": "zNpLVG79Pfk"},
            ]},
            {"title": "Module 2 · Banking Regulation Act & RBI Powers", "videos": [
                {"title": "Functions of RBI — supervisory & regulatory powers", "yt": "tdRbdx2yU8Q"},
            ]},
            {"title": "Module 3 · Licensing, Governance & Compliance Ethics", "videos": [
                {"title": "Role and Functions of the RBI (governance & compliance)", "yt": "Bqyek4dnycM"},
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
                {"title": "Jan Dhan Yojana in 2 Minutes | PMJDY Explained", "yt": "bl-IPyNxd1g"},
                {"title": "Pradhan Mantri Jan-Dhan Yojana | #11YearsOfJanDhan", "yt": "gP4xUiQt974"},
            ]},
            {"title": "Module 2 · Priority Sector Lending Norms", "videos": [
                {"title": "RBI's Biggest Lending Rule | PSL Explained", "yt": "nE_TLJh-gkY"},
                {"title": "RBI Priority Sector Lending — 8 priority sectors explained", "yt": "BKPL9ELF3pw"},
            ]},
            {"title": "Module 3 · Measuring Inclusion Outcomes", "videos": [
                {"title": "PM Jan Dhan Yojana — facilities & benefits explained", "yt": "fWXlhlzW1SU"},
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
                {"title": "What Is Credit Risk? | The Biggest Risk in Banking Explained", "yt": "PTLPfM8EHaY"},
                {"title": "Credit Risk Explained | PD, LGD, EAD Made Simple", "yt": "gnIBNFVzjsQ"},
            ]},
            {"title": "Module 2 · NPA Classification & Basel III Capital Adequacy", "videos": [
                {"title": "What Is NPA In Banking? Non Performing Assets Explained", "yt": "LynCHhDEv4s"},
                {"title": "NPA Explained | Types, Causes, Provisioning of NPA", "yt": "xWseKgOL_C0"},
            ]},
            {"title": "Module 3 · Stress Testing & Resolution", "videos": [
                {"title": "Credit Risk Management — Credit Analysis and Risk Assessment", "yt": "yYl9rbKmb6o"},
                {"title": "Non-Performing Assets — impact on banks & resolution", "yt": "9LRGVcTeUXU"},
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
        "areas": ["Digital Banking", "Cybersecurity and Data Protection"],
        "description": "UPI, IMPS, NEFT/RTGS and the regulatory framework securing India's digital payments ecosystem.",
        "modules": [
            {"title": "Module 1 · Payment Systems Landscape (UPI, IMPS, NEFT/RTGS)", "videos": [
                {"title": "What is UPI? | Unified Payments Interface Explained | Full Guide", "yt": "Kow5dgx0hFQ"},
            ]},
            {"title": "Module 2 · Digital Banking Security & Fraud Prevention", "videos": [
                {"title": "AI for Risk Management in Banking — Fraud Detection & Credit Risk", "yt": "MruBEP9SMKo"},
            ]},
            {"title": "Module 3 · Emerging Trends (CBDC, Account Aggregators)", "videos": [
                {"title": "India's Digital Rupee — RBI Launches First Pilot | CBDC Explained", "yt": "rz9HJtsp65w"},
                {"title": "RBI Digital Rupee Pilot — How Retail CBDC Differs From UPI", "yt": "D93iVphPyuo"},
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
                {"title": "Role and Functions of the RBI (regulatory conduct & oversight)", "yt": "Bqyek4dnycM"},
            ]},
            {"title": "Module 2 · Decision-Making Under Regulatory Uncertainty", "videos": [
                {"title": "What Is Credit Risk? | The Biggest Risk in Banking Explained", "yt": "PTLPfM8EHaY"},
            ]},
            {"title": "Module 3 · Communicating Financial Risk to Leadership", "videos": [
                {"title": "What Is NPA In Banking? Non Performing Assets Explained", "yt": "LynCHhDEv4s"},
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
                {"title": "Jan Dhan Yojana in 2 Minutes | PMJDY Explained", "yt": "bl-IPyNxd1g"},
            ]},
            {"title": "Module 2 · PMJDY in Plain Language", "videos": [
                {"title": "Pradhan Mantri Jan-Dhan Yojana | #11YearsOfJanDhan", "yt": "gP4xUiQt974"},
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
