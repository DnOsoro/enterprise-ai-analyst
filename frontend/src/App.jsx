import React, { useState } from 'react';
import axios from 'axios';
import { Database, UploadCloud, Link as LinkIcon, Send, Terminal, BarChart2, CheckCircle, AlertCircle } from 'lucide-react';
import DataChart from './components/DataChart';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function App() {
  const [fileInfo, setFileInfo] = useState(null);
  const [connectionString, setConnectionString] = useState('');
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);
    setError(null);

    try {
      const res = await axios.post(`${API_BASE}/api/upload`, formData);
      setFileInfo(res.data);
      setResponse(null);
    } catch (err) {
      setError('Upload failed: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleRunQuery = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setError(null);

    try {
      const res = await axios.post(`${API_BASE}/api/query`, { question });
      setResponse(res.data);
    } catch (err) {
      setError('Query execution failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-[#0a0d14] text-slate-100 font-sans overflow-hidden">
      
      {/* Sidebar Control Panel */}
      <aside className="w-80 bg-[#111521] border-r border-[#23293e] p-6 flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-3 mb-8">
            <Database className="w-6 h-6 text-[#6366f1]" />
            <h1 className="font-bold text-lg tracking-wide text-white">Data Hub</h1>
          </div>

          {/* File Upload Section */}
          <div className="mb-6">
            <label className="text-xs font-semibold text-[#94a3b8] uppercase tracking-wider block mb-3">
              Upload File
            </label>
            <label className="border-2 border-dashed border-[#23293e] hover:border-[#6366f1] bg-[#161b2a] transition-colors rounded-xl p-6 flex flex-col items-center justify-center cursor-pointer group">
              <UploadCloud className="w-8 h-8 text-[#94a3b8] group-hover:text-[#6366f1] mb-2 transition-colors" />
              <span className="text-sm font-medium text-slate-200">Upload Data</span>
              <span className="text-xs text-[#94a3b8] mt-1">CSV, Excel, or JSON formats</span>
              <input type="file" onChange={handleFileUpload} className="hidden" accept=".csv,.xlsx,.xls,.json,.parquet" />
            </label>
            {fileInfo && (
              <div className="mt-3 flex items-center gap-2 text-xs text-emerald-400 bg-emerald-950/40 border border-emerald-800/50 p-2.5 rounded-lg">
                <CheckCircle className="w-4 h-4 shrink-0" />
                <span className="truncate">{fileInfo.filename} ({fileInfo.rows} rows)</span>
              </div>
            )}
          </div>

          <div className="relative flex py-2 items-center">
            <div className="flex-grow border-t border-[#23293e]"></div>
            <span className="flex-shrink mx-4 text-xs text-[#94a3b8] font-semibold uppercase">OR</span>
            <div className="flex-grow border-t border-[#23293e]"></div>
          </div>

          {/* Direct SQL Link Section */}
          <div className="mt-4">
            <label className="text-xs font-semibold text-[#94a3b8] uppercase tracking-wider block mb-3 flex items-center gap-2">
              <LinkIcon className="w-3.5 h-3.5" />
              SQL Server Link
            </label>
            <textarea
              rows="3"
              value={connectionString}
              onChange={(e) => setConnectionString(e.target.value)}
              placeholder="mssql+pymssql://user:pass@server:1433/dbname"
              className="w-full bg-[#161b2a] border border-[#23293e] rounded-xl p-3 text-xs text-slate-200 focus:outline-none focus:border-[#6366f1] transition-colors font-mono resize-none"
            />
            <button 
              disabled
              className="w-full mt-3 bg-[#161b2a] border border-[#23293e] text-[#94a3b8] text-xs font-semibold py-2.5 rounded-xl cursor-not-allowed opacity-60 flex items-center justify-center gap-2"
            >
              <Database className="w-3.5 h-3.5" />
              Connect Endpoint
            </button>
          </div>
        </div>

        <div className="text-xs text-[#94a3b8] border-t border-[#23293e] pt-4">
          Engine: <span className="text-slate-300">FastAPI + DuckDB</span>
        </div>
      </aside>

      {/* Main Workspace Area */}
      <main className="flex-1 flex flex-col h-screen overflow-y-auto">
        {!fileInfo && !response ? (
          /* Empty State View */
          <div className="flex-1 flex flex-col items-center justify-center text-center px-4">
            <h2 className="text-4xl font-extrabold tracking-tight text-white mb-3">
              Conversational Analytics
            </h2>
            <p className="text-[#94a3b8] max-w-md text-sm leading-relaxed">
              Connect your database or upload a dataset to explore your data using natural language.
            </p>
          </div>
        ) : (
          /* Active Results View */
          <div className="flex-1 p-8 max-w-5xl mx-auto w-full space-y-8">
            
            {error && (
              <div className="flex items-center gap-3 bg-rose-950/40 border border-rose-800/50 text-rose-300 p-4 rounded-xl text-sm">
                <AlertCircle className="w-5 h-5 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {response && response.success && (
              <div className="space-y-6">
                {/* Executive Narrative */}
                <div className="bg-[#161b2a] border border-[#23293e] p-6 rounded-xl space-y-2">
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-[#6366f1] flex items-center gap-2">
                    <BarChart2 className="w-4 h-4" />
                    Executive Summary
                  </h3>
                  <p className="text-slate-200 text-lg leading-relaxed font-normal">
                    {response.insight}
                  </p>
                </div>

                {/* Recharts Graphical Rendering */}
                <div>
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-[#94a3b8] mb-3">
                    Visual Synthesis
                  </h3>
                  <DataChart data={response.data} />
                </div>

                {/* SQL Code Block */}
                <div>
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-[#94a3b8] mb-3 flex items-center gap-2">
                    <Terminal className="w-4 h-4" />
                    Verified SQL Execution
                  </h3>
                  <pre className="bg-[#111521] border border-[#23293e] p-4 rounded-xl text-xs font-mono text-emerald-400 overflow-x-auto">
                    {response.generated_sql}
                  </pre>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Floating Natural Language Prompt Input */}
        <div className="p-6 bg-[#0a0d14]/80 backdrop-blur border-t border-[#23293e]">
          <div className="max-w-4xl mx-auto relative flex items-center">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleRunQuery()}
              disabled={!fileInfo || loading}
              placeholder={fileInfo ? "Ask a question about your data..." : "Please upload a dataset from the sidebar to begin..."}
              className="w-full bg-[#161b2a] border border-[#23293e] rounded-xl py-3.5 pl-4 pr-12 text-sm text-slate-100 placeholder-[#94a3b8] focus:outline-none focus:border-[#6366f1] disabled:opacity-50 transition-colors"
            />
            <button
              onClick={handleRunQuery}
              disabled={!fileInfo || loading || !question.trim()}
              className="absolute right-2.5 p-2 bg-[#6366f1] hover:bg-[#4f46e5] text-white rounded-lg disabled:opacity-40 transition-colors"
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}