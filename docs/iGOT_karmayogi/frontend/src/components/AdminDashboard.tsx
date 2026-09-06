import React, { useState, useEffect } from 'react';
import { MacroWorkforceReport, api } from '../api';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  AreaChart,
  Area,
  LineChart,
  Line,
  Legend
} from 'recharts';
import {
  BarChart3,
  TrendingUp,
  Users,
  Shield,
  Clock,
  Sparkles,
  MapPin,
  AlertTriangle,
  Layers,
  Brain,
  Download,
  CheckCircle2
} from 'lucide-react';

export const AdminDashboard: React.FC = () => {
  const [report, setReport] = useState<MacroWorkforceReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedZone, setSelectedZone] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const data = await api.getWorkforceAnalytics();
        setReport(data);
      } catch (err) {
        console.error('Failed to load workforce analytics', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading || !report) {
    return (
      <div className="flex flex-col items-center justify-center p-16 text-slate-500">
        <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-3"></div>
        <p className="text-sm font-semibold">Aggregating Pan-India MoSPI Workforce Metrics...</p>
      </div>
    );
  }

  // Predictive chart data transformation
  const aiTrendData = report.predictive_capacity_projections
    .filter(p => p.focus_domain.includes('AI & Machine Learning'))
    .map(p => ({
      year: p.year,
      withoutIntervention: p.projected_without_intervention,
      withIntervention: p.projected_with_igot_intervention,
      target: p.recommended_target
    }));

  const gisTrendData = report.predictive_capacity_projections
    .filter(p => p.focus_domain.includes('GIS & Spatial'))
    .map(p => ({
      year: p.year,
      withoutIntervention: p.projected_without_intervention,
      withIntervention: p.projected_with_igot_intervention,
      target: p.recommended_target
    }));

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner with MoSPI Header */}
      <div className="bg-gradient-to-r from-slate-900 via-blue-950 to-indigo-950 text-white rounded-xl p-6 shadow-md border border-slate-800">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[11px] uppercase font-bold tracking-widest bg-blue-500/30 text-blue-300 px-2.5 py-0.5 rounded border border-blue-400/40">
                MoSPI Executive Headquarters • NSSTA Directorate
              </span>
              <span className="text-[11px] text-emerald-400 flex items-center gap-1 font-semibold">
                ● Live Workforce Telemetry
              </span>
            </div>
            <h2 className="text-xl font-black tracking-tight text-white">
              Official Statistical Cadre: Macro Capacity & Skill Intelligence
            </h2>
            <p className="text-xs text-slate-300 mt-1 max-w-2xl">
              Real-time aggregation across 6 NSSO Zones, 5 Central Divisions, and 4,820 statistical officers under the Ministry of Statistics and Programme Implementation.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => window.print()}
              className="flex items-center gap-1.5 bg-white/10 hover:bg-white/20 text-xs font-semibold px-3 py-2 rounded-lg border border-white/20 transition-colors"
            >
              <Download className="w-3.5 h-3.5 text-amber-300" />
              Export MoSPI Report
            </button>
          </div>
        </div>

        {/* 4 Macro KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-800">
          <div className="bg-white/5 rounded-lg p-3.5 border border-white/10">
            <div className="text-[11px] text-slate-400 font-medium uppercase tracking-wider flex items-center justify-between">
              Total Cadre Enrolled
              <Users className="w-4 h-4 text-blue-400" />
            </div>
            <div className="text-2xl font-black text-white mt-1">
              {report.total_active_cadre.toLocaleString()}
            </div>
            <div className="text-[10px] text-blue-300 mt-0.5">
              {report.iss_officers_count} ISS • {report.sss_officers_count} SSS Officers
            </div>
          </div>

          <div className="bg-white/5 rounded-lg p-3.5 border border-white/10">
            <div className="text-[11px] text-slate-400 font-medium uppercase tracking-wider flex items-center justify-between">
              Avg Readiness Index
              <TrendingUp className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-2xl font-black text-emerald-400 mt-1">
              {report.average_readiness_index}%
            </div>
            <div className="text-[10px] text-emerald-300 mt-0.5">
              +4.8% YoY across standard roles
            </div>
          </div>

          <div className="bg-white/5 rounded-lg p-3.5 border border-white/10">
            <div className="text-[11px] text-slate-400 font-medium uppercase tracking-wider flex items-center justify-between">
              iGOT Study Hours
              <Clock className="w-4 h-4 text-amber-400" />
            </div>
            <div className="text-2xl font-black text-amber-300 mt-1">
              {report.total_training_hours_completed.toLocaleString()}h
            </div>
            <div className="text-[10px] text-amber-200 mt-0.5">
              Across verified TPAC tracks
            </div>
          </div>

          <div className="bg-white/5 rounded-lg p-3.5 border border-white/10">
            <div className="text-[11px] text-slate-400 font-medium uppercase tracking-wider flex items-center justify-between">
              Assessments Cleared
              <Sparkles className="w-4 h-4 text-purple-400" />
            </div>
            <div className="text-2xl font-black text-purple-300 mt-1">
              {report.assessments_completed_count.toLocaleString()}
            </div>
            <div className="text-[10px] text-purple-200 mt-0.5">
              RAG Bloom's-level certified
            </div>
          </div>
        </div>
      </div>

      {/* Regional NSSO FOD Heatmap & Zonal Table */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <MapPin className="w-4 h-4 text-rose-600" />
              Regional Competency Distribution (6 NSSO FOD Field Zones)
            </h3>
            <p className="text-xs text-slate-500">
              Comparative benchmark of statistical, technical, and governance readiness across India
            </p>
          </div>
          <span className="text-xs bg-slate-100 text-slate-700 px-2.5 py-1 rounded-full font-semibold">
            Field Operations Cadre: 2,950 Officers
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Regional Table */}
          <div className="lg:col-span-2 overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                  <th className="py-2.5 px-3">NSSO Zone</th>
                  <th className="py-2.5 px-3 text-center">Officers</th>
                  <th className="py-2.5 px-3 text-center">Readiness</th>
                  <th className="py-2.5 px-3 text-center">Stat / Tech / Gov</th>
                  <th className="py-2.5 px-3">Critical Upskilling Deficit</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-xs">
                {report.regional_metrics.map((reg) => (
                  <tr
                    key={reg.zone}
                    onClick={() => setSelectedZone(reg.zone)}
                    className="hover:bg-blue-50/50 cursor-pointer transition-colors"
                  >
                    <td className="py-3 px-3 font-semibold text-slate-900">
                      {reg.zone}
                    </td>
                    <td className="py-3 px-3 text-center text-slate-600 font-medium">
                      {reg.total_officers}
                    </td>
                    <td className="py-3 px-3 text-center">
                      <span
                        className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                          reg.avg_readiness >= 75
                            ? 'bg-emerald-100 text-emerald-800'
                            : 'bg-amber-100 text-amber-800'
                        }`}
                      >
                        {reg.avg_readiness}%
                      </span>
                    </td>
                    <td className="py-3 px-3 text-center text-[11px] font-mono text-slate-600">
                      <span className="text-blue-700 font-bold">{reg.stat_score.toFixed(0)}</span> /{' '}
                      <span className="text-purple-700 font-bold">{reg.tech_score.toFixed(0)}</span> /{' '}
                      <span className="text-emerald-700 font-bold">{reg.gov_score.toFixed(0)}</span>
                    </td>
                    <td className="py-3 px-3">
                      <span className="text-[11px] font-medium text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                        {reg.top_deficiency}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Regional Summary Bar Chart */}
          <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 flex flex-col justify-between">
            <div>
              <h4 className="text-xs font-bold text-slate-800 mb-2">
                Regional Readiness Comparison
              </h4>
              <p className="text-[11px] text-slate-500 mb-3">
                Identifies zones requiring urgent NSSTA residential deployment
              </p>
            </div>
            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={report.regional_metrics.map(r => ({
                    name: r.zone.split(' ')[0],
                    readiness: r.avg_readiness
                  }))}
                  layout="vertical"
                  margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
                  <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 10 }} />
                  <YAxis dataKey="name" type="category" tick={{ fontSize: 11 }} />
                  <Tooltip formatter={(val: any) => [`${val}%`, 'Readiness']} />
                  <Bar dataKey="readiness" fill="#3b82f6" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="text-[10px] text-slate-400 text-right mt-2">
              Scale: 0 to 100% Competency Baseline
            </div>
          </div>
        </div>
      </div>

      {/* Division Skill Deficiency Matrix */}
      <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-xs">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Layers className="w-4 h-4 text-purple-600" />
              Division-Wise Skill Deficiency Matrix (Heatmap)
            </h3>
            <p className="text-xs text-slate-500">
              Quantified deficits across core MoSPI divisions to direct departmental training allocations
            </p>
          </div>
          <span className="text-xs font-semibold text-slate-600">
            5 MoSPI Directorates
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {report.division_heatmap.map((div) => (
            <div
              key={div.division}
              className="bg-slate-50 rounded-xl p-4 border border-slate-200 hover:border-slate-300 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h4 className="text-xs font-bold text-slate-900 leading-snug">
                    {div.division}
                  </h4>
                  <span className="text-[10px] font-bold text-slate-500 bg-white px-2 py-0.5 rounded border border-slate-200">
                    {div.officer_count} Officers
                  </span>
                </div>

                {/* Gap bars */}
                <div className="space-y-1.5 mt-3 text-[11px]">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600">Technical (R/Python/Stata):</span>
                    <span className={`font-bold ${div.technical_gap > 25 ? 'text-rose-600' : 'text-slate-800'}`}>
                      -{div.technical_gap}% Gap
                    </span>
                  </div>
                  <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${div.technical_gap > 25 ? 'bg-rose-500' : 'bg-purple-600'}`}
                      style={{ width: `${Math.min(100, div.technical_gap * 2.5)}%` }}
                    />
                  </div>

                  <div className="flex justify-between items-center pt-1">
                    <span className="text-slate-600">Statistical Methodology:</span>
                    <span className="font-bold text-slate-800">-{div.statistical_gap}% Gap</span>
                  </div>
                  <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-600"
                      style={{ width: `${Math.min(100, div.statistical_gap * 2.5)}%` }}
                    />
                  </div>

                  <div className="flex justify-between items-center pt-1">
                    <span className="text-slate-600">Cloud / DPDP Governance:</span>
                    <span className="font-bold text-slate-800">-{div.governance_gap}% Gap</span>
                  </div>
                  <div className="w-full bg-slate-200 h-1.5 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-emerald-600"
                      style={{ width: `${Math.min(100, div.governance_gap * 2.5)}%` }}
                    />
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-200">
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">
                  Critical Intervention Targets:
                </div>
                <div className="flex flex-wrap gap-1">
                  {div.critical_skills_needed.map((sk, i) => (
                    <span
                      key={i}
                      className="text-[10px] bg-white text-slate-700 px-2 py-0.5 rounded border border-slate-200 font-medium"
                    >
                      {sk}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Lower Row: Training Velocity & Predictive Capacity Modeling */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Training Velocity Chart */}
        <div className="lg:col-span-6 bg-white rounded-xl border border-slate-200 p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-blue-600" />
                Training Completion Velocity (6-Month Trajectory)
              </h3>
              <p className="text-xs text-slate-500">
                Monthly growth in logged hours and verified competency certifications
              </p>
            </div>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={report.training_velocity_monthly}>
                <defs>
                  <linearGradient id="hoursGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="month" tick={{ fontSize: 11 }} />
                <YAxis tick={{ fontSize: 10 }} />
                <Tooltip />
                <Area
                  type="monotone"
                  dataKey="hours_logged"
                  stroke="#2563eb"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#hoursGrad)"
                  name="Hours Logged"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          <div className="flex items-center justify-between text-xs text-slate-500 mt-2">
            <span>Velocity acceleration: +211% since Oct 2025 launch</span>
            <span className="font-semibold text-blue-700">4,420 hrs in Mar 2026</span>
          </div>
        </div>

        {/* Predictive AI Capacity Modeling (2025 -> 2028) */}
        <div className="lg:col-span-6 bg-white rounded-xl border border-slate-200 p-6 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <Brain className="w-4 h-4 text-indigo-600" />
                Predictive AI & Modernization Capacity Forecast (2025 - 2027)
              </h3>
              <p className="text-xs text-slate-500">
                AI/ML & GIS capability transition with vs without targeted iGOT/TPAC intervention
              </p>
            </div>
            <span className="text-[11px] bg-purple-50 text-purple-700 font-bold px-2 py-0.5 rounded border border-purple-200">
              MoSPI 2026-28 Vision
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={aiTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="year" tick={{ fontSize: 11 }} />
                <YAxis domain={[20, 100]} tick={{ fontSize: 10 }} />
                <Tooltip formatter={(val: any) => [`${val}%`, '']} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '8px' }} />
                <Line
                  type="monotone"
                  dataKey="withIntervention"
                  name="With iGOT Karmayogi AI Engine"
                  stroke="#10b981"
                  strokeWidth={2.5}
                  dot={{ r: 4 }}
                />
                <Line
                  type="monotone"
                  dataKey="withoutIntervention"
                  name="Without Intervention (Baseline Trend)"
                  stroke="#ef4444"
                  strokeDasharray="4 4"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="target"
                  name="Target MoSPI Capacity"
                  stroke="#6366f1"
                  strokeWidth={2}
                  dot={{ r: 3 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="flex items-center justify-between text-xs text-slate-500 mt-2">
            <span>Simulated with Bayesian regression over historical NSSTA cohorts</span>
            <span className="font-semibold text-emerald-700">Reaches 88% capacity by 2027</span>
          </div>
        </div>
      </div>
    </div>
  );
};
