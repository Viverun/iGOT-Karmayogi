import React from 'react';
import { OfficerProfile } from '../api';
import { ShieldCheck, UserCheck, BarChart3, BookOpen, Terminal, Sparkles, Award } from 'lucide-react';

interface HeaderProps {
  currentTab: 'learner' | 'admin' | 'assessments' | 'interop';
  setCurrentTab: (tab: 'learner' | 'admin' | 'assessments' | 'interop') => void;
  officers: OfficerProfile[];
  selectedOfficer: OfficerProfile | null;
  onSelectOfficer: (officer: OfficerProfile) => void;
}

export const Header: React.FC<HeaderProps> = ({
  currentTab,
  setCurrentTab,
  officers,
  selectedOfficer,
  onSelectOfficer,
}) => {
  return (
    <header className="border-b border-slate-200 bg-white sticky top-0 z-50 shadow-xs">
      {/* Top National Strip */}
      <div className="h-1.5 w-full bg-gradient-to-r from-amber-500 via-white to-emerald-600"></div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-3">
          {/* Logo & National Branding */}
          <div className="flex items-center gap-3.5">
            <div className="w-11 h-11 rounded-lg bg-gradient-to-br from-blue-900 to-indigo-950 flex items-center justify-center text-amber-400 shadow-sm border border-blue-800">
              <span className="font-serif font-black text-2xl tracking-tighter">🏛️</span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-bold tracking-widest uppercase text-amber-600 bg-amber-50 px-2 py-0.5 rounded border border-amber-200">
                  MoSPI • NSSTA
                </span>
                <span className="text-[11px] font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                  Mission Karmayogi AI
                </span>
              </div>
              <h1 className="text-lg font-bold text-slate-900 leading-tight">
                Statistical Competency Intelligence & Learning Layer
              </h1>
              <p className="text-xs text-slate-500 hidden sm:block">
                Autonomous Role Profiling, Target-Actual Gap Vectorization & RAG Assessments (PS 26101)
              </p>
            </div>
          </div>

          {/* Officer Selector & Cadre Indicator */}
          <div className="flex items-center gap-3">
            <div className="text-right hidden md:block">
              <div className="text-xs text-slate-500 font-medium">Logged Officer Profile</div>
              <div className="text-xs font-semibold text-slate-800 flex items-center justify-end gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                {selectedOfficer?.cadre.split(' - ')[0] || 'Cadre'}
              </div>
            </div>

            <div className="relative">
              <select
                aria-label="Select Logged Officer Profile"
                value={selectedOfficer?.officer_id || ''}
                onChange={(e) => {
                  const off = officers.find((o) => o.officer_id === e.target.value);
                  if (off) onSelectOfficer(off);
                }}
                className="bg-slate-50 hover:bg-slate-100 text-slate-900 font-medium text-xs rounded-lg border border-slate-300 py-2 pl-3 pr-8 focus:outline-none focus:ring-2 focus:ring-blue-600 transition-colors shadow-xs"
              >
                {officers.map((off) => (
                  <option key={off.officer_id} value={off.officer_id}>
                    {off.name} ({off.designation} - {off.zone} Zone)
                  </option>
                ))}
              </select>
            </div>

            {selectedOfficer && (
              <div className="w-9 h-9 rounded-full bg-blue-700 text-white font-bold text-xs flex items-center justify-center border-2 border-amber-400 shadow-xs">
                {selectedOfficer.avatar_initials}
              </div>
            )}
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="flex space-x-1 sm:space-x-4 border-t border-slate-100 pt-1 overflow-x-auto">
          <button
            onClick={() => setCurrentTab('learner')}
            className={`flex items-center gap-2 py-2.5 px-3 border-b-2 font-medium text-xs whitespace-nowrap transition-colors ${
              currentTab === 'learner'
                ? 'border-blue-600 text-blue-700 font-semibold'
                : 'border-transparent text-slate-500 hover:text-slate-800 hover:border-slate-300'
            }`}
          >
            <UserCheck className="w-4 h-4" />
            <span>Learner Intelligence Hub</span>
          </button>

          <button
            onClick={() => setCurrentTab('admin')}
            className={`flex items-center gap-2 py-2.5 px-3 border-b-2 font-medium text-xs whitespace-nowrap transition-colors ${
              currentTab === 'admin'
                ? 'border-blue-600 text-blue-700 font-semibold'
                : 'border-transparent text-slate-500 hover:text-slate-800 hover:border-slate-300'
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span>Workforce Macro Analytics (Admin/HR)</span>
          </button>

          <button
            onClick={() => setCurrentTab('assessments')}
            className={`flex items-center gap-2 py-2.5 px-3 border-b-2 font-medium text-xs whitespace-nowrap transition-colors ${
              currentTab === 'assessments'
                ? 'border-blue-600 text-blue-700 font-semibold'
                : 'border-transparent text-slate-500 hover:text-slate-800 hover:border-slate-300'
            }`}
          >
            <Sparkles className="w-4 h-4 text-purple-600" />
            <span>AI Assessment & Quiz Studio (RAG)</span>
          </button>

          <button
            onClick={() => setCurrentTab('interop')}
            className={`flex items-center gap-2 py-2.5 px-3 border-b-2 font-medium text-xs whitespace-nowrap transition-colors ${
              currentTab === 'interop'
                ? 'border-blue-600 text-blue-700 font-semibold'
                : 'border-transparent text-slate-500 hover:text-slate-800 hover:border-slate-300'
            }`}
          >
            <Terminal className="w-4 h-4 text-emerald-600" />
            <span>iGOT Karmayogi API Interoperability</span>
          </button>
        </div>
      </div>
    </header>
  );
};
