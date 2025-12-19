import React from 'react';
import { Search, BrainCircuit, ShieldAlert, Lock, Zap, FileText, Check } from 'lucide-react';

const STEPS = [
    { id: 1, label: 'Detective', icon: Search },
    { id: 2, label: 'Verifier', icon: BrainCircuit },
    { id: 3, label: 'Auditor', icon: ShieldAlert },
    { id: 4, label: 'Gatekeeper', icon: Lock },
    { id: 5, label: 'Red Team', icon: Zap },
    { id: 6, label: 'Reporting', icon: FileText },
];

export default function AgentStepper({ status }) {
    // Mock progress based on status, real logic would parsing logs or explicit backend state
    const getCurrentStep = () => {
        if (status === 'completed') return 7;
        if (status === 'idle') return 0;
        return 3; // Default 'busy' state mockup if status doesn't give granular info yet
    };

    const currentStep = getCurrentStep();

    return (
        <div className="w-full bg-surface border-y border-border py-8 px-12 mb-8">
            <div className="flex justify-between relative max-w-5xl mx-auto">
                {/* Connecting Line */}
                <div className="absolute top-1/2 left-0 w-full h-0.5 bg-border -z-0"></div>
                <div
                    className="absolute top-1/2 left-0 h-0.5 bg-primary transition-all duration-1000 -z-0"
                    style={{ width: status === 'completed' ? '100%' : status === 'scanning' ? '40%' : '0%' }}
                ></div>

                {STEPS.map((step) => {
                    const isCompleted = status === 'completed' || (status === 'scanning' && step.id < 3); // Mock logic
                    const isActive = status === 'scanning' && step.id === 3; // Mock logic

                    return (
                        <div key={step.id} className="relative z-10 flex flex-col items-center gap-3">
                            <div className={`w-12 h-12 rounded-xl flex items-center justify-center border-2 transition-all duration-500 bg-surface ${isActive
                                ? 'border-primary text-primary shadow-[0_0_20px_rgba(35,134,54,0.4)] scale-110'
                                : isCompleted
                                    ? 'border-primary bg-primary text-white'
                                    : 'border-border text-muted'
                                }`}>
                                {isCompleted ? <Check size={20} strokeWidth={3} /> : <step.icon size={20} />}
                            </div>
                            <span className={`text-xs font-bold uppercase tracking-wider ${isActive || isCompleted ? 'text-text' : 'text-muted/50'}`}>
                                {step.label}
                            </span>
                        </div>
                    );
                })}
            </div>

            {status === 'scanning' && (
                <div className="text-center mt-6">
                    <span className="text-sm text-primary font-mono animate-pulse">
                        &gt; Executing deep analysis patterns...
                    </span>
                </div>
            )}
        </div>
    );
}
