import axios from 'axios';

export const API_BASE = 'http://127.0.0.1:8000/api';

export interface CompetencyItem {
  id: string;
  name: string;
  pillar: string;
  description: string;
  keywords: string[];
}

export interface RoleDefinition {
  role_id: string;
  title: string;
  department: string;
  grade: string;
  description: string;
  target_competencies: Record<string, number>;
  primary_focus: string[];
}

export interface TrainingLog {
  course_id: string;
  course_title: string;
  source: string;
  completion_date: string;
  hours_spent: number;
  score_achieved: number;
}

export interface OfficerProfile {
  officer_id: string;
  name: string;
  designation: string;
  role_id: string;
  department: string;
  cadre: string;
  zone: string;
  office_location: string;
  education: string;
  years_experience: number;
  avatar_initials: string;
  training_history: TrainingLog[];
  current_competencies: Record<string, number>;
  self_assessments: Record<string, number>;
}

export interface GapItem {
  competency_id: string;
  competency_name: string;
  pillar: string;
  pillar_label: string;
  target_score: number;
  actual_score: number;
  gap_score: number;
  gap_percentage: number;
  is_primary_focus: boolean;
  urgency_level: 'Critical' | 'High' | 'Moderate' | 'Satisfied';
}

export interface RecommendationItem {
  course_id: string;
  title: string;
  provider: string;
  competency_id: string;
  competency_name: string;
  duration_hours: number;
  level: string;
  is_tpac_recommended: boolean;
  points_award: number;
  urgency: string;
  rank_score: number;
  explanation: string;
}

export interface GapAnalysisReport {
  officer_id: string;
  officer_name: string;
  role_id: string;
  role_title: string;
  overall_readiness_score: number;
  vector_cosine_similarity: number;
  total_gaps_identified: number;
  critical_gaps_count: number;
  pillar_scores: Record<string, { target_avg: number; actual_avg: number; gap_avg: number }>;
  gap_details: GapItem[];
  radar_data: Array<{
    subject: string;
    competency_id: string;
    actual: number;
    target: number;
    gap: number;
    pillar: string;
  }>;
  recommendations: RecommendationItem[];
  relevant_tpac_pathway: {
    pathway_id: string;
    title: string;
    target_audience: string;
    focus_areas: string[];
    recommended_courses: string[];
    mandatory_credits: number;
    cadre: string;
  };
}

export interface MCQOption {
  key: string;
  text: string;
  is_correct: boolean;
  distractor_rationale?: string;
}

export interface AssessmentQuestion {
  id: string;
  blooms_taxonomy: 'Recall' | 'Application' | 'Analysis';
  competency_id: string;
  question: string;
  options: MCQOption[];
  correct_key: string;
  explanation: string;
  source_citation: string;
}

export interface AssessmentTest {
  test_id: string;
  title: string;
  description: string;
  topic: string;
  document_source: string;
  total_questions: number;
  duration_minutes: number;
  questions?: AssessmentQuestion[];
  created_by: string;
  target_role?: string;
}

export interface TestSubmissionFeedback {
  question_id: string;
  question: string;
  blooms_taxonomy: string;
  user_answer: string;
  correct_answer: string;
  is_correct: boolean;
  explanation: string;
  distractor_rationale?: string;
  source_citation: string;
}

export interface TestSubmissionResult {
  test_id: string;
  score_percentage: number;
  passed: boolean;
  correct_answers: number;
  total_questions: number;
  feedback: TestSubmissionFeedback[];
  competency_upgrades: Record<string, number>;
}

export interface RegionalCompetencyMetric {
  zone: string;
  total_officers: number;
  avg_readiness: number;
  stat_score: number;
  tech_score: number;
  gov_score: number;
  mgt_score: number;
  top_deficiency: string;
}

export interface DivisionDeficiencyMetric {
  division: string;
  officer_count: number;
  statistical_gap: number;
  technical_gap: number;
  governance_gap: number;
  managerial_gap: number;
  critical_skills_needed: string[];
}

