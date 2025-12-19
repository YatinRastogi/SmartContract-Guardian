import React, { useState, useEffect } from 'react';
import { ShieldCheck, Timer, Wifi } from 'lucide-react';

export default function Header({ status }) {
    const [seconds, setSeconds] = useState(0);

    useEffect(() => {
        let interval;
        if (status === 'scanning') {
            interval = setInterval(() => setSeconds(s => s + 1), 1000);
        } else if (status === 'idle') {
            setSeconds(0);
        }
        return () => clearInterval(interval);
    }, [status]);

    return (
        <header className="flex items-center justify-between px-8 py-5 border-b border-border bg-surface/50 backdrop-blur-md sticky top-0 z-40">
            {/* Branding */}
            <div className="flex items-center gap-4">
                <div className="bg-primary/10 p-2.5 rounded-lg border border-primary/20 shadow-[0_0_15px_rgba(35,134,54,0.1)]">
                    <ShieldCheck className="text-primary w-6 h-6" />
                </div>
                <div>
                    <h1 className="text-xl font-bold text-white tracking-tight">SmartContract Guardian</h1>
                    <p className="text-[10px] text-muted font-mono uppercase tracking-widest">AI Security Pipeline v1.0</p>
                </div>
            </div>

            {/* System Status & Timer */}
            <div className="flex items-center gap-6">
                {(status === 'scanning' || status === 'completed') && (
                    <div className={`flex items-center gap-2 px-4 py-1.5 rounded-full border ${status === 'completed' ? 'bg-primary/10 border-primary/30 text-primary' : 'bg-background border-border text-text'}`}>
                        <Timer size={14} className={status === 'scanning' ? 'text-secondary animate-pulse' : 'text-primary'} />
                        <span className="text-xs font-mono">
                            {status === 'scanning' ? `Scanning: ${seconds}s` : `Audit Completed in ${seconds}s`}
                        </span>
                    </div>
                )}

                <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${status === 'scanning' ? 'bg-alert animate-ping' : status === 'completed' ? 'bg-primary' : 'bg-secondary'}`}></div>
                    <span className="text-xs font-semibold text-muted uppercase tracking-wider">
                        System: {status === 'idle' ? 'Ready' : status === 'scanning' ? 'Active' : 'Report Ready'}
                    </span>
                </div>
            </div>
        </header>
    );
}
