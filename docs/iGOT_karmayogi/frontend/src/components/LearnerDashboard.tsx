import React, { useState } from 'react';
import {
  OfficerProfile,
  GapAnalysisReport,
  RoleDefinition,
  RecommendationItem
} from '../api';
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  Legend,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from 'recharts';
import {
  Award,
  BookOpen,
  CheckCircle2,
  Clock,
  Compass,
  FileText,
  Flame,
  GraduationCap,
  HelpCircle,
  Layers,
  MapPin,
  RefreshCw,
  Sparkles,
  TrendingUp,
  User,
  Zap
} from 'lucide-react';

interface LearnerDashboardProps {
  officer: OfficerProfile;
  gapReport: GapAnalysisReport | null;
  roles: Record<string, RoleDefinition>;
  onSyncCourse: (courseId: string, duration: number) => Promise<void>;
  onRoleSwitch: (roleId: string) => Promise<void>;
  loading: boolean;
  onTakeQuizForCourse?: (competencyId: string) => void;
}

export const LearnerDashboard: React.FC<LearnerDashboardProps> = ({
  officer,
  gapReport,
  roles,
  onSyncCourse,
  onRoleSwitch,
  loading,
  onTakeQuizForCourse
}) => {
  const [syncingCourseId, setSyncingCourseId] = useState<string | null>(null);
  const [selectedPillarFilter, setSelectedPillarFilter] = useState<string>('all');
  const [roleSwitchModalOpen, setRoleSwitchModalOpen] = useState(false);
  const [selectedNewRole, setSelectedNewRole] = useState(officer.role_id);
  const [activeTab, setActiveTab] = useState<'matrix' | 'courses' | 'history'>('matrix');

  if (!gapReport) {
    return (
      <div className="flex flex-col items-center justify-center p-12 text-slate-500">
        <RefreshCw className="w-8 h-8 animate-spin text-blue-600 mb-2" />
        <p className="text-sm font-medium">Computing Vectorized Competency Matrices...</p>
      </div>
    );
  }

  const handleSimulateCompletion = async (rec: RecommendationItem) => {
    try {
      setSyncingCourseId(rec.course_id);
      await onSyncCourse(rec.course_id, rec.duration_hours);
    } finally {
      setSyncingCourseId(null);
    }
  };

  const filteredGaps = selectedPillarFilter === 'all'
    ? gapReport.gap_details
    : gapReport.gap_details.filter(g => g.pillar === selectedPillarFilter);

  // Top 8 radar competencies for neat visualization
  const radarChartData = gapReport.radar_data.slice(0, 8);

  const totalLoggedHours = officer.training_history.reduce((acc, t) => acc + t.hours_spent, 0);

  return (
    <div className="space-y-6 pb-12">
      {/* Top Profile Banner */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs relative overflow-hidden">
        <div className="absolute top-0 right-0 w-80 h-full bg-gradient-to-l from-blue-50/70 to-transparent pointer-events-none" />
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
          <div className="flex items-start gap-4">
            <div className="w-16 h-16 rounded-xl bg-gradient-to-br from-blue-700 to-indigo-900 text-amber-300 font-extrabold text-2xl flex items-center justify-center shadow-md border-2 border-amber-400">
              {officer.avatar_initials}
            </div>
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h2 className="text-xl font-bold text-slate-900">{officer.name}</h2>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-blue-100 text-blue-800 font-semibold border border-blue-200">
                  {officer.cadre}
                </span>
                <span className="text-xs px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 font-medium">
                  {officer.years_experience} Yrs MoSPI Service
                </span>
              </div>
              <p className="text-sm font-semibold text-slate-700 mt-1">
                {gapReport.role_title}
              </p>
              <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500 mt-2">
                <span className="flex items-center gap-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" />
                  {officer.office_location}
                </span>
                <span className="flex items-center gap-1">
                  <GraduationCap className="w-3.5 h-3.5 text-slate-400" />
                  {officer.education}
                </span>
              </div>
            </div>
          </div>

          {/* Quick Metrics & Career Simulator Button */}
          <div className="flex flex-wrap items-center gap-4">
            <div className="bg-slate-50 border border-slate-200 rounded-lg px-4 py-2.5 text-center min-w-[100px]">
              <div className="text-[11px] uppercase font-bold tracking-wider text-slate-500">Readiness</div>
              <div className="text-xl font-extrabold text-blue-700">{gapReport.overall_readiness_score}%</div>
            </div>
            <div className="bg-slate-50 border border-slate-200 rounded-lg px-4 py-2.5 text-center min-w-[100px]">
              <div className="text-[11px] uppercase font-bold tracking-wider text-slate-500">Vector Sim</div>
              <div className="text-xl font-extrabold text-emerald-600">{(gapReport.vector_cosine_similarity * 100).toFixed(0)}%</div>
            </div>
            <div className="bg-slate-50 border border-slate-200 rounded-lg px-4 py-2.5 text-center min-w-[100px]">
              <div className="text-[11px] uppercase font-bold tracking-wider text-slate-500">Study Hours</div>
              <div className="text-xl font-extrabold text-indigo-700">{totalLoggedHours}h</div>
            </div>

            <button
              onClick={() => setRoleSwitchModalOpen(true)}
              className="flex items-center gap-2 bg-gradient-to-r from-blue-700 to-indigo-800 hover:from-blue-800 hover:to-indigo-900 text-white font-medium text-xs px-3.5 py-2.5 rounded-lg shadow-xs transition-all cursor-pointer"
            >
              <Compass className="w-4 h-4 text-amber-300" />
              <span>Simulate Promotion / Role Shift</span>
            </button>
          </div>
        </div>
      </div>

      {/* Role Switch Simulation Modal */}
      {roleSwitchModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-md w-full p-6 border border-slate-200 animate-in fade-in zoom-in-95">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Compass className="w-5 h-5 text-blue-600" />
              Career Progression & Gap Simulator
            </h3>
            <p className="text-xs text-slate-600 mt-1">
              Select a prospective MoSPI role to preview how your competencies match against that role's baseline expectations.
            </p>

            <div className="mt-4 space-y-2">
              {Object.values(roles).map((r) => (
                <label
                  key={r.role_id}
                  className={`flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
                    selectedNewRole === r.role_id
                      ? 'border-blue-600 bg-blue-50/60'
                      : 'border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  <input
                    type="radio"
                    name="role"
                    checked={selectedNewRole === r.role_id}
                    onChange={() => setSelectedNewRole(r.role_id)}
                    className="mt-1 text-blue-600 focus:ring-blue-500"
                  />
                  <div>
                    <div className="text-xs font-bold text-slate-900">{r.title}</div>
                    <div className="text-[11px] text-slate-500">{r.grade} • {r.department}</div>
                  </div>
                </label>
              ))}
            </div>

            <div className="mt-6 flex justify-end gap-2">
              <button
                onClick={() => setRoleSwitchModalOpen(false)}
                className="px-3.5 py-2 rounded-lg border border-slate-300 text-xs font-medium text-slate-700 hover:bg-slate-100"
              >
                Cancel
              </button>
              <button
                onClick={async () => {
                  await onRoleSwitch(selectedNewRole);
                  setRoleSwitchModalOpen(false);
                }}
                className="px-4 py-2 rounded-lg bg-blue-600 text-xs font-medium text-white hover:bg-blue-700 shadow-xs"
              >
                Apply Role & Recompute Gaps
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Grid: Radar Chart + Pillar Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Radar Chart (Actual vs Target) */}
        <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200 p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Flame className="w-4 h-4 text-amber-500" />
                Dynamic Competency Radar (Actual vs Role Target)
              </h3>
              <p className="text-xs text-slate-500">
                Multi-dimensional projection across statistical, technical, and governance competencies
              </p>
            </div>
            <span className="text-xs bg-emerald-50 text-emerald-700 px-2.5 py-1 rounded-full font-semibold border border-emerald-200">
              Cosine Fit: {(gapReport.vector_cosine_similarity * 100).toFixed(1)}%
            </span>
          </div>

          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarChartData}>
                <PolarGrid stroke="#e2e8f0" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: '#475569', fontSize: 11 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: '#94a3b8', fontSize: 10 }} />
                <Radar
                  name="Role Target Baseline"
                  dataKey="target"
                  stroke="#2563eb"
                  fill="#3b82f6"
                  fillOpacity={0.15}
                  strokeWidth={2}
                />
                <Radar
                  name="Officer Actual Score"
                  dataKey="actual"
                  stroke="#10b981"
                  fill="#10b981"
                  fillOpacity={0.4}
                  strokeWidth={2}
                />
                <Legend
                  wrapperStyle={{ paddingTop: '10px', fontSize: '12px' }}
                />
                <Tooltip
                  formatter={(val: any) => [`${val} / 100`, '']}
                  contentStyle={{ borderRadius: '8px', fontSize: '12px', borderColor: '#cbd5e1' }}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>

          <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Primary Focus Areas: {roles[officer.role_id]?.primary_focus.join(', ')}</span>
            <span className="font-semibold text-slate-700">Target Scale: 0 - 100 Points</span>
          </div>
        </div>

        {/* 4-Pillar Score Summary Cards */}
        <div className="lg:col-span-5 flex flex-col justify-between space-y-4">
          <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs flex-1">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2 mb-3">
              <Layers className="w-4 h-4 text-blue-600" />
              MoSPI 4-Pillar Competency Indices
            </h3>

            <div className="space-y-3">
              {Object.entries(gapReport.pillar_scores).map(([pillarKey, p]) => {
                const labels: Record<string, string> = {
                  statistical: 'Statistical Competencies',
                  technical: 'Technical & Data Science',
                  digital_governance: 'Digital Governance & Cloud',
                  behavioural_managerial: 'Behavioural & Leadership'
                };
                const colors: Record<string, string> = {
                  statistical: 'bg-blue-600',
                  technical: 'bg-purple-600',
                  digital_governance: 'bg-emerald-600',
                  behavioural_managerial: 'bg-amber-600'
                };
                const pct = p.target_avg > 0 ? Math.min(100, Math.round((p.actual_avg / p.target_avg) * 100)) : 100;

                return (
                  <div key={pillarKey} className="p-2.5 rounded-lg bg-slate-50 border border-slate-100">
                    <div className="flex justify-between items-center text-xs mb-1.5">
                      <span className="font-bold text-slate-800">{labels[pillarKey] || pillarKey}</span>
                      <span className="text-slate-500 font-medium">
                        {p.actual_avg} / {p.target_avg} pts <span className="font-bold text-slate-700">({pct}%)</span>
                      </span>
                    </div>
                    <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                      <div
                        className={`h-full ${colors[pillarKey] || 'bg-blue-600'} transition-all duration-500`}
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                    {p.gap_avg > 0 ? (
                      <div className="text-[11px] text-rose-600 font-semibold mt-1">
                        Deficit: -{p.gap_avg} pts to standard
                      </div>
                    ) : (
                      <div className="text-[11px] text-emerald-600 font-medium mt-1">
                        ✓ Meets role baseline
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* NSSTA TPAC Framework Box */}
          <div className="bg-gradient-to-br from-indigo-900 to-blue-950 text-white rounded-xl p-5 shadow-xs border border-indigo-800">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] uppercase font-bold tracking-widest bg-indigo-800/80 text-amber-300 px-2 py-0.5 rounded border border-indigo-600">
                NSSTA TPAC Pathway
              </span>
              <span className="text-xs font-semibold text-indigo-200">
                Cadre: {gapReport.relevant_tpac_pathway.cadre}
              </span>
            </div>
            <h4 className="text-sm font-bold text-white mb-1">
              {gapReport.relevant_tpac_pathway.title}
            </h4>
            <p className="text-xs text-indigo-200 mb-3">
              {gapReport.relevant_tpac_pathway.target_audience}
            </p>
            <div className="flex flex-wrap gap-1.5 mb-3">
              {gapReport.relevant_tpac_pathway.focus_areas.map((f, i) => (
                <span key={i} className="text-[10px] bg-white/10 px-2 py-0.5 rounded text-indigo-100">
                  {f}
                </span>
              ))}
            </div>
            <div className="text-[11px] text-indigo-300 flex items-center justify-between border-t border-indigo-800/60 pt-2">
              <span>Mandatory Credits: {gapReport.relevant_tpac_pathway.mandatory_credits} hrs</span>
              <span className="text-amber-300 font-semibold">Endorsed by MoSPI Training Cell</span>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs: Gap Matrix vs Recommendations vs Training History */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="border-b border-slate-200 bg-slate-50/70 px-6 py-3 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab('matrix')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${
                activeTab === 'matrix'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:bg-slate-200/60'
              }`}
            >
              Skill Gap Matrix ({gapReport.total_gaps_identified} Deficits)
            </button>
            <button
              onClick={() => setActiveTab('courses')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${
                activeTab === 'courses'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:bg-slate-200/60'
              }`}
            >
              iGOT & TPAC Recommendations ({gapReport.recommendations.length})
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-colors ${
                activeTab === 'history'
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'text-slate-600 hover:bg-slate-200/60'
              }`}
            >
              Certified Training Logs ({officer.training_history.length})
            </button>
          </div>

          {activeTab === 'matrix' && (
            <div className="flex items-center gap-2 text-xs">
              <span className="text-slate-500 font-medium">Filter Pillar:</span>
              <select
                aria-label="Filter competencies by pillar"
                value={selectedPillarFilter}
                onChange={(e) => setSelectedPillarFilter(e.target.value)}
                className="bg-white border border-slate-300 text-slate-800 text-xs rounded-md px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-600"
              >
                <option value="all">All Pillars</option>
                <option value="statistical">Statistical</option>
                <option value="technical">Technical</option>
                <option value="digital_governance">Digital Governance</option>
                <option value="behavioural_managerial">Behavioural & Managerial</option>
              </select>
            </div>
          )}
        </div>

        {/* Tab 1: Detailed Skill Gap Table */}
        {activeTab === 'matrix' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                  <th className="py-3 px-4">Competency</th>
                  <th className="py-3 px-4">Pillar</th>
                  <th className="py-3 px-4 text-center">Actual / Target</th>
                  <th className="py-3 px-4 text-center">Gap Score</th>
                  <th className="py-3 px-4">Urgency</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs">
                {filteredGaps.map((gap) => (
                  <tr key={gap.competency_id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-4">
                      <div className="font-bold text-slate-900 flex items-center gap-1.5">
                        {gap.competency_name}
                        {gap.is_primary_focus && (
                          <span className="text-[10px] bg-amber-100 text-amber-800 font-bold px-1.5 py-0.2 rounded border border-amber-200">
                            Role Core
                          </span>
                        )}
                      </div>
                      <div className="text-[11px] text-slate-500 font-mono">{gap.competency_id}</div>
                    </td>
                    <td className="py-3 px-4 text-slate-600">{gap.pillar_label}</td>
                    <td className="py-3 px-4 text-center font-medium">
                      <span className="font-bold text-slate-800">{gap.actual_score}</span>
                      <span className="text-slate-400"> / </span>
                      <span className="text-slate-600">{gap.target_score}</span>
                    </td>
                    <td className="py-3 px-4 text-center">
                      {gap.gap_score > 0 ? (
                        <span className="font-bold text-rose-600 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                          -{gap.gap_score} pts
                        </span>
                      ) : (
                        <span className="font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                          Satisfied
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <span
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                          gap.urgency_level === 'Critical'
                            ? 'bg-rose-100 text-rose-800 border-rose-300'
                            : gap.urgency_level === 'High'
                            ? 'bg-amber-100 text-amber-800 border-amber-300'
                            : gap.urgency_level === 'Moderate'
                            ? 'bg-blue-100 text-blue-800 border-blue-300'
                            : 'bg-emerald-100 text-emerald-800 border-emerald-300'
                        }`}
                      >
                        {gap.urgency_level}
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      {gap.gap_score > 0 ? (
                        <button
                          onClick={() => {
                            setActiveTab('courses');
                          }}
                          className="text-[11px] font-semibold text-blue-600 hover:text-blue-800 hover:underline cursor-pointer"
                        >
                          View iGOT Courses →
                        </button>
                      ) : (
                        <span className="text-[11px] text-emerald-600 flex items-center justify-end gap-1 font-medium">
                          <CheckCircle2 className="w-3.5 h-3.5" /> Certified
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Tab 2: Explainable Recommendations (iGOT + TPAC) */}
        {activeTab === 'courses' && (
          <div className="p-6 space-y-4">
            <div className="bg-blue-50/70 border border-blue-200 rounded-lg p-3 text-xs text-blue-900 flex items-start gap-2.5">
              <Sparkles className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
              <div>
                <span className="font-bold">Explainable AI Recommendation Logic:</span> Courses are ranked by combining Gap Severity (45%), Core Role Priority (35%), and NSSTA TPAC Advisory Endorsements (20%). Click "Simulate iGOT Progress & Sync" to simulate webhook course completion and automatic score upgrades.
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {gapReport.recommendations.map((rec) => {
                const isSyncing = syncingCourseId === rec.course_id;
                return (
                  <div
                    key={rec.course_id}
                    className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs hover:border-blue-400 transition-all flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-start justify-between gap-2 mb-2">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                          {rec.provider}
                        </span>
                        <div className="flex items-center gap-1.5">
                          {rec.is_tpac_recommended && (
                            <span className="text-[10px] font-bold bg-purple-50 text-purple-700 px-2 py-0.5 rounded border border-purple-200">
                              TPAC Endorsed
                            </span>
                          )}
                          <span
                            className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                              rec.urgency === 'Critical'
                                ? 'bg-rose-100 text-rose-800'
                                : 'bg-amber-100 text-amber-800'
                            }`}
                          >
                            {rec.urgency}
                          </span>
                        </div>
                      </div>

                      <h4 className="text-sm font-bold text-slate-900 mb-1 leading-snug">
                        {rec.title}
                      </h4>

                      <div className="flex items-center gap-3 text-xs text-slate-500 mb-3">
                        <span className="flex items-center gap-1">
                          <Clock className="w-3.5 h-3.5 text-slate-400" />
                          {rec.duration_hours} Hours
                        </span>
                        <span>•</span>
                        <span className="font-medium text-slate-700">{rec.level} Level</span>
                        <span>•</span>
                        <span className="font-semibold text-emerald-700">+{rec.points_award} Pts Upgrade</span>
                      </div>

                      {/* Explainable AI Note */}
                      <div className="bg-slate-50 rounded-lg p-3 border border-slate-200 text-xs text-slate-700 mb-4">
                        <span className="font-bold text-slate-900 block mb-1">AI Recommendation Rationale:</span>
                        <p className="italic text-slate-600 leading-relaxed">"{rec.explanation}"</p>
                      </div>
                    </div>

                    <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-3">
                      <div className="text-[11px] text-slate-400 font-mono">
                        ID: {rec.course_id}
                      </div>

                      <button
                        onClick={() => handleSimulateCompletion(rec)}
                        disabled={isSyncing}
                        className="flex items-center gap-1.5 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs px-3.5 py-2 rounded-lg transition-colors shadow-xs disabled:opacity-50 cursor-pointer"
                      >
                        {isSyncing ? (
                          <>
                            <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                            <span>Syncing iGOT Webhook...</span>
                          </>
                        ) : (
                          <>
                            <Zap className="w-3.5 h-3.5 text-amber-300" />
                            <span>Simulate iGOT Progress & Sync</span>
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Tab 3: Prior Training History */}
        {activeTab === 'history' && (
          <div className="p-6">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-4">
              Synchronized iGOT Karmayogi & NSSTA Official Training Records
            </h4>

            {officer.training_history.length === 0 ? (
              <p className="text-sm text-slate-400">No training modules logged yet.</p>
            ) : (
              <div className="space-y-3">
                {officer.training_history.map((log, idx) => (
                  <div
                    key={idx}
                    className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl border border-slate-200 bg-slate-50 hover:bg-white transition-colors gap-3"
                  >
                    <div className="flex items-start gap-3">
                      <div className="w-9 h-9 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center shrink-0 border border-emerald-200 mt-0.5">
                        <Award className="w-5 h-5" />
                      </div>
                      <div>
                        <h5 className="text-xs font-bold text-slate-900">{log.course_title}</h5>
                        <div className="flex items-center gap-2 text-[11px] text-slate-500 mt-0.5">
                          <span>{log.source}</span>
                          <span>•</span>
                          <span>Completed: {log.completion_date}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-4 text-xs sm:text-right">
                      <div>
                        <div className="text-[10px] text-slate-400 uppercase font-semibold">Duration</div>
                        <div className="font-bold text-slate-700">{log.hours_spent} Hours</div>
                      </div>
                      <div>
                        <div className="text-[10px] text-slate-400 uppercase font-semibold">Score</div>
                        <div className="font-bold text-emerald-700">{log.score_achieved}%</div>
                      </div>
                      <span className="text-[10px] bg-emerald-50 text-emerald-700 font-bold px-2 py-0.5 rounded border border-emerald-200">
                        Verified
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
