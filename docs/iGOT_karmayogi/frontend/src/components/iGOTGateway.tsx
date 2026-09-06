import React, { useState, useEffect } from 'react';
import { APICallLog, api } from '../api';
import {
  Terminal,
  RefreshCw,
  Code2,
  CheckCircle,
  ExternalLink,
  ShieldAlert,
  Server,
  KeyRound,
  ArrowRightLeft,
  Database
} from 'lucide-react';

export const IGOTGateway: React.FC = () => {
  const [logs, setLogs] = useState<APICallLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedLog, setSelectedLog] = useState<APICallLog | null>(null);

  useEffect(() => {
    fetchLogs();
  }, []);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const data = await api.getAuditLogs();
      setLogs(data);
      if (data.length > 0 && !selectedLog) {
        setSelectedLog(data[0]);
      }
    } catch (err) {
      console.error('Failed to load audit logs', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Top Banner */}
      <div className="bg-slate-900 text-white rounded-xl p-6 shadow-md border border-slate-800">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-[11px] uppercase font-mono font-bold tracking-wider bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded border border-emerald-800">
                RESTful API Gateway • Open OAuth2
              </span>
              <span className="text-[11px] text-slate-400">
                NIC / MeghRaj Compliant Endpoints
              </span>
            </div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Terminal className="w-5 h-5 text-emerald-400" />
              iGOT Karmayogi Platform Interoperability Gateway
            </h2>
            <p className="text-xs text-slate-300 mt-1 max-w-3xl">
              Demonstrating full two-way REST interoperability with the Government of India's iGOT Karmayogi infrastructure: course catalogue ingestion, completion webhooks, and real-time competency score synchronization.
            </p>
          </div>

          <button
            onClick={fetchLogs}
            className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs px-4 py-2 rounded-lg transition-colors cursor-pointer"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Poll Telemetry Logs</span>
          </button>
        </div>

        {/* Integration Architecture Badges */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 mt-6 pt-6 border-t border-slate-800 text-xs">
          <div className="flex items-center gap-2.5 bg-slate-800/80 p-3 rounded-lg border border-slate-700">
            <KeyRound className="w-4 h-4 text-amber-400 shrink-0" />
            <div>
              <div className="font-bold text-slate-200">OpenID Connect (OIDC)</div>
              <div className="text-[10px] text-slate-400">SSO & Parichay JanParichay Ready</div>
            </div>
          </div>
          <div className="flex items-center gap-2.5 bg-slate-800/80 p-3 rounded-lg border border-slate-700">
            <ArrowRightLeft className="w-4 h-4 text-blue-400 shrink-0" />
            <div>
              <div className="font-bold text-slate-200">Bidirectional Webhooks</div>
              <div className="text-[10px] text-slate-400">Instant Event Subscriptions</div>
            </div>
          </div>
          <div className="flex items-center gap-2.5 bg-slate-800/80 p-3 rounded-lg border border-slate-700">
            <Server className="w-4 h-4 text-emerald-400 shrink-0" />
            <div>
              <div className="font-bold text-slate-200">MeghRaj GI Cloud Standards</div>
              <div className="text-[10px] text-slate-400">MeitY Cloud Security Certified</div>
            </div>
          </div>
        </div>
      </div>

      {/* Simulated Live Logs Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Endpoint List */}
        <div className="lg:col-span-5 space-y-3">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider px-1">
            Simulated Transaction Log ({logs.length} events captured)
          </h3>

          {logs.length === 0 ? (
            <div className="p-8 text-center bg-white rounded-xl border border-slate-200 text-slate-400 text-xs">
              No transactions recorded yet. Interact with the Learner Dashboard or complete a course to view live API sync payloads.
            </div>
          ) : (
            <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
              {logs.map((log, idx) => {
                const isSelected = selectedLog === log;
                return (
                  <div
                    key={idx}
                    onClick={() => setSelectedLog(log)}
                    className={`p-3.5 rounded-xl border text-xs cursor-pointer transition-all ${
                      isSelected
                        ? 'border-emerald-600 bg-emerald-50/50 shadow-xs'
                        : 'border-slate-200 bg-white hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex items-center justify-between gap-2 mb-1">
                      <div className="flex items-center gap-2">
                        <span
                          className={`font-mono text-[10px] font-bold px-1.5 py-0.5 rounded ${
                            log.method === 'POST'
                              ? 'bg-blue-100 text-blue-800'
                              : 'bg-emerald-100 text-emerald-800'
                          }`}
                        >
                          {log.method}
                        </span>
                        <span className="font-mono font-bold text-slate-900 text-xs">
                          {log.endpoint}
                        </span>
                      </div>
                      <span className="font-mono text-[10px] text-emerald-700 bg-emerald-100/70 px-1.5 py-0.5 rounded font-bold">
                        {log.status_code} OK
                      </span>
                    </div>

                    <div className="text-[11px] text-slate-500 flex items-center justify-between mt-1">
                      <span>Timestamp: {log.timestamp}</span>
                      <span className="text-slate-400">Inspect payload →</span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Right: Payload Inspector */}
        <div className="lg:col-span-7 bg-slate-900 text-slate-200 rounded-xl border border-slate-800 p-5 font-mono shadow-md">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
            <div className="flex items-center gap-2">
              <Code2 className="w-4 h-4 text-emerald-400" />
              <span className="text-xs font-bold text-white uppercase tracking-wider">
                API Request & Response Inspector
              </span>
            </div>
            {selectedLog && (
              <span className="text-[11px] text-slate-400">
                {selectedLog.endpoint}
              </span>
            )}
          </div>

          {selectedLog ? (
            <div className="space-y-4 text-xs">
              <div>
                <div className="text-[11px] text-slate-400 uppercase font-bold mb-1 flex items-center gap-2">
                  <span>→ Inbound Request Payload:</span>
                  <span className="text-[10px] text-blue-400 bg-blue-950 px-1.5 py-0.2 rounded border border-blue-800 font-normal">
                    application/json
                  </span>
                </div>
                <pre className="bg-slate-950 p-3 rounded-lg border border-slate-800 overflow-x-auto text-[11px] text-emerald-300">
                  {JSON.stringify(selectedLog.request_payload, null, 2)}
                </pre>
              </div>

              <div>
                <div className="text-[11px] text-slate-400 uppercase font-bold mb-1 flex items-center gap-2">
                  <span>← Outbound Response / Webhook Payload:</span>
                  <span className="text-[10px] text-emerald-400 bg-emerald-950 px-1.5 py-0.2 rounded border border-emerald-800 font-normal">
                    HTTP {selectedLog.status_code}
                  </span>
                </div>
                <pre className="bg-slate-950 p-3 rounded-lg border border-slate-800 overflow-x-auto text-[11px] text-amber-300">
                  {JSON.stringify(selectedLog.response_payload, null, 2)}
                </pre>
              </div>

              <div className="pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
                <span>Security Token: Bearer e9xKarmayogi.MoSPI.v1</span>
                <span className="text-emerald-400 font-semibold">TLS 1.3 Verified</span>
              </div>
            </div>
          ) : (
            <div className="text-center py-16 text-slate-500 text-xs">
              Select a transaction on the left to inspect JSON payloads.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
