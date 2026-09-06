"""NSSTA TPAC-recommended training programmes.

TPAC (Training Programme Approval Committee) of NSSTA approves cadre-specific
training programmes for the Indian Statistical Service (ISS) and Subordinate
Statistical Service (SSS). These are surfaced alongside iGOT courses in the
personalized recommendation layer, per PS 26101.
"""

TPAC_PATHWAYS = [
    {
        "key": "tpac-sna-core",
        "name": "System of National Accounts (SNA 2008): GVA and Base Revision",
        "provider": "NSSTA / National Accounts Division",
        "badge": "TPAC · ISS",
        "cadre": "ISS",
        "level": "Advanced",
        "hours": 40,
        "areas": ["National Accounts", "Data Quality Frameworks"],
        "description": "Institutional sector accounts, supply-use tables, double deflation methodologies, and financial intermediation (FISIM) under SNA 2008.",
    },
    {
        "key": "tpac-cpi-index",
        "name": "Consumer Price Index (CPI): Laspeyres Formula & Basket Revision",
        "provider": "Price Statistics Division / NSSTA",
        "badge": "TPAC · Both",
        "cadre": "Both",
        "level": "Intermediate",
        "hours": 22,
        "areas": ["Price Statistics", "Statistical Methods"],
        "description": "CPI compilation workflow, Laspeyres geometric mean indexation, price quotation validation, and basket revision cycles.",
    },
    {
        "key": "tpac-plfs-capi",
        "name": "CAPI Tablet Administration & Multi-Stage Sampling in NSSO",
        "provider": "NSSO FOD / NSSTA",
        "badge": "TPAC · SSS",
        "cadre": "SSS",
        "level": "Beginner",
        "hours": 18,
        "areas": ["Survey Design", "Sampling Techniques"],
        "description": "Field verification protocol, household selection procedures, response non-sampling error reduction, and CAPI synchronization.",
    },
    {
        "key": "tpac-r-survey",
        "name": "R for Official Statistics: Survey Weighting & Microdata Analysis",
        "provider": "MoSPI Training Cell / IIT Kanpur",
        "badge": "TPAC · ISS",
        "cadre": "ISS",
        "level": "Advanced",
        "hours": 36,
        "areas": ["Statistical Methods", "Python", "Metadata Standards"],
        "description": "Advanced microdata analysis using the R survey package for NSSO round estimation and variance calculations.",
    },
    {
        "key": "tpac-ai-anomaly",
        "name": "AI/ML Applications in Price Statistics & Anomaly Detection",
        "provider": "Computer Centre MoSPI / IIIT Hyderabad",
        "badge": "TPAC · Both",
        "cadre": "Both",
        "level": "Intermediate",
        "hours": 20,
        "areas": ["AI and Emerging Tech", "Price Statistics", "Data Quality Frameworks"],
        "description": "Machine learning workflows for automated outlier detection in weekly retail price quotations and automated item classification.",
    },
    {
        "key": "tpac-dpdp-gov",
        "name": "DPDP Act 2023 & Respondent Confidentiality in Official Statistics",
        "provider": "MeitY / MoSPI Legal",
        "badge": "TPAC · Both",
        "cadre": "Both",
        "level": "Intermediate",
        "hours": 12,
        "areas": ["Cybersecurity and Data Protection", "Ethics and Values"],
        "description": "Legal mandates of the DPDP Act 2023, consent architectures, anonymization, and Collection of Statistics Act 2008 harmonisation.",
    },
    {
        "key": "tpac-gis-spatial",
        "name": "Applied QGIS & Spatial Analysis for Field Survey Operations",
        "provider": "NSSTA / Survey of India",
        "badge": "TPAC · Both",
        "cadre": "Both",
        "level": "Intermediate",
        "hours": 30,
        "areas": ["GIS", "Sampling Techniques"],
        "description": "Geographic information systems for boundary delineation, geo-tagging primary sampling units (PSUs), and satellite crop overlay.",
    },
]

TPAC_BY_KEY = {c["key"]: c for c in TPAC_PATHWAYS}


def get_tpac_pathways(department_key: str | None = None, top_gaps: list | None = None) -> list:
    """TPAC programmes, ranked against the user's measured gaps when available."""
    gap_by_area = {g["area"]: g["gap"] for g in (top_gaps or [])}

    def rank(c: dict) -> float:
        return max((gap_by_area.get(a, 0) for a in c["areas"]), default=0)

    scored = sorted(TPAC_PATHWAYS, key=rank, reverse=True)
    if department_key == "space":
        # space users still see cross-cutting TPAC programmes first
        cross = [c for c in scored if not any(a in ("National Accounts", "Price Statistics",
                                                    "Labour Statistics", "Survey Design",
                                                    "Sampling Techniques") for a in c["areas"])]
        domain = [c for c in scored if c not in cross]
        return cross + domain
    return scored
