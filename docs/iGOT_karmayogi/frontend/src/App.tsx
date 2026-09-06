import React, { useState, useEffect } from 'react';
import {
  OfficerProfile,
  RoleDefinition,
  GapAnalysisReport,
  api
} from './api';
import { Header } from './components/Header';
import { LearnerDashboard } from './components/LearnerDashboard';
import { AdminDashboard } from './components/AdminDashboard';
import { QuizEngine } from './components/QuizEngine';
import { IGOTGateway } from './components/iGOTGateway';
import { RefreshCw, AlertCircle } from 'lucide-react';

export function App() {
  const [currentTab, setCurrentTab] = useState<'learner' | 'admin' | 'assessments' | 'interop'>('learner');
  const [officers, setOfficers] = useState<OfficerProfile[]>([]);
  const [selectedOfficer, setSelectedOfficer] = useState<OfficerProfile | null>(null);
  const [roles, setRoles] = useState<Record<string, RoleDefinition>>({});
  const [gapReport, setGapReport] = useState<GapAnalysisReport | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize data on mount
  useEffect(() => {
    const initData = async () => {
      try {
        setLoading(true);
        const [officersList, rolesList] = await Promise.all([
          api.getOfficers(),
          api.getRoles()
        ]);
        setOfficers(officersList);
        setRoles(rolesList);
        if (officersList.length > 0) {
          const firstOfficer = officersList[0];
          setSelectedOfficer(firstOfficer);
          await loadGapReport(firstOfficer.officer_id);
        }
      } catch (err: any) {
        console.error('Initialization error', err);
        setError('Could not connect to FastAPI backend at http://127.0.0.1:8000. Please ensure the backend is running.');
      } finally {
        setLoading(false);
      }
    };
    initData();
  }, []);

  const loadGapReport = async (officerId: string) => {
    try {
      const report = await api.getGapAnalysis(officerId);
      setGapReport(report);
    } catch (err) {
      console.error('Failed to load gap report', err);
    }
  };

  const handleSelectOfficer = async (officer: OfficerProfile) => {
    setSelectedOfficer(officer);
    await loadGapReport(officer.officer_id);
  };

  const handleSyncCourse = async (courseId: string, duration: number) => {
    if (!selectedOfficer) return;
    try {
      await api.syncCourseProgress(
        selectedOfficer.officer_id,
        courseId,
        100, // 100% completion
        duration
      );
      // Refresh officer profile and gap analysis
      const updatedOfficer = await api.getOfficer(selectedOfficer.officer_id);
      setSelectedOfficer(updatedOfficer);
      await loadGapReport(updatedOfficer.officer_id);
    } catch (err) {
      console.error('Failed to sync course', err);
    }
  };

  const handleRoleSwitch = async (newRoleId: string) => {
    if (!selectedOfficer) return;
    try {
      const res = await api.switchOfficerRole(selectedOfficer.officer_id, newRoleId);
      setSelectedOfficer(res.profile);
      await loadGapReport(selectedOfficer.officer_id);
    } catch (err) {
      console.error('Failed to switch role', err);
    }
  };

  const handleRefreshOfficer = async () => {
    if (!selectedOfficer) return;
    const updatedOfficer = await api.getOfficer(selectedOfficer.officer_id);
    setSelectedOfficer(updatedOfficer);
    await loadGapReport(updatedOfficer.officer_id);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-6 text-slate-600">
        <div className="w-10 h-10 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
        <h2 className="text-base font-bold text-slate-800">
          Initializing MoSPI Competency Intelligence Platform...
        </h2>
        <p className="text-xs text-slate-500 mt-1">
          Loading official taxonomies, vector indices, and role baselines
        </p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-white rounded-xl border border-rose-200 p-6 shadow-sm text-center">
          <AlertCircle className="w-10 h-10 text-rose-600 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-900">Backend Connection Error</h3>
          <p className="text-xs text-slate-600 mt-2 mb-4">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg text-xs font-semibold hover:bg-blue-700"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Header
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        officers={officers}
        selectedOfficer={selectedOfficer}
        onSelectOfficer={handleSelectOfficer}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        {currentTab === 'learner' && selectedOfficer && (
          <LearnerDashboard
            officer={selectedOfficer}
            gapReport={gapReport}
            roles={roles}
            onSyncCourse={handleSyncCourse}
            onRoleSwitch={handleRoleSwitch}
            loading={loading}
          />
        )}

        {currentTab === 'admin' && <AdminDashboard />}

        {currentTab === 'assessments' && selectedOfficer && (
          <QuizEngine
            currentOfficer={selectedOfficer}
            onRefreshOfficer={handleRefreshOfficer}
          />
        )}

        {currentTab === 'interop' && <IGOTGateway />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-4 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-2">
          <div>
            <span>Ministry of Statistics & Programme Implementation (MoSPI) • National Statistical Systems Training Academy (NSSTA)</span>
          </div>
          <div className="flex items-center gap-3 font-medium">
            <span>Problem Statement 26101</span>
            <span>•</span>
            <span className="text-emerald-700">iGOT Karmayogi Compliant</span>
            <span>•</span>
            <span>Mission Karmayogi Bharat</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
export default App;
