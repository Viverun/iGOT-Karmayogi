"""Department-aware assessment question bank (dummy content, FRAC-flavoured).

Questions are grouped by competency type (Domain / Functional / Behavioural) and
served based on the logged-in user's department. Department matching is keyword
based — enough for a demo with one presented user (MoSPI) plus generic fallback.
"""

QUESTION_BANK = {
    "statistics": [
        {"id": "stat1", "qtype": "Domain", "area": "Sampling Techniques",
         "text": "A survey must estimate the average household expenditure in a large state with wide urban–rural variation. Which sampling design is most appropriate?",
         "options": ["Simple random sampling", "Stratified random sampling", "Systematic sampling with a random start", "Snowball sampling"], "answer": 1},
        {"id": "stat2", "qtype": "Domain", "area": "Survey Design",
         "text": "In the Official Statistical System, what is the primary purpose of a 'pilot round' before a full survey launch?",
         "options": ["To publish preliminary estimates", "To test the questionnaire, field logistics and training", "To satisfy administrative approval requirements", "To replace the census"], "answer": 1},
        {"id": "stat3", "qtype": "Domain", "area": "Statistical Methods",
         "text": "The Consumer Price Index (CPI) is an example of:",
         "options": ["An index number measuring price changes over time", "A measure of central tendency", "A sampling frame", "A regression coefficient"], "answer": 0},
        {"id": "stat4", "qtype": "Functional", "area": "Data Interpretation",
         "text": "A district's NSDP per capita is rising, but its Gini coefficient is also rising. What does this combination suggest?",
         "options": ["Uniform growth across all groups", "Average income growth with widening inequality", "Falling average income", "A data collection error"], "answer": 1},
        {"id": "stat5", "qtype": "Functional", "area": "Python",
         "text": "In pandas, which function is most direct for computing a mean by category?",
         "options": ["df.sort_values()", "df.groupby(col).mean()", "df.pivot()", "df.applymap()"], "answer": 1},
        {"id": "stat6", "qtype": "Functional", "area": "SQL",
         "text": "Which SQL clause filters rows AFTER grouping has been applied?",
         "options": ["WHERE", "HAVING", "ORDER BY", "LIMIT"], "answer": 1},
        {"id": "stat7", "qtype": "Functional", "area": "Digital Governance",
         "text": "The 'once-only' principle in digital government means:",
         "options": ["Citizens submit the same data to government only once, reused across departments", "Each scheme accepts only one application", "Data is stored only once for security", "Only one officer signs off a file"], "answer": 0},
        {"id": "stat8", "qtype": "Functional", "area": "Cybersecurity and Data Protection",
         "text": "Under the DPDP Act, 2023, before processing personal data a government body must generally ensure:",
         "options": ["Data is published openly", "A lawful basis and notice/consent requirements are met", "Data is kept for at least 10 years", "Consent of the Parliament"], "answer": 1},
        {"id": "stat9", "qtype": "Behavioural", "area": "Communication",
         "text": "You must present complex survey findings to non-technical senior leadership. The best first step is:",
         "options": ["Share the full raw dataset", "Lead with key findings in plain language with 2–3 charts", "Present the methodology in detail first", "Circulate the questionnaire"], "answer": 1},
        {"id": "stat10", "qtype": "Behavioural", "area": "Ethics and Values",
         "text": "A stakeholder pressures you to delay releasing an unfavourable statistic indefinitely. The appropriate action is to:",
         "options": ["Delay it as instructed", "Release modified estimates", "Follow the dissemination policy and escalate through official channels", "Leak it to the media"], "answer": 2},
    ],
    "space": [
        # ---- L1 (easy) ----
        {"id": "spc1", "level": "L1", "qtype": "Domain", "area": "Remote Sensing Fundamentals",
         "text": "Which type of satellite orbit allows continuous observation of the same area of the Earth?",
         "options": ["Polar sun-synchronous orbit", "Low Earth equatorial orbit", "Geostationary orbit", "Highly elliptical Molniya orbit"], "answer": 2},
        {"id": "spc2", "level": "L1", "qtype": "Domain", "area": "Remote Sensing Fundamentals",
         "text": "In optical remote sensing, the Normalized Difference Vegetation Index (NDVI) primarily indicates:",
         "options": ["Soil moisture at depth", "Vegetation health and density", "Atmospheric pressure", "Ocean salinity"], "answer": 1},
        {"id": "spc3", "level": "L1", "qtype": "Domain", "area": "Remote Sensing Fundamentals",
         "text": "Which sensor type can image the Earth's surface at night and through clouds?",
         "options": ["Optical multispectral sensor", "Thermal infrared only", "Synthetic Aperture Radar (SAR)", "Hyperspectral sensor"], "answer": 2},
        {"id": "spc4", "level": "L1", "qtype": "Domain", "area": "Satellite Data Processing",
         "text": "Georeferencing a satellite image means:",
         "options": ["Compressing the image for storage", "Assigning real-world coordinates to image pixels", "Increasing image resolution", "Removing cloud cover"], "answer": 1},
        {"id": "spc5", "level": "L1", "qtype": "Functional", "area": "GIS",
         "text": "A vector GIS layer differs from a raster layer in that it stores features as:",
         "options": ["Regular grid of pixels", "Points, lines and polygons with attributes", "Frequency bands", "Compressed video frames"], "answer": 1},
        {"id": "spc6", "level": "L1", "qtype": "Functional", "area": "Data Interpretation",
         "text": "Time-series analysis of NDVI over a district is best used to:",
         "options": ["Monitor crop health and drought conditions over time", "Design satellite hardware", "Replace ground surveys entirely", "Estimate population density"], "answer": 0},
        {"id": "spc7", "level": "L1", "qtype": "Functional", "area": "Digital Governance",
         "text": "The Bhuvan geoportal of ISRO is an example of:",
         "options": ["A communication satellite", "A national geospatial platform for public use", "A weather balloon programme", "A launch vehicle"], "answer": 1},
        {"id": "spc8", "level": "L1", "qtype": "Functional", "area": "Cybersecurity and Data Protection",
         "text": "Satellite imagery classified for restricted government use should be:",
         "options": ["Shared on public cloud drives", "Handled per government security classification and data-sharing policies", "Posted on social media for transparency", "Emailed to personal accounts"], "answer": 1},
        {"id": "spc9", "level": "L1", "qtype": "Behavioural", "area": "Communication",
         "text": "Explaining satellite-based flood-inundation maps to district officials, you should:",
         "options": ["Use technical radar terminology throughout", "Present actionable map findings with clear legends and next steps", "Only share raw data files", "Avoid showing maps"], "answer": 1},
        # ---- L2 (medium) ----
        {"id": "spc10", "level": "L2", "qtype": "Domain", "area": "Remote Sensing Fundamentals",
         "text": "A sun-synchronous polar orbit is preferred for Earth-observation satellites mainly because it:",
         "options": ["Keeps the satellite over one fixed point", "Passes each location at roughly the same local solar time, aiding comparison", "Avoids the Van Allen belts entirely", "Requires no station-keeping"], "answer": 1},
        {"id": "spc11", "level": "L2", "qtype": "Domain", "area": "Remote Sensing Fundamentals",
         "text": "Vegetation appears bright in near-infrared imagery primarily because of:",
         "options": ["Chlorophyll absorption in visible bands and high NIR reflectance from leaf structure", "Thermal emission from leaves", "Water content in stems", "Soil background"], "answer": 0},
        {"id": "spc12", "level": "L2", "qtype": "Domain", "area": "Satellite Data Processing",
         "text": "The spatial resolution of a sensor refers to:",
         "options": ["How many spectral bands it has", "The smallest ground feature it can distinguish", "How often it revisits a location", "Its radiometric accuracy"], "answer": 1},
        {"id": "spc13", "level": "L2", "qtype": "Domain", "area": "Satellite Data Processing",
         "text": "Atmospheric correction of optical imagery is performed to:",
         "options": ["Remove cloud shadows only", "Convert top-of-atmosphere reflectance to surface reflectance", "Sharpen image edges", "Reduce file size"], "answer": 1},
        {"id": "spc14", "level": "L2", "qtype": "Functional", "area": "GIS",
         "text": "An overlay analysis combining a flood-prone-area layer with a settlement layer is used to:",
         "options": ["Identify settlements at risk of flooding", "Classify land cover from scratch", "Georeference satellite images", "Compress map data"], "answer": 0},
        {"id": "spc15", "level": "L2", "qtype": "Functional", "area": "GIS",
         "text": "Which coordinate system is most appropriate for nationwide Indian mapping projects today?",
         "options": ["Latitude-longitude on Everest datum only", "LCC/WGS84-based projected systems as per NSDI standards", "Local survey plane coordinates everywhere", "UTM zones are banned"], "answer": 1},
        {"id": "spc16", "level": "L2", "qtype": "Functional", "area": "Python",
         "text": "Which Python library is most commonly used for reading and analysing raster geospatial data?",
         "options": ["Matplotlib", "Rasterio / GDAL", "BeautifulSoup", "Seaborn"], "answer": 1},
        {"id": "spc17", "level": "L2", "qtype": "Functional", "area": "Data Interpretation",
         "text": "A change-detection study shows urban area expansion of 12% over a decade. The most defensible first check before reporting is:",
         "options": ["Publish immediately", "Validate against independent data (ground truth, other sensors) and check classification accuracy", "Round the number down", "Only report the year of maximum change"], "answer": 1},
        {"id": "spc18", "level": "L2", "qtype": "Behavioural", "area": "Problem Solving",
         "text": "Cloud cover blocks optical imagery during a flood. The most practical response is to:",
         "options": ["Abandon the assessment", "Wait indefinitely for clear skies", "Use Synthetic Aperture Radar (SAR) data or multi-temporal composites", "Use last decade's imagery"], "answer": 2},
        # ---- L3 (hard) ----
        {"id": "spc19", "level": "L3", "qtype": "Domain", "area": "Satellite Data Processing",
         "text": "In SAR interferometry (InSAR), millimetre-scale ground deformation is estimated from:",
         "options": ["Backscatter intensity differences", "Phase differences between successive passes", "Polarisation ratios", "Thermal anomalies"], "answer": 1},
        {"id": "spc20", "level": "L3", "qtype": "Domain", "area": "Remote Sensing Fundamentals",
         "text": "A key limitation of using NDVI for crop-yield estimation in heterogeneous smallholder landscapes is:",
         "options": ["NDVI cannot be computed from satellites", "Mixed pixels saturate and confound crop type with background variability", "NDVI only works at night", "NDVI requires radar data"], "answer": 1},
        {"id": "spc21", "level": "L3", "qtype": "Domain", "area": "Satellite Data Processing",
         "text": "Speckle noise inherent in SAR imagery is best mitigated by:",
         "options": ["Nearest-neighbour resampling", "Multi-looking and adaptive filtering (e.g. Lee/Sigma filters)", "Histogram equalisation", "Increasing the pixel grid"], "answer": 1},
        {"id": "spc22", "level": "L3", "qtype": "Functional", "area": "GIS",
         "text": "For hydrological flood-inundation modelling, a Digital Elevation Model is used primarily to derive:",
         "options": ["Land ownership parcels", "Flow direction, accumulation and inundation extents", "Soil chemistry", "Population density"], "answer": 1},
        {"id": "spc23", "level": "L3", "qtype": "Functional", "area": "AI and Emerging Tech",
         "text": "When applying deep-learning semantic segmentation to satellite imagery, the most defensible way to report accuracy is:",
         "options": ["Training accuracy only", "Confusion-matrix metrics (IoU/F1) on a held-out spatially independent test set", "Visual inspection by one analyst", "Pixel count of predicted classes"], "answer": 1},
        {"id": "spc24", "level": "L3", "qtype": "Functional", "area": "Python",
         "text": "For processing a 50,000 x 50,000 pixel national mosaic that exceeds RAM, the most appropriate approach is:",
         "options": ["Load fully into a NumPy array", "Windowed/block-wise processing (e.g. rasterio windows or Dask arrays)", "Convert to CSV", "Downsample permanently"], "answer": 1},
        {"id": "spc25", "level": "L3", "qtype": "Behavioural", "area": "Decision Making",
         "text": "Two satellite-derived estimates of cropped area differ by 8%. As the approving officer you should:",
         "options": ["Pick the estimate from the newer satellite", "Average them and publish", "Commission a validation protocol comparing methodology, reference data and error bars before release", "Withhold both from all users"], "answer": 2},
    ],
    "general": [
        {"id": "gen1", "qtype": "Domain", "area": "National Priorities",
         "text": "Viksit Bharat 2047 envisions India as a developed nation by which year?",
         "options": ["2022", "2030", "2047", "2050"], "answer": 2},
        {"id": "gen2", "qtype": "Functional", "area": "Digital Governance",
         "text": "Which initiative provides a single sign-on for accessing multiple government digital services?",
         "options": ["DigiLocker", "Digital India", "Ayushman Bharat", "SWAYAM"], "answer": 0},
        {"id": "gen3", "qtype": "Functional", "area": "AI and Emerging Tech",
         "text": "A key risk of using generative AI for official drafting without review is:",
         "options": ["It is always slower than manual work", "Hallucinated or incorrect content presented confidently", "It cannot handle Indian languages", "It requires no electricity"], "answer": 1},
        {"id": "gen4", "qtype": "Behavioural", "area": "Citizen Centricity",
         "text": "'Jan Bhagidari' in governance best refers to:",
         "options": ["Public participation in planning and delivery", "Privatisation of services", "Judicial review", "Inter-ministerial coordination"], "answer": 0},
        {"id": "gen5", "qtype": "Behavioural", "area": "Decision Making",
         "text": "The 'rule-based to role-based' vision of Mission Karmayogi emphasises:",
         "options": ["Strict seniority-based postings", "Competency-driven role assignment and capacity building", "Outsourcing government roles", "Reducing the workforce"], "answer": 1},
        {"id": "gen6", "qtype": "Functional", "area": "Policy Formulation",
         "text": "Evidence-based policy making primarily relies on:",
         "options": ["Tradition and precedent only", "Data, evaluation and stakeholder evidence", "Media opinion polls alone", "Individual intuition"], "answer": 1},
    ],
}

DEPARTMENT_KEYWORDS = {
    "statistics": ["statistic", "mospi", "nso", "survey", "census"],
    "space": ["space", "isro", "adrin", "satellite"],
    # departments can be added here; everything else falls back to "general"
}


def department_key(department: str) -> str:
    d = (department or "").lower()
    for key, words in DEPARTMENT_KEYWORDS.items():
        if any(w in d for w in words):
            return key
    return "general"


def questions_for(department: str) -> list:
    return QUESTION_BANK[department_key(department)]
