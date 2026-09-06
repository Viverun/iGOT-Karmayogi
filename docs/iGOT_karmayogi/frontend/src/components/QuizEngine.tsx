import React, { useState, useEffect } from 'react';
import {
  AssessmentTest,
  AssessmentQuestion,
  TestSubmissionResult,
  OfficerProfile,
  api
} from '../api';
import {
  Sparkles,
  BookOpen,
  CheckCircle2,
  XCircle,
  Clock,
  Award,
  Upload,
  Layers,
  FileText,
  AlertCircle,
  HelpCircle,
  Check,
  RotateCcw,
  ArrowRight,
  TrendingUp,
  ShieldCheck,
  Send
} from 'lucide-react';

interface QuizEngineProps {
  currentOfficer: OfficerProfile;
  onRefreshOfficer: () => Promise<void>;
}

export const QuizEngine: React.FC<QuizEngineProps> = ({
  currentOfficer,
  onRefreshOfficer
}) => {
  const [tests, setTests] = useState<AssessmentTest[]>([]);
  const [selectedTestId, setSelectedTestId] = useState<string | null>(null);
  const [activeTest, setActiveTest] = useState<AssessmentTest | null>(null);
  const [userAnswers, setUserAnswers] = useState<Record<string, string>>({});
  const [submissionResult, setSubmissionResult] = useState<TestSubmissionResult | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);

  // Trainer Enablement Tool States
  const [isTrainerMode, setIsTrainerMode] = useState(false);
  const [generateTopic, setGenerateTopic] = useState('Survey Sampling & Quality Controls');
  const [selectedDocSource, setSelectedDocSource] = useState('nsso_survey_methodology.txt');
  const [generating, setGenerating] = useState(false);
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [notification, setNotification] = useState<string | null>(null);

  useEffect(() => {
    loadTests();
  }, []);

  const loadTests = async () => {
    try {
      setLoading(true);
      const data = await api.getAssessments();
      setTests(data);
      if (data.length > 0 && !selectedTestId) {
        handleSelectTest(data[0].test_id);
      }
    } catch (err) {
      console.error('Failed to load tests', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTest = async (testId: string) => {
    try {
      setSelectedTestId(testId);
      setSubmissionResult(null);
      setUserAnswers({});
      const fullTest = await api.getAssessment(testId);
      setActiveTest(fullTest);
    } catch (err) {
      console.error('Failed to load full test', err);
    }
  };

  const handleOptionSelect = (questionId: string, optionKey: string) => {
    if (submissionResult) return; // Prevent changing after submission
    setUserAnswers((prev) => ({ ...prev, [questionId]: optionKey }));
  };

  const handleSubmitQuiz = async () => {
    if (!activeTest || !selectedTestId) return;
    try {
      setSubmitting(true);
      const res = await api.submitAssessment(
        selectedTestId,
        currentOfficer.officer_id,
        userAnswers
      );
      setSubmissionResult(res);
      await onRefreshOfficer(); // Refresh profile so radar/gap updates live!
    } catch (err) {
      console.error('Failed to submit test', err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleGenerateTest = async () => {
    try {
      setGenerating(true);
      const newTest = await api.generateAssessment(
        selectedDocSource,
        generateTopic,
        3,
        currentOfficer.role_id
      );
      setNotification(`Created new AI Assessment: "${newTest.title}"`);
      await loadTests();
      handleSelectTest(newTest.test_id);
      setIsTrainerMode(false);
    } catch (err) {
      console.error('Failed to generate test', err);
    } finally {
      setGenerating(false);
    }
  };

  const handleFileUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return;
    try {
      setUploading(true);
      const formData = new FormData();
      formData.append('file', uploadFile);
      formData.append('topic', generateTopic);
      const res = await api.uploadDocument(formData);
      setNotification(res.message);
      setUploadFile(null);
      await loadTests();
      handleSelectTest(res.generated_test_id);
      setIsTrainerMode(false);
    } catch (err) {
      console.error('Upload failed', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-[11px] font-bold uppercase tracking-widest bg-purple-100 text-purple-800 px-2 py-0.5 rounded border border-purple-200">
              Bloom's Taxonomy • Statistical RAG
            </span>
            <span className="text-xs text-slate-500 font-medium">
              MoSPI Assessment Engine (PS 26101)
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-900">
            AI-Powered Assessment & Distractor Verification Studio
          </h2>
          <p className="text-xs text-slate-600 mt-1">
            Contextual quizzes synthesized from official MoSPI manuals (NSSO, NAD, CPI) with calibrated statistical distractors and instant score accreditation.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsTrainerMode(!isTrainerMode)}
            className={`flex items-center gap-2 px-3.5 py-2.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
              isTrainerMode
                ? 'bg-purple-700 text-white shadow-xs'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-800 border border-slate-300'
            }`}
          >
            <Sparkles className="w-4 h-4 text-amber-300" />
            <span>{isTrainerMode ? 'Exit Trainer Studio' : 'Open Trainer Enablement Studio'}</span>
          </button>
        </div>
      </div>

      {notification && (
        <div className="bg-emerald-50 border border-emerald-200 text-emerald-900 text-xs px-4 py-3 rounded-lg flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>{notification}</span>
          </div>
          <button onClick={() => setNotification(null)} className="text-emerald-700 font-bold hover:underline">
            ✕
          </button>
        </div>
      )}

      {/* Trainer Enablement Studio Drawer */}
      {isTrainerMode && (
        <div className="bg-gradient-to-br from-purple-50/70 to-indigo-50/50 rounded-xl border border-purple-200 p-6 shadow-xs animate-in fade-in">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-purple-950 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-purple-600" />
                NSSTA / MoSPI Trainer Test Synthesis Console
              </h3>
              <p className="text-xs text-purple-700 mt-0.5">
                Generate new official quizzes on-the-fly by parsing guideline PDFs or existing statistical manuals.
              </p>
            </div>
            <span className="text-[11px] bg-purple-200/60 text-purple-900 px-2 py-0.5 rounded font-bold">
              Instructor Mode
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Form 1: Generate from preloaded MoSPI manual */}
            <div className="bg-white rounded-xl p-4 border border-purple-200 shadow-xs">
              <h4 className="text-xs font-bold text-slate-900 mb-2 flex items-center gap-1.5">
                <FileText className="w-4 h-4 text-blue-600" />
                Option A: Synthesize from Preloaded MoSPI Repository
              </h4>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="block text-slate-600 font-medium mb-1">Select Source Document</label>
                  <select
                    value={selectedDocSource}
                    onChange={(e) => setSelectedDocSource(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-xs text-slate-800"
                  >
                    <option value="nsso_survey_methodology.txt">NSSO 78th Round Survey Design & CAPI Protocol</option>
                    <option value="national_accounts_statistics.txt">National Accounts Statistics (GVA & SNA 2008)</option>
                    <option value="cpi_compilation_manual.txt">Price Statistics Division - CPI Compilation SOP</option>
                  </select>
                </div>

                <div>
                  <label className="block text-slate-600 font-medium mb-1">Assessment Topic Label</label>
                  <input
                    type="text"
                    value={generateTopic}
                    onChange={(e) => setGenerateTopic(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-300 rounded-lg p-2 text-xs text-slate-800"
                    placeholder="e.g. Sampling Weights & Variance Estimation"
                  />
                </div>

                <button
                  onClick={handleGenerateTest}
                  disabled={generating}
                  className="w-full mt-2 bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
                >
                  {generating ? (
                    <>
                      <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Extracting Chunks & Synthesizing MCQs...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-3.5 h-3.5 text-amber-300" />
                      <span>Auto-Generate Assessment with Distractors</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Form 2: Ingest Custom PDF/TXT Document */}
            <form onSubmit={handleFileUpload} className="bg-white rounded-xl p-4 border border-purple-200 shadow-xs">
              <h4 className="text-xs font-bold text-slate-900 mb-2 flex items-center gap-1.5">
                <Upload className="w-4 h-4 text-emerald-600" />
                Option B: Upload New Guideline Document (PDF / TXT)
              </h4>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="block text-slate-600 font-medium mb-1">Select File from System</label>
                  <input
                    type="file"
                    accept=".pdf,.txt,.md"
                    onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                    className="w-full text-xs text-slate-600 file:mr-3 file:py-1.5 file:px-3 file:rounded-md file:border-0 file:text-xs file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
                  />
                </div>

                <p className="text-[11px] text-slate-500">
                  Parses document layout, splits into semantic vectors, and applies Bloom's taxonomy prompting to output questions with citations.
                </p>

                <button
                  type="submit"
                  disabled={!uploadFile || uploading}
                  className="w-full mt-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-2 px-4 rounded-lg text-xs transition-colors flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
                >
                  {uploading ? (
                    <>
                      <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                      <span>Ingesting & Indexing Document...</span>
                    </>
                  ) : (
                    <>
                      <Upload className="w-3.5 h-3.5" />
                      <span>Ingest Document & Deploy Test</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Main Assessment Grid: Test Selector + Question Taker */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Test Selector List */}
        <div className="lg:col-span-4 space-y-3">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider px-1">
            Available Assessment Modules ({tests.length})
          </h3>

          <div className="space-y-2">
            {tests.map((t) => {
              const isSelected = selectedTestId === t.test_id;
              return (
                <div
                  key={t.test_id}
                  onClick={() => handleSelectTest(t.test_id)}
                  className={`p-4 rounded-xl border cursor-pointer transition-all ${
                    isSelected
                      ? 'border-blue-600 bg-blue-50/60 shadow-xs'
                      : 'border-slate-200 bg-white hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <span className="text-[10px] font-bold text-blue-700 bg-blue-100/70 px-2 py-0.5 rounded font-mono">
                      {t.test_id}
                    </span>
                    <span className="text-[11px] text-slate-500 flex items-center gap-1 font-medium">
                      <Clock className="w-3 h-3" /> {t.duration_minutes} Mins
                    </span>
                  </div>

                  <h4 className="text-xs font-bold text-slate-900 leading-snug mb-1">
                    {t.title}
                  </h4>

                  <p className="text-[11px] text-slate-500 line-clamp-2 mb-2">
                    {t.description}
                  </p>

                  <div className="flex items-center justify-between text-[11px] text-slate-600 border-t border-slate-100 pt-2">
                    <span>{t.total_questions} Questions</span>
                    <span className="font-semibold text-purple-700">{t.created_by}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Test Taking / Results View */}
        <div className="lg:col-span-8 bg-white rounded-xl border border-slate-200 p-6 shadow-xs">
          {activeTest ? (
            <div>
              {/* Test Header */}
              <div className="border-b border-slate-200 pb-4 mb-6">
                <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
                  <span className="text-xs font-bold text-purple-700 bg-purple-50 px-2.5 py-0.5 rounded border border-purple-200">
                    Topic: {activeTest.topic}
                  </span>
                  <div className="flex items-center gap-3 text-xs text-slate-500 font-medium">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      {activeTest.duration_minutes} Minutes Allocated
                    </span>
                    <span>•</span>
                    <span>Source: <code className="text-slate-700">{activeTest.document_source}</code></span>
                  </div>
                </div>

                <h3 className="text-base font-bold text-slate-900 mt-2">
                  {activeTest.title}
                </h3>
                <p className="text-xs text-slate-600 mt-1">
                  {activeTest.description}
                </p>
              </div>

              {/* Submission Score Banner */}
              {submissionResult && (
                <div
                  className={`p-5 rounded-xl border mb-6 ${
                    submissionResult.passed
                      ? 'bg-emerald-50 border-emerald-300 text-emerald-950'
                      : 'bg-rose-50 border-rose-300 text-rose-950'
                  }`}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      {submissionResult.passed ? (
                        <div className="w-12 h-12 rounded-full bg-emerald-600 text-white flex items-center justify-center font-extrabold text-xl shadow-xs shrink-0">
                          ✓
                        </div>
                      ) : (
                        <div className="w-12 h-12 rounded-full bg-rose-600 text-white flex items-center justify-center font-extrabold text-xl shadow-xs shrink-0">
                          ✕
                        </div>
                      )}
                      <div>
                        <div className="text-sm font-bold">
                          {submissionResult.passed
                            ? 'Assessment Cleared! Competency Score Upgraded'
                            : 'Assessment Needs Improvement (Below 60%)'}
                        </div>
                        <div className="text-xs mt-0.5 text-slate-700">
                          Scored <span className="font-extrabold">{submissionResult.score_percentage}%</span> (
                          {submissionResult.correct_answers} of {submissionResult.total_questions} correct)
                        </div>
                      </div>
                    </div>

                    {submissionResult.passed && Object.keys(submissionResult.competency_upgrades).length > 0 && (
                      <div className="bg-white/80 backdrop-blur-xs p-2.5 rounded-lg border border-emerald-300 text-xs">
                        <div className="text-[10px] font-bold uppercase text-emerald-800">
                          Profile Competencies Enhanced:
                        </div>
                        <div className="font-semibold text-slate-900 mt-0.5">
                          {Object.entries(submissionResult.competency_upgrades).map(([k, v]) => (
                            <span key={k} className="mr-2">
                              {k}: <span className="text-emerald-700 font-bold">{v} pts (+4)</span>
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Question List */}
              <div className="space-y-8">
                {activeTest.questions?.map((q, qIndex) => {
                  const userAns = userAnswers[q.id];
                  const feedbackItem = submissionResult?.feedback.find(f => f.question_id === q.id);

                  return (
                    <div
                      key={q.id}
                      className="p-5 rounded-xl border border-slate-200 bg-slate-50/40 space-y-4"
                    >
                      {/* Question meta */}
                      <div className="flex items-center justify-between text-xs">
                        <span className="font-bold text-slate-800">
                          Question {qIndex + 1} of {activeTest.total_questions}
                        </span>
                        <div className="flex items-center gap-2">
                          <span
                            className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                              q.blooms_taxonomy === 'Recall'
                                ? 'bg-blue-100 text-blue-800 border-blue-200'
                                : q.blooms_taxonomy === 'Application'
                                ? 'bg-amber-100 text-amber-800 border-amber-200'
                                : 'bg-purple-100 text-purple-800 border-purple-200'
                            }`}
                          >
                            Bloom's: {q.blooms_taxonomy}
                          </span>
                          <span className="text-[10px] text-slate-400 font-mono">
                            {q.competency_id}
                          </span>
                        </div>
                      </div>

                      {/* Question Stem */}
                      <p className="text-sm font-semibold text-slate-900 leading-relaxed">
                        {q.question}
                      </p>

                      {/* 4 Options */}
                      <div className="space-y-2">
                        {q.options.map((opt) => {
                          const isSelected = userAns === opt.key;
                          let optionStyle = 'border-slate-200 bg-white hover:bg-slate-50 text-slate-800';

                          if (submissionResult) {
                            if (opt.is_correct) {
                              optionStyle = 'border-emerald-500 bg-emerald-50 text-emerald-950 font-semibold';
                            } else if (isSelected && !opt.is_correct) {
                              optionStyle = 'border-rose-500 bg-rose-50 text-rose-950';
                            }
                          } else if (isSelected) {
                            optionStyle = 'border-blue-600 bg-blue-50 text-blue-950 font-medium shadow-2xs';
                          }

                          return (
                            <div
                              key={opt.key}
                              onClick={() => handleOptionSelect(q.id, opt.key)}
                              className={`p-3 rounded-lg border text-xs cursor-pointer transition-colors flex items-start gap-3 ${optionStyle}`}
                            >
                              <span
                                className={`w-5 h-5 rounded-full border flex items-center justify-center font-bold text-[11px] shrink-0 mt-0.5 ${
                                  isSelected
                                    ? 'bg-blue-600 border-blue-600 text-white'
                                    : 'border-slate-300 bg-slate-100 text-slate-600'
                                }`}
                              >
                                {opt.key}
                              </span>
                              <div className="flex-1">
                                <span>{opt.text}</span>
                              </div>
                            </div>
                          );
                        })}
                      </div>

                      {/* Feedback & Distractor Rationale (Shown after submission) */}
                      {feedbackItem && (
                        <div className="mt-4 pt-3 border-t border-slate-200 text-xs space-y-2">
                          <div className="flex items-center gap-1.5 font-bold">
                            {feedbackItem.is_correct ? (
                              <span className="text-emerald-700 flex items-center gap-1">
                                <CheckCircle2 className="w-4 h-4" /> Correct Answer: Option {feedbackItem.correct_answer}
                              </span>
                            ) : (
                              <span className="text-rose-700 flex items-center gap-1">
                                <XCircle className="w-4 h-4" /> Incorrect. Correct Answer: Option {feedbackItem.correct_answer}
                              </span>
                            )}
                          </div>

                          <div className="bg-slate-100 rounded-lg p-3 text-slate-700 leading-relaxed">
                            <span className="font-bold text-slate-900 block mb-0.5">Explanation:</span>
                            {feedbackItem.explanation}
                          </div>

                          {feedbackItem.distractor_rationale && (
                            <div className="bg-amber-50/80 border border-amber-200 rounded-lg p-2.5 text-amber-900">
                              <span className="font-bold text-amber-950 block mb-0.5">Distractor Flaw Analysis:</span>
                              {feedbackItem.distractor_rationale}
                            </div>
                          )}

                          <div className="text-[11px] text-slate-500 italic flex items-center gap-1">
                            <BookOpen className="w-3.5 h-3.5 text-slate-400" />
                            Official MoSPI Citation: {feedbackItem.source_citation}
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>

              {/* Submit / Retake Action Button */}
              <div className="mt-8 pt-6 border-t border-slate-200 flex items-center justify-between">
                <div className="text-xs text-slate-500">
                  {Object.keys(userAnswers).length} of {activeTest.total_questions} questions answered
                </div>

                {!submissionResult ? (
                  <button
                    onClick={handleSubmitQuiz}
                    disabled={submitting || Object.keys(userAnswers).length === 0}
                    className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs px-5 py-2.5 rounded-lg shadow-xs transition-colors disabled:opacity-50 cursor-pointer"
                  >
                    {submitting ? (
                      <>
                        <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        <span>Evaluating Submissions & Citations...</span>
                      </>
                    ) : (
                      <>
                        <Send className="w-3.5 h-3.5" />
                        <span>Submit Assessment for Grading</span>
                      </>
                    )}
                  </button>
                ) : (
                  <button
                    onClick={() => {
                      setSubmissionResult(null);
                      setUserAnswers({});
                    }}
                    className="flex items-center gap-2 bg-slate-800 hover:bg-slate-900 text-white font-semibold text-xs px-4 py-2 rounded-lg shadow-xs transition-colors cursor-pointer"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>Retake Assessment</span>
                  </button>
                )}
              </div>
            </div>
          ) : (
            <p className="text-sm text-slate-400 text-center py-12">Select a test from the left panel.</p>
          )}
        </div>
      </div>
    </div>
  );
};
