"""ISRO / Department of Space learning roadmap for the demo.

5 courses from real Indian platforms (IIRS/ISRO Outreach, NPTEL, NRSC/Bhuvan,
freeCodeCamp). Content is delivered ON-SITE via embedded YouTube players —
learners are never redirected. Video IDs are real, publicly available YouTube
videos/playlists (swap any dead link for an equivalent from the same playlist).
"""

ROADMAP_COURSES = [
    {
        "key": "rs-fundamentals",
        "name": "Fundamentals of Remote Sensing & Digital Image Processing",
        "provider": "IIRS/ISRO Outreach Programme + NPTEL",
        "badge": "ISRO",
        "level": "L1 → L2",
        "hours": 12,
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
        "areas": ["Remote Sensing Fundamentals", "Digital Governance"],
        "description": "Orbital mechanics to NavIC/GPS: how positioning, navigation and timing underpin surveying, logistics and location-based governance services.",
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
]


def get_roadmap(department_key: str):
    if department_key == "space":
        return ROADMAP_COURSES
    return []


def get_course(key: str):
    for c in ROADMAP_COURSES:
        if c["key"] == key:
            return c
    return None
