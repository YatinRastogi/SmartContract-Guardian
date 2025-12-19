import React, { useState } from 'react';
import ReactDiffViewer from 'react-diff-viewer-continued';
import { FileCode, ArrowRightLeft } from 'lucide-react';

// Simple style override for dark mode diff
const styles = {
    variables: {
        dark: {
            diffViewerBackground: '#0d1117',
            diffViewerColor: '#c9d1d9',
            addedBackground: '#1f6feb20',
            addedColor: '#c9d1d9',
            removedBackground: '#da363320',
            removedColor: '#c9d1d9',
            wordAddedBackground: '#1f6feb40',
            wordRemovedBackground: '#da363340',
            addedGutterBackground: '#1f6feb10',
            removedGutterBackground: '#da363310',
            gutterBackground: '#0d1117',
            gutterColor: '#484f58',
        }
    }
};

export default function DiffViewer({ originalCode, fixedCode }) {
    if (!originalCode || !fixedCode) return null;

    return (
        <div className="border border-border rounded-xl overflow-hidden bg-surface">
            <div className="flex items-center justify-between px-4 py-3 bg-surface border-b border-border">
                <div className="flex items-center gap-2 text-sm font-bold text-white">
                    <FileCode size={16} className="text-muted" />
                    <span>Source Diff</span>
                </div>
                <div className="flex items-center gap-4 text-xs font-mono text-muted">
                    <span className="flex items-center gap-1.5 text-alert"><span className="w-2 h-2 rounded-full bg-alert"></span> Original</span>
                    <span className="flex items-center gap-1.5 text-secondary"><span className="w-2 h-2 rounded-full bg-secondary"></span> Smart Fix</span>
                </div>
            </div>
            <div className="max-h-[600px] overflow-auto custom-scrollbar">
                <ReactDiffViewer
                    oldValue={originalCode}
                    newValue={fixedCode}
                    splitView={true}
                    useDarkTheme={true}
                    styles={styles}
                    hideLineNumbers={false}
                    leftTitle="Vulnerable Contract"
                    rightTitle="Secured Contract"
                />
            </div>
        </div>
    );
}
