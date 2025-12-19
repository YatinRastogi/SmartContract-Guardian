import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { AlertCircle, AlertTriangle, Info, ShieldAlert } from 'lucide-react';

const SEVERITY_MAP = {
    'Critical': { color: 'text-alert bg-alert/10 border-alert/20', icon: ShieldAlert },
    'High': { color: 'text-orange-500 bg-orange-500/10 border-orange-500/20', icon: AlertTriangle },
    'Medium': { color: 'text-yellow-500 bg-yellow-500/10 border-yellow-500/20', icon: AlertCircle },
    'Low': { color: 'text-blue-500 bg-blue-500/10 border-blue-500/20', icon: Info },
    'Informational': { color: 'text-gray-400 bg-gray-500/10 border-gray-500/20', icon: Info },
};

export default function FindingsList({ issues }) {
    if (!issues || issues.length === 0) {
        return (
            <div className="p-12 text-center text-muted border border-dashed border-border rounded-xl">
                <ShieldAlert className="w-12 h-12 mx-auto mb-4 opacity-20" />
                <p>No static vulnerabilities detected.</p>
            </div>
        )
    }

    return (
        <div className="space-y-6">
            {issues.map((issue, idx) => {
                const severity = issue.severity || issue.impact || 'Medium'; // Fallback
                const style = SEVERITY_MAP[severity] || SEVERITY_MAP['Medium'];
                const Icon = style.icon;

                return (
                    <div key={idx} className="bg-surface border border-border rounded-xl overflow-hidden hover:border-text/20 transition-all">
                        {/* Header */}
                        <div className="flex items-start justify-between p-6 bg-background/50 border-b border-border">
                            <div className="flex gap-4">
                                <div className={`p-2 rounded-lg h-fit ${style.color} border`}>
                                    <Icon size={20} />
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold text-text mb-1 flex items-center gap-2">
                                        {issue.check}
                                        <span className={`text-[10px] px-2 py-0.5 rounded-full border uppercase tracking-wide ${style.color}`}>
                                            {severity}
                                        </span>
                                    </h3>
                                    <p className="text-sm text-muted font-mono">{(issue.description || 'No description available').split('.')[0]}.</p>
                                </div>
                            </div>
                            {issue.line && (
                                <div className="text-xs font-mono text-muted border border-border px-3 py-1 rounded">
                                    Line {issue.line}
                                </div>
                            )}
                        </div>

                        {/* Content */}
                        <div className="p-6">
                            <div className="prose prose-invert prose-sm max-w-none text-muted mb-6">
                                <p>{issue.description || 'No detailed description provided.'}</p>
                                <p className="font-semibold text-text mt-2">Suggestion: <span className="font-normal text-muted">Review the logic flow and ensure state changes verify permissions.</span></p>
                            </div>

                            {/* Code Snippet - Only if available in raw data (assuming Slither output sometimes has it or we pass it) */}
                            <div className="rounded-lg overflow-hidden border border-border bg-[#0d1117]">
                                <div className="px-4 py-2 bg-border/20 text-xs font-mono text-muted border-b border-border flex items-center justify-between">
                                    <span>Source Preview</span>
                                    <span>Solidity</span>
                                </div>
                                <SyntaxHighlighter
                                    language="solidity"
                                    style={vscDarkPlus}
                                    customStyle={{ margin: 0, fontSize: 13, background: 'transparent' }}
                                    showLineNumbers={true}
                                    wrapLines={true}
                                >
                                    {issue.code || "// Code snippet not available in raw report."}
                                </SyntaxHighlighter>
                            </div>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
