import React from 'react';
import { Shield, CheckCircle, Cpu, Lock, Activity, Server } from 'lucide-react';

const steps = [
    { id: 1, name: 'Detection', icon: Shield },
    { id: 2, name: 'AI Logic', icon: Cpu },
    { id: 3, name: 'Gatekeeper', icon: Lock },
    { id: 4, name: 'Red Team', icon: Activity },
];

export default function Sidebar({ status }) {
    const getCurrentPhase = () => {
        if (status === 'completed') return 5;
        if (status === 'idle') return 0;

        // Simple logic mapping
        if (status === 'scanning') return 2;
        return 1;
    };

    const currentStep = getCurrentPhase();

    return (
        <div className="w-80 h-screen bg-slate-900 border-r border-slate-800 flex flex-col fixed left-0 top-0 z-50">
            {/* Logo */}
            <div className="p-6 border-b border-slate-800 flex items-center gap-3">
                <div className="p-2 bg-blue-500/10 rounded-lg">
                    <Server className="text-cyan-400 w-6 h-6" />
                </div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">
                    SmartAudit
                </h1>
            </div>

            {/* Stepper */}
            <div className="flex-1 p-8 space-y-8 overflow-y-auto">
                {steps.map((step, index) => {
                    const isActive = currentStep >= step.id;
                    const isCompleted = currentStep > step.id;
                    const Icon = step.icon;

                    return (
                        <div key={step.id} className="relative flex items-center gap-4">
                            {/* Connector Line */}
                            {index !== steps.length - 1 && (
                                <div className={`absolute left-5 top-10 w-0.5 h-12 transition-colors duration-500 ${isCompleted ? 'bg-cyan-500' : 'bg-slate-800'}`} />
                            )}

                            <div
                                className={`z-10 w-10 h-10 rounded-full flex items-center justify-center border-2 transition-all duration-500 ${isActive
                                        ? 'border-cyan-500 bg-cyan-950 text-cyan-400 shadow-[0_0_15px_rgba(6,182,212,0.3)]'
                                        : 'border-slate-800 bg-slate-900 text-slate-600'
                                    }`}
                            >
                                {isCompleted ? <CheckCircle size={18} /> : <Icon size={18} />}
                            </div>
                            <div>
                                <h3 className={`font-semibold text-sm ${isActive ? 'text-slate-200' : 'text-slate-600'}`}>
                                    {step.name}
                                </h3>
                                <p className="text-xs text-slate-500">
                                    {isActive ? (isCompleted ? 'Completed' : 'Processing...') : 'Pending'}
                                </p>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Terminal Removed as requested */}
        </div>
    );
}
