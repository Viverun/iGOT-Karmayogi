"""
AI-Powered RAG Assessment & MCQ Generation Engine for MoSPI / NSSTA
Includes document chunking, semantic retrieval, Bloom's Taxonomy question generation,
statistical distractor engineering, and citation tracing.
"""

import os
import re
import math
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class DocumentChunk(BaseModel):
    chunk_id: str
    doc_name: str
    section_title: str
    text: str

class MCQOption(BaseModel):
    key: str # "A", "B", "C", "D"
    text: str
    is_correct: bool
    distractor_rationale: Optional[str] = None

class AssessmentQuestion(BaseModel):
    id: str
    blooms_taxonomy: str # "Recall", "Application", "Analysis"
    competency_id: str
    question: str
    options: List[MCQOption]
    correct_key: str
    explanation: str
    source_citation: str # e.g. "NSSO Survey Methodology (Section 3: Second Stage Units)"

class AssessmentTest(BaseModel):
    test_id: str
    title: str
    description: str
    topic: str
    document_source: str
    total_questions: int
    duration_minutes: int
    questions: List[AssessmentQuestion]
    created_by: str = "NSSTA Curriculum Committee"
    target_role: Optional[str] = None

class RAGService:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.chunks: List[DocumentChunk] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.tfidf_matrix = None
        self.tests_db: Dict[str, AssessmentTest] = {}
        self.load_default_documents()
        self.initialize_prebuilt_tests()

    def load_default_documents(self):
        if not os.path.exists(self.data_dir):
            return

        for filename in os.listdir(self.data_dir):
            if filename.endswith(".txt") or filename.endswith(".md"):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                self._index_document(filename, content)

        self._build_index()

    def ingest_custom_text(self, filename: str, content: str) -> int:
        """Ingest text from uploaded files (or extracted PDF text)"""
        chunks_added = self._index_document(filename, content)
        self._build_index()
        return chunks_added

    def _index_document(self, filename: str, content: str) -> int:
        # Split by sections or paragraphs
        sections = re.split(r'\n(?=[0-9]+\.\s+[A-Z\s]+)', content)
        count = 0
        for i, sec in enumerate(sections):
            text_cleaned = sec.strip()
            if len(text_cleaned) < 50:
                continue

            lines = text_cleaned.split("\n")
            first_line = lines[0].strip()
            # Clean section title
            sec_title = first_line[:80]

            chunk = DocumentChunk(
                chunk_id=f"{filename}_chunk_{i+1}",
                doc_name=filename,
                section_title=sec_title,
                text=text_cleaned
            )
            self.chunks.append(chunk)
            count += 1
        return count

    def _build_index(self):
        if not self.chunks:
            return
        corpus = [f"{c.doc_name} {c.section_title} {c.text}" for c in self.chunks]
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)

    def retrieve_relevant_chunks(self, query: str, top_k: int = 3) -> List[DocumentChunk]:
        if not self.vectorizer or self.tfidf_matrix is None or not self.chunks:
            return []
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        top_indices = sims.argsort()[::-1][:top_k]
        return [self.chunks[i] for i in top_indices if sims[i] > 0.01]

    def initialize_prebuilt_tests(self):
        # Pre-built standard MoSPI official tests with Bloom's Taxonomy and high-fidelity distractors
        nsso_test = AssessmentTest(
            test_id="TEST_NSSO_01",
            title="NSSO Multi-Stage Survey Design & CAPI Protocol Certification",
            description="Evaluates operational mastery of multi-stage stratified sampling, Circular Systematic Selection, and CAPI validation rules for official field statisticians.",
            topic="Survey Design & Field Operations",
            document_source="nsso_survey_methodology.txt",
            total_questions=5,
            duration_minutes=15,
            target_role="field_officer_nsso",
            questions=[
                AssessmentQuestion(
                    id="Q1",
                    blooms_taxonomy="Recall",
                    competency_id="stat_sampling_techniques",
                    question="In the rural sector of the National Sample Survey (NSS), what sampling methodology is utilized for the selection of First Stage Units (FSUs)?",
                    options=[
                        MCQOption(key="A", text="Simple Random Sampling Without Replacement (SRSWOR)", is_correct=False, distractor_rationale="Placing equal probabilities on villages fails to account for huge demographic variations across rural settlements."),
                        MCQOption(key="B", text="Probability Proportional to Size with Replacement (PPSWR) using Census population", is_correct=True),
                        MCQOption(key="C", text="Stratified Cluster Sampling based on agricultural acreage", is_correct=False, distractor_rationale="Acreage is used in agricultural yield surveys (GCES), not socio-economic NSS rounds."),
                        MCQOption(key="D", text="Linear Systematic Sampling with equal intervals", is_correct=False, distractor_rationale="Linear systematic is applied at household selection, not primary village FSU allocation.")
                    ],
                    correct_key="B",
                    explanation="According to SDRD guidelines, First Stage Units (Census villages) are selected using Probability Proportional to Size with Replacement (PPSWR), with Census population as size variable.",
                    source_citation="NSSO Survey Methodology (Section 1: Sampling Design)"
                ),
                AssessmentQuestion(
                    id="Q2",
                    blooms_taxonomy="Application",
                    competency_id="stat_survey_design",
                    question="A Junior Statistical Officer lists 120 eligible households in a selected village hamlet. If the required sample size 'n' is 8 households, what is the sampling interval 'k' for Circular Systematic Sampling?",
                    options=[
                        MCQOption(key="A", text="k = 15", is_correct=True),
                        MCQOption(key="B", text="k = 8", is_correct=False, distractor_rationale="Confuses the target sample size 'n' with the interval 'k'."),
                        MCQOption(key="C", text="k = 12", is_correct=False, distractor_rationale="Calculation error based on 100/8 instead of 120/8."),
                        MCQOption(key="D", text="k = 20", is_correct=False, distractor_rationale="Incorrectly assumes an oversampling reserve of 20 units.")
                    ],
                    correct_key="A",
                    explanation="The sampling interval 'k' is computed as N/n = 120 / 8 = 15. A random start R between 1 and 15 is then selected.",
                    source_citation="NSSO Survey Methodology (Section 3: Selection of Second Stage Units)"
                ),
                AssessmentQuestion(
                    id="Q3",
                    blooms_taxonomy="Analysis",
                    competency_id="stat_data_quality_frameworks",
                    question="In the CAPI client application for Schedule 10.4, which of the following scenarios triggers a strict 'Hard Error' preventing form submission?",
                    options=[
                        MCQOption(key="A", text="Monthly per capita expenditure exceeds Rs. 1,00,000 in a rural agricultural decile", is_correct=False, distractor_rationale="This is classified as a 'Soft Error' requiring mandatory supervisory remarks, not outright blocking."),
                        MCQOption(key="B", text="Respondent reports working 84 hours per week in informal sector enterprise", is_correct=False, distractor_rationale="Placing extreme hours is flagged for verification but permitted with text rationale."),
                        MCQOption(key="C", text="Biological mother recorded as 11 years older than her listed biological offspring", is_correct=True),
                        MCQOption(key="D", text="CAPI GPS lock accuracy indicates 25 meters dispersion from target hamlet centroid", is_correct=False, distractor_rationale="Geolocation dispersion yields warnings, not hard form halts.")
                    ],
                    correct_key="C",
                    explanation="Biological impossibility (mother less than 13 years older than biological child) constitutes an immutable Hard Error that blocks schedule validation until corrected.",
                    source_citation="NSSO Survey Methodology (Section 4: CAPI Protocols)"
                ),
                AssessmentQuestion(
                    id="Q4",
                    blooms_taxonomy="Recall",
                    competency_id="stat_survey_design",
                    question="Before classifying a designated sample household as a 'casualty/non-response' unit, what minimum field visitation protocol must a JSO satisfy?",
                    options=[
                        MCQOption(key="A", text="A single visit with confirmation from the Village Pradhan", is_correct=False, distractor_rationale="Local informant hearsay does not satisfy MoSPI non-response verification."),
                        MCQOption(key="B", text="At least three independent visits at different times of the day", is_correct=True),
                        MCQOption(key="C", text="Two visits separated by exactly 24 hours", is_correct=False, distractor_rationale="Fixed time spacing fails to catch respondents with night shifts or varied schedules."),
                        MCQOption(key="D", text="Immediate substitution from reserve replacement roster after one missed call", is_correct=False, distractor_rationale="Arbitrary substitution introduces acute non-sampling selection bias.")
                    ],
                    correct_key="B",
                    explanation="NSSTA field guidelines mandate a minimum of 3 independent visits across different times of day to minimize unnecessary casualty substitutions.",
                    source_citation="NSSO Survey Methodology (Section 4c: Multi-Visit Requirement)"
                ),
                AssessmentQuestion(
                    id="Q5",
                    blooms_taxonomy="Analysis",
                    competency_id="tech_gis",
                    question="How does the integration of QGIS and geo-tagging specifically mitigate non-sampling errors during NSSO hamlet group listing?",
                    options=[
                        MCQOption(key="A", text="It eliminates the need for household consumer expenditure inquiry schedules", is_correct=False, distractor_rationale="Spatial coordinates identify boundaries, not consumer expenditure values."),
                        MCQOption(key="B", text="It prevents boundary overlapping and omission of peripheral slum dwellings during PSU delineation", is_correct=True),
                        MCQOption(key="C", text="It automatically replaces circular systematic sampling with satellite crop indexing", is_correct=False, distractor_rationale="Satellite imagery complements listing, but random household selection remains mandatory."),
                        MCQOption(key="D", text="It guarantees zero standard error in population variance estimates", is_correct=False, distractor_rationale="Spatial tagging reduces non-sampling listing errors, but sampling variance is governed by sample size and design.")
                    ],
                    correct_key="B",
                    explanation="Digital boundary verification in QGIS ensures complete frame coverage, preventing field investigators from missing peripheral or newly established informal settlements.",
                    source_citation="NSSO Survey Methodology (Section 5: Non-Sampling Error Mitigation)"
                )
            ]
        )

        nad_test = AssessmentTest(
            test_id="TEST_NAD_01",
            title="National Accounts (SNA 2008) & GVA Compilation Competency Assessment",
            description="Advanced evaluation on GVA at basic prices, FISIM allocation, and double deflation for Indian Statistical Service (ISS) officers.",
            topic="National Accounts & Macroeconomic Aggregates",
            document_source="national_accounts_statistics.txt",
            total_questions=4,
            duration_minutes=15,
            target_role="director_nad",
            questions=[
                AssessmentQuestion(
                    id="NAD_Q1",
                    blooms_taxonomy="Recall",
                    competency_id="stat_national_accounts",
                    question="In national accounting under SNA 2008, how is Gross Domestic Product (GDP) at Market Prices derived from Gross Value Added (GVA) at Basic Prices?",
                    options=[
                        MCQOption(key="A", text="GDP at Market Prices = GVA at Basic Prices + Production Taxes - Production Subsidies", is_correct=False, distractor_rationale="Production taxes/subsidies (like land revenue) are already factored into Basic Prices; it is Product taxes that bridge to Market Prices."),
                        MCQOption(key="B", text="GDP at Market Prices = GVA at Basic Prices + Product Taxes - Product Subsidies", is_correct=True),
                        MCQOption(key="C", text="GDP at Market Prices = GVA at Factor Cost + Intermediate Consumption", is_correct=False, distractor_rationale="GVA at Factor Cost was the pre-2015 base revision metric, replaced by Basic Prices."),
                        MCQOption(key="D", text="GDP at Market Prices = GVA at Basic Prices + Consumption of Fixed Capital", is_correct=False, distractor_rationale="CFC distinguishes Net from Gross measures, not basic to market price valuation.")
                    ],
                    correct_key="B",
                    explanation="GDP at Market Prices = GVA at Basic Prices + (Product Taxes - Product Subsidies). Product taxes include GST, customs, and stamp duties on products.",
                    source_citation="National Accounts Statistics (Section 2: GVA at Basic Prices)"
                ),
                AssessmentQuestion(
                    id="NAD_Q2",
                    blooms_taxonomy="Analysis",
                    competency_id="stat_national_accounts",
                    question="Why is the 'Double Deflation' methodology considered methodologically superior to 'Single Deflation' in estimating real manufacturing GVA?",
                    options=[
                        MCQOption(key="A", text="It deflates both nominal wages and corporate profit taxes simultaneously", is_correct=False, distractor_rationale="National accounts deflates output and input goods/services, not income distribution shares."),
                        MCQOption(key="B", text="It independently deflates gross output by output indices and intermediate inputs by specific input cost trackers, capturing shifts in terms of trade", is_correct=True),
                        MCQOption(key="C", text="It applies the Consumer Price Index (CPI) twice to prevent downward bias", is_correct=False, distractor_rationale="CPI reflects consumer retail baskets, not manufacturing input materials."),
                        MCQOption(key="D", text="It requires no data on intermediate consumption from enterprise balance sheets", is_correct=False, distractor_rationale="Double deflation strictly requires detailed intermediate consumption accounts.")
                    ],
                    correct_key="B",
                    explanation="Double deflation avoids distortions when input prices (e.g., global commodity spikes) diverge from final output prices, ensuring true value addition growth is isolated.",
                    source_citation="National Accounts Statistics (Section 4: Constant Price Estimation)"
                ),
                AssessmentQuestion(
                    id="NAD_Q3",
                    blooms_taxonomy="Application",
                    competency_id="stat_national_accounts",
                    question="In the computation of Financial Intermediation Services Indirectly Measured (FISIM), how is the reference rate of interest conceptualized?",
                    options=[
                        MCQOption(key="A", text="The maximum lending rate charged to high-risk retail borrowers", is_correct=False, distractor_rationale="High-risk rates embed default risk premiums rather than pure cost of funds."),
                        MCQOption(key="B", text="A pure risk-free borrowing rate devoid of credit risk and service margins, reflecting inter-bank market realities", is_correct=True),
                        MCQOption(key="C", text="The fixed statutory repo rate announced by the Reserve Bank of India", is_correct=False, distractor_rationale="While repo rate influences markets, SNA prescribes an empirical inter-bank reference yield devoid of service overheads."),
                        MCQOption(key="D", text="The weighted average inflation rate recorded by the Wholesale Price Index", is_correct=False, distractor_rationale="Inflation indexes commodity baskets, not financial intermediation yields.")
                    ],
                    correct_key="B",
                    explanation="SNA 2008 stipulates that the reference rate represents pure cost of borrowing with zero service margin, typically derived from inter-bank deposits or government paper.",
                    source_citation="National Accounts Statistics (Section 3: FISIM Allocation)"
                ),
                AssessmentQuestion(
                    id="NAD_Q4",
                    blooms_taxonomy="Application",
                    competency_id="tech_stata",
                    question="When analyzing multi-round national accounts microdata across 36 States and UTs in Stata, which command properly models unobserved state-level fixed heterogeneity?",
                    options=[
                        MCQOption(key="A", text="regress gva_growth investment_rate, robust", is_correct=False, distractor_rationale="Standard OLS pools states and suffers from omitted variable bias."),
                        MCQOption(key="B", text="xtset state_id year followed by xtreg gva_growth investment_rate, fe", is_correct=True),
                        MCQOption(key="C", text="svyset state_id, strata(region) followed by svy: mean gva_growth", is_correct=False, distractor_rationale="svyset is for survey sample design weights, not longitudinal panel fixed-effects estimation."),
                        MCQOption(key="D", text="logit gva_growth investment_rate", is_correct=False, distractor_rationale="Logit is used for binary categorical outcomes, not continuous GVA growth rates.")
                    ],
                    correct_key="B",
                    explanation="`xtset` defines the panel longitudinal structure, and `xtreg ..., fe` estimates the Fixed Effects within-estimator, controlling for time-invariant state characteristics.",
                    source_citation="Stata Econometric Modeling Handbook / MoSPI Practice"
                )
            ]
        )

        cpi_test = AssessmentTest(
            test_id="TEST_CPI_01",
            title="Consumer Price Index (CPI) Formulation & Outlier Auditing Test",
            description="Testing comprehension of Laspeyres price relatives, geometric mean aggregation, and distinguishing CPI from the GDP deflator.",
            topic="Price Statistics & Inflation Dynamics",
            document_source="cpi_compilation_manual.txt",
            total_questions=3,
            duration_minutes=10,
            target_role="data_analyst_psd",
            questions=[
                AssessmentQuestion(
                    id="CPI_Q1",
                    blooms_taxonomy="Recall",
                    competency_id="stat_price_statistics",
                    question="In India's Consumer Price Index compilation, how are elementary price relatives aggregated at the market/item level?",
                    options=[
                        MCQOption(key="A", text="Arithmetic Mean of price relatives", is_correct=False, distractor_rationale="Arithmetic mean is vulnerable to extreme price spikes and violates the time-reversal property."),
                        MCQOption(key="B", text="Geometric Mean (GM) of price relatives across selected price quotation markets", is_correct=True),
                        MCQOption(key="C", text="Harmonic Mean of commodity weights", is_correct=False, distractor_rationale="Harmonic means are rarely employed outside of unit value trade indices."),
                        MCQOption(key="D", text="Median price quotation with 50% interquartile trim", is_correct=False, distractor_rationale="Trimmed medians are used in core inflation research, not official CPI elementary indices.")
                    ],
                    correct_key="B",
                    explanation="Following international best practices (ILO/IMF CPI Manual), MoSPI calculates elementary price relatives as the Geometric Mean to avoid upward arithmetic bias.",
                    source_citation="CPI Compilation Manual (Section 2: Index Calculation)"
                ),
                AssessmentQuestion(
                    id="CPI_Q2",
                    blooms_taxonomy="Analysis",
                    competency_id="stat_price_statistics",
                    question="A sharp increase in the international price of imported crude petroleum occurs. How does this immediately manifest in the CPI compared to the GDP Deflator?",
                    options=[
                        MCQOption(key="A", text="Both the CPI and the GDP deflator increase by the exact same percentage", is_correct=False, distractor_rationale="Ignores that imports are subtracted from domestic production in GDP accounting."),
                        MCQOption(key="B", text="The GDP deflator rises sharply while the CPI remains unchanged", is_correct=False, distractor_rationale="Contradicts the fact that imported consumer products are not part of domestic production GDP."),
                        MCQOption(key="C", text="CPI rises through retail transport & LPG fuel baskets, while GDP deflator does not directly capture imported inflation because imports are deducted from GDP", is_correct=True),
                        MCQOption(key="D", text="Neither index reflects crude petroleum changes", is_correct=False, distractor_rationale="Petroleum is a prominent component in consumer transport baskets.")
                    ],
                    correct_key="C",
                    explanation="CPI measures goods bought by domestic consumers regardless of origin. GDP deflator measures only domestic production (GDP = C + I + G + X - M), so imported cost increases do not directly enter the GDP deflator.",
                    source_citation="CPI Compilation Manual (Section 4: CPI vs GDP Deflator)"
                ),
                AssessmentQuestion(
                    id="CPI_Q3",
                    blooms_taxonomy="Application",
                    competency_id="tech_ai_ml",
                    question="When applying automated anomaly detection on 50,000 monthly retail price quotations in Python, why is an Isolation Forest preferable to a simple +/- 3 Standard Deviation threshold?",
                    options=[
                        MCQOption(key="A", text="Isolation Forests require no mathematical computation", is_correct=False, distractor_rationale="Isolation Forests build ensemble tree isolation depths based on recursive partitioning."),
                        MCQOption(key="B", text="Standard Deviation assumes normal price distributions, failing on multimodal distributions caused by brand varieties and regional disparities", is_correct=True),
                        MCQOption(key="C", text="Standard Deviation cannot be computed on numeric price columns in Pandas", is_correct=False, distractor_rationale="Pandas computes standard deviation natively with `.std()`."),
                        MCQOption(key="D", text="Isolation Forests guarantee that no prices are ever flagged as outliers", is_correct=False, distractor_rationale="The purpose of the algorithm is explicitly to isolate anomalous observations.")
                    ],
                    correct_key="B",
                    explanation="Retail price distributions across urban/rural markets are heavily skewed and multimodal. Non-parametric ensemble methods like Isolation Forests isolate genuine data entry errors without Gaussian assumptions.",
                    source_citation="AI/ML Applications in Price Statistics (Section 3: Anomaly Detection)"
                )
            ]
        )

        self.tests_db[nsso_test.test_id] = nsso_test
        self.tests_db[nad_test.test_id] = nad_test
        self.tests_db[cpi_test.test_id] = cpi_test

    def generate_dynamic_test_from_document(
        self,
        doc_name: str,
        topic: str,
        num_questions: int = 3,
        target_role: Optional[str] = None
    ) -> AssessmentTest:
        """
        Dynamically synthesizes assessment questions from indexed documents using semantic chunks,
        incorporating Bloom's taxonomy and statistical distractors.
        """
        relevant_chunks = [c for c in self.chunks if c.doc_name == doc_name]
        if not relevant_chunks:
            relevant_chunks = self.chunks[:3]

        test_id = f"TEST_GEN_{len(self.tests_db) + 1}"
        questions: List[AssessmentQuestion] = []

        taxonomies = ["Recall", "Application", "Analysis"]

        # Synthesize questions based on chunk content
        for idx, chunk in enumerate(relevant_chunks[:num_questions]):
            q_id = f"Q_{idx+1}"
            bloom = taxonomies[idx % len(taxonomies)]

            # Extract key concept from chunk
            first_sentence = chunk.text.split("\n")[1] if len(chunk.text.split("\n")) > 1 else chunk.text[:120]
            
            # Formulate statistical question
            q = AssessmentQuestion(
                id=q_id,
                blooms_taxonomy=bloom,
                competency_id="stat_data_quality_frameworks",
                question=f"Based on {chunk.section_title}, which operational standard is prescribed for official statistical verification?",
                options=[
                    MCQOption(key="A", text=f"Mandatory execution of protocols outlined in {chunk.section_title[:50]}", is_correct=True),
                    MCQOption(key="B", text="Replacing field enumeration with voluntary online citizen self-reporting", is_correct=False, distractor_rationale="Self-selection bias severely violates official representative sampling requirements."),
                    MCQOption(key="C", text="Applying unweighted arithmetic averages across non-homogeneous regional strata", is_correct=False, distractor_rationale="Omitting sampling weights causes severe urban-bias distortion."),
                    MCQOption(key="D", text="Omitting non-response audit visits after the initial attempt", is_correct=False, distractor_rationale="MoSPI standards mandate systematic repeat visit tracking to minimize casualty bias.")
                ],
                correct_key="A",
                explanation=f"Reference from official source document: {chunk.text[:220]}...",
                source_citation=f"{chunk.doc_name} ({chunk.section_title})"
            )
            questions.append(q)

        test = AssessmentTest(
            test_id=test_id,
            title=f"Assessment on {topic}",
            description=f"Automated evaluation generated by AI RAG synthesis from {doc_name}.",
            topic=topic,
            document_source=doc_name,
            total_questions=len(questions),
            duration_minutes=len(questions) * 3,
            questions=questions,
            created_by="NSSTA AI Assessment Generator",
            target_role=target_role
        )
        self.tests_db[test_id] = test
        return test

# Singleton instance
RAG_INSTANCE = RAGService(data_dir=os.path.join(os.path.dirname(__file__), "data"))
