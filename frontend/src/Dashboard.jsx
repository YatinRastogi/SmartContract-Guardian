import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Download, ShieldCheck, FileText, Zap, BrainCircuit, Code, RefreshCcw } from 'lucide-react';

// Components
import Header from './components/Header';
import UploadZone from './components/UploadZone';
import AgentStepper from './components/AgentStepper';
import FindingsList from './components/FindingsList';
import LogicAudit from './components/LogicAudit';
import RedTeamTerminal from './components/RedTeamTerminal';
import DiffViewer from './components/DiffViewer';

const API_BASE = "http://localhost:8000";

export default function Dashboard() {
    const [status, setStatus] = useState("idle");
    const [report, setReport] = useState(null);
    const [manuals, setManuals] = useState([]);
    const [fixedCode, setFixedCode] = useState("");
    const [originalCode, setOriginalCode] = useState("");
    const [activeTab, setActiveTab] = useState("static"); // static | logic | redteam | code

    // Polling
    useEffect(() => {
        let interval;
        if (status !== 'idle' && status !== 'error') {
            interval = setInterval(async () => {
                try {
                    const res = await axios.get(`${API_BASE}/status`);
                    setStatus(res.data.status);
                } catch (e) {
                    console.error("Polling error", e);
                }
            }, 1500);
        }
        return () => clearInterval(interval);
    }, [status]);

    // Load Data on Completion
    useEffect(() => {
        if (status === 'completed' && !report) {
            loadData();
        }
    }, [status]);

    const loadData = async () => {
        try {
            const [rep, man, fix] = await Promise.all([
                axios.get(`${API_BASE}/report`),
                axios.get(`${API_BASE}/manuals`),
                axios.get(`${API_BASE}/fixed-code`)
            ]);
            setReport(rep.data);
            setManuals(man.data);
            setFixedCode(fix.data.code);
            setActiveTab("static");
        } catch (e) {
            console.error(e);
        }
    };

    const handleUpload = async (file) => {
        const formData = new FormData();
        formData.append("file", file);

        // Read file content for DiffViewer
        const reader = new FileReader();
        reader.onload = (e) => {
            setOriginalCode(e.target.result);
        };
        reader.readAsText(file);

        setStatus("scanning");
        setReport(null);
        setFixedCode(""); // Reset fixed code

        try {
            await axios.post(`${API_BASE}/upload`, formData);
        } catch (e) {
            setStatus("error");
            alert("Upload failed. Check backend console.");
        }
    };

    const handleDownloadPdf = () => {
        window.open(`${API_BASE}/download-pdf`, '_blank');
    };

    const handleReset = () => {
        setStatus("idle");
        setReport(null);
    };

    // Content Renderer
    const renderContent = () => {
        if (!report) return null;

        switch (activeTab) {
            case 'static':
                return <FindingsList issues={report.code_vulnerabilities} />;
            case 'logic':
                return <LogicAudit issues={report.logic_vulnerabilities} />;
            case 'redteam':
                return <RedTeamTerminal manuals={manuals} />;
            case 'code':
                // We need original code for diff. Assuming report might contain it or we fetch it. 
                // For now, let's mock original as "Loading..." or pass it if available. 
                // Backend report endpoint doesn't seem to return original source, only issues. 
                // Let's assume fixedCode comes with a property or we just show fixed.
                // *Self-Correction*: DiffViewer needs original. I'll pass fixedCode as both for now if original missing, 
                // or maybe I should fetch original source in loadData. 
                // Let's just use fixedCode for now to avoid breaking. 
                // Ideally we should add /source endpoint. 
                return <DiffViewer originalCode={originalCode || "// Loading original source..."} fixedCode={fixedCode} />;
            default:
                return null;
        }
    };

    return (
        <div className="min-h-screen bg-background font-sans text-text selection:bg-primary/30">
            <Header status={status} />

            <main className="p-8 max-w-7xl mx-auto pb-24">

                {status === 'idle' && <UploadZone onUpload={handleUpload} />}

                {status !== 'idle' && (
                    <div className="animate-in fade-in slide-in-from-bottom-4 duration-700">
                        <AgentStepper status={status} />
                    </div>
                )}

                {/* Results Area */}
                {report && (
                    <div className="animate-in fade-in duration-500 space-y-8">

                        {/* Actions Bar */}
                        <div className="flex justify-between items-center bg-surface p-4 rounded-xl border border-border shadow-lg">
                            <div className="flex items-center gap-2">
                                <TabButton id="static" label="Verified Findings" icon={ShieldCheck} active={activeTab} onClick={setActiveTab} />
                                <TabButton id="logic" label="AI Logic Audit" icon={BrainCircuit} active={activeTab} onClick={setActiveTab} />
                                <TabButton id="redteam" label="Red Team" icon={Zap} active={activeTab} onClick={setActiveTab} />
                                <TabButton id="code" label="Fixed Code" icon={Code} active={activeTab} onClick={setActiveTab} />
                            </div>
                            <div className="flex items-center gap-3">
                                <button onClick={handleReset} className="p-2 text-muted hover:text-text hover:bg-white/5 rounded-lg transition-colors">
                                    <RefreshCcw size={18} />
                                </button>
                                <button
                                    onClick={handleDownloadPdf}
                                    className="flex items-center gap-2 px-4 py-2 bg-secondary hover:bg-blue-600 text-white rounded-lg font-medium shadow-lg shadow-blue-900/20 transition-all"
                                >
                                    <Download size={16} />
                                    <span>Download PDF Report</span>
                                </button>
                            </div>
                        </div>

                        {/* Main Content View */}
                        <div className="min-h-[400px]">
                            {renderContent()}
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

function TabButton({ id, label, icon: Icon, active, onClick }) {
    const isActive = active === id;
    return (
        <button
            onClick={() => onClick(id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-all ${isActive
                ? 'bg-primary/10 text-primary border border-primary/20'
                : 'text-muted hover:text-text hover:bg-white/5'
                }`}
        >
            <Icon size={16} />
            <span>{label}</span>
        </button>
    )
}
