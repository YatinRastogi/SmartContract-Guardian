import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { CloudUpload, FileCode, Shield } from 'lucide-react';

export default function UploadZone({ onUpload }) {
    const onDrop = useCallback((acceptedFiles) => {
        if (acceptedFiles.length > 0) {
            onUpload(acceptedFiles[0]);
        }
    }, [onUpload]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'text/sol': ['.sol'] },
        multiple: false
    });

    return (
        <div className="max-w-2xl mx-auto mt-20">
            <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-2xl p-16 text-center transition-all cursor-pointer group ${isDragActive
                        ? 'border-primary bg-primary/5'
                        : 'border-border bg-surface hover:border-text/30'
                    }`}
            >
                <input {...getInputProps()} />

                <div className="relative inline-block mb-8">
                    <div className={`absolute inset-0 bg-secondary/20 blur-xl rounded-full transition-opacity ${isDragActive ? 'opacity-100' : 'opacity-0 group-hover:opacity-50'}`}></div>
                    <CloudUpload size={64} className={`relative z-10 transition-colors ${isDragActive ? 'text-primary' : 'text-muted group-hover:text-text'}`} />
                </div>

                <h2 className="text-2xl font-bold text-white mb-3">Initiate Security Audit</h2>
                <p className="text-muted mb-8 max-w-sm mx-auto">
                    Drag & drop your solidity smart contract here, or click to browse files.
                </p>

                <button className="px-8 py-3 bg-primary hover:bg-green-600 text-white font-semibold rounded-lg shadow-lg shadow-green-900/20 transition-all flex items-center gap-2 mx-auto">
                    <Shield size={18} />
                    Start 6-Agent Scan
                </button>

                <div className="mt-8 flex items-center justify-center gap-4 text-xs text-muted/60 font-mono">
                    <span className="flex items-center gap-1"><FileCode size={12} /> .sol supported</span>
                    <span>•</span>
                    <span>Max 5MB</span>
                </div>
            </div>
        </div>
    );
}
