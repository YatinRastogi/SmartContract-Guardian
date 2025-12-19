import React, { useState } from 'react';
import { Terminal, Copy, ChevronDown, ChevronUp } from 'lucide-react';

export default function RedTeamTerminal({ manuals }) {
    const [isExpanded, setIsExpanded] = useState(false);
    const [activeManual, setActiveManual] = useState(0);

    if (!manuals || manuals.length === 0) return null;

    return (
        <div className="border border-border rounded-xl overflow-hidden bg-[#0d1117] transition-all duration-300">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between p-4 bg-surface hover:bg-surface/80 transition-colors"
            >
                <div className="flex items-center gap-3">
                    <div className="bg-black/50 p-2 rounded text-red-500 border border-red-500/20">
                        <Terminal size={18} />
                    </div>
                    <div className="text-left">
                        <h3 className="text-sm font-bold text-white">Red Team Exploit Logs</h3>
                        <p className="text-xs text-muted">Simulated attack vectors and Foundry scripts</p>
                    </div>
                </div>
                {isExpanded ? <ChevronUp size={20} className="text-muted" /> : <ChevronDown size={20} className="text-muted" />}
            </button>

            {isExpanded && (
                <div className="p-0 flex flex-col md:flex-row h-[500px] border-t border-border">
                    {/* Manual Selector */}
                    <div className="w-full md:w-64 bg-surface/50 border-r border-border overflow-y-auto">
                        {manuals.map((m, idx) => (
                            <button
                                key={idx}
                                onClick={() => setActiveManual(idx)}
                                className={`w-full text-left p-3 text-xs font-mono border-b border-border/50 hover:bg-surface transition-colors ${activeManual === idx ? 'bg-red-500/10 text-red-400 border-l-2 border-l-red-500' : 'text-muted'
                                    }`}
                            >
                                {m.title}
                            </button>
                        ))}
                    </div>

                    {/* Terminal Content */}
                    <div className="flex-1 bg-black p-6 font-mono text-xs text-green-400 overflow-y-auto custom-scrollbar leading-relaxed">
                        <div className="opacity-50 mb-4 select-none">
                            &gt; Initializing Red Team Protocols...<br />
                            &gt; Accessing Exploit Database...<br />
                            &gt; Target Locked: {manuals[activeManual]?.title}<br />
                            ----------------------------------------
                        </div>
                        <pre className="whitespace-pre-wrap font-inherit">
                            {manuals[activeManual]?.content}
                        </pre>
                    </div>
                </div>
            )}
        </div>
    );
}