export interface PredictiveCapacityModel {
  year: number;
  focus_domain: string;
  baseline_proficiency: number;
  projected_without_intervention: number;
  projected_with_igot_intervention: number;
  recommended_target: number;
}

export interface MacroWorkforceReport {
  total_active_cadre: number;
  iss_officers_count: number;
  sss_officers_count: number;
  average_readiness_index: number;
  total_training_hours_completed: number;
  assessments_completed_count: number;
  regional_metrics: RegionalCompetencyMetric[];
  division_heatmap: DivisionDeficiencyMetric[];
  training_velocity_monthly: Array<{
    month: string;
    hours_logged: number;
    certifications: number;
    active_users: number;
  }>;
  predictive_capacity_projections: PredictiveCapacityModel[];
}

export interface APICallLog {
  timestamp: string;
  endpoint: string;
  method: string;
  status_code: number;
  request_payload: any;
  response_payload: any;
}

export const api = {
  getOfficers: async (): Promise<OfficerProfile[]> => {
    const res = await axios.get(`${API_BASE}/officers`);
    return res.data;
  },
  getOfficer: async (id: string): Promise<OfficerProfile> => {
    const res = await axios.get(`${API_BASE}/officer/${id}`);
    return res.data;
  },
  getRoles: async (): Promise<Record<string, RoleDefinition>> => {
    const res = await axios.get(`${API_BASE}/roles`);
    return res.data;
  },
  getGapAnalysis: async (officerId: string): Promise<GapAnalysisReport> => {
    const res = await axios.get(`${API_BASE}/gap-analysis/${officerId}`);
    return res.data;
  },
  switchOfficerRole: async (officerId: string, newRoleId: string) => {
    const res = await axios.post(`${API_BASE}/officer/${officerId}/switch-role`, {
      new_role_id: newRoleId
    });
    return res.data;
  },
  getIgotCourses: async (competencyId?: string) => {
    const url = competencyId ? `${API_BASE}/igot/courses?competency_id=${competencyId}` : `${API_BASE}/igot/courses`;
    const res = await axios.get(url);
    return res.data;
  },
  syncCourseProgress: async (officerId: string, courseId: string, progress: number, hours: number) => {
    const res = await axios.post(`${API_BASE}/igot/sync-progress`, {
      officer_id: officerId,
      course_id: courseId,
      progress_percentage: progress,
      hours_logged: hours
    });
    return res.data;
  },
  getAuditLogs: async (): Promise<APICallLog[]> => {
    const res = await axios.get(`${API_BASE}/igot/audit-logs`);
    return res.data;
  },
  getAssessments: async (): Promise<AssessmentTest[]> => {
    const res = await axios.get(`${API_BASE}/assessments`);
    return res.data;
  },
  getAssessment: async (testId: string): Promise<AssessmentTest> => {
    const res = await axios.get(`${API_BASE}/assessment/${testId}`);
    return res.data;
  },
  submitAssessment: async (testId: string, officerId: string, answers: Record<string, string>): Promise<TestSubmissionResult> => {
    const res = await axios.post(`${API_BASE}/assessment/${testId}/submit`, {
      officer_id: officerId,
      answers
    });
    return res.data;
  },
  generateAssessment: async (documentSource: string, topic: string, numQuestions: number = 3, targetRole?: string): Promise<AssessmentTest> => {
    const res = await axios.post(`${API_BASE}/assessment/generate`, {
      document_source: documentSource,
      topic,
      num_questions: numQuestions,
      target_role: targetRole
    });
    return res.data;
  },
  uploadDocument: async (formData: FormData) => {
    const res = await axios.post(`${API_BASE}/assessment/upload-doc`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return res.data;
  },
  getWorkforceAnalytics: async (): Promise<MacroWorkforceReport> => {
    const res = await axios.get(`${API_BASE}/admin/analytics`);
    return res.data;
  }
};
