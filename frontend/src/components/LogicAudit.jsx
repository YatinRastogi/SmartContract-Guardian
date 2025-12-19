import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { BrainCircuit, BadgeCheck, Eye } from 'lucide-react';

export default function LogicAudit({ issues }) {
    if (!issues || issues.length === 0) return null;

    return (
        <div className="space-y-8">
            {issues.map((issue, idx) => (
                <div key={idx} className="bg-surface border border-primary/20 rounded-xl overflow-hidden shadow-[0_0_20px_rgba(35,134,54,0.05)]">
                    <div className="flex items-center gap-3 bg-primary/5 p-4 border-b border-primary/10">
                        <BrainCircuit className="text-primary" size={20} />
                        <span className="text-sm font-bold text-primary tracking-wider uppercase">AI Logic Auditor Analysis</span>
                        <div className="flex-1"></div>
                        <div className="flex items-center gap-1.5 px-3 py-1 bg-primary/20 rounded-full text-xs font-bold text-primary border border-primary/30">
                            <BadgeCheck size={14} />
                            Gatekeeper Verified
                        </div>
                    </div>

                    <div className="p-6 md:p-8 grid md:grid-cols-2 gap-8">
                        {/* Left: Explanation */}
                        <div className="space-y-4">
                            <h3 className="text-xl font-bold text-white">{issue.title || issue.original_check}</h3>

                            <div className="flex gap-2 mb-4">
                                <span className="px-2 py-1 bg-border rounded text-[10px] font-mono text-muted uppercase">Category: Logic/State</span>
                                <span className="px-2 py-1 bg-border rounded text-[10px] font-mono text-muted uppercase">Confidence: High</span>
                            </div>

                            <div className="prose prose-invert prose-sm border-l-2 border-primary/30 pl-4 py-1">
                                <p className="text-gray-300 leading-relaxed">{issue.explanation}</p>
                            </div>

                            {issue.remediation && (
                                <div className="bg-blue-900/10 p-4 rounded-lg border border-blue-900/30">
                                    <h4 className="text-blue-400 text-sm font-bold mb-1">Recommended Fix</h4>
                                    <p className="text-blue-200/70 text-sm">{issue.remediation}</p>
                                </div>
                            )}
                        </div>

                        {/* Right: Code Citation */}
                        <div className="space-y-2">
                            <div className="flex items-center gap-2 text-xs text-muted font-mono mb-2">
                                <Eye size={14} />
                                <span>Vulnerable Pattern Detection</span>
                            </div>
                            <div className="rounded-lg overflow-hidden border border-border bg-[#0d1117] shadow-inner h-full">
                                <SyntaxHighlighter
                                    language="solidity"
                                    style={vscDarkPlus}
                                    customStyle={{ margin: 0, height: '100%', fontSize: 12, background: 'transparent' }}
                                    showLineNumbers={true}
                                    wrapLines={true}
                                >
                                    {issue.code_citation || "// No verification citation."}
                                </SyntaxHighlighter>
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}
