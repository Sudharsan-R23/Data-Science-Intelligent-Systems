import React from 'react';

const ResultDisplay = ({ result, onReset }) => {
    if (!result) return null;

    const isHighRisk = result.prediction === 1;
    const healthScore = Math.round((1 - result.probability) * 100);

    return (
        <div className="animate-fade-in">
            {/* Details Activities Header Style */}
            <div className="flex items-center justify-between mb-8">
                <div className="flex items-center space-x-4">
                    <button onClick={onReset} className="w-10 h-10 rounded-xl bg-slate-100 flex items-center justify-center text-slate-400">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 19l-7-7 7-7" />
                        </svg>
                    </button>
                    <h2 className="text-xl font-bold text-slate-800">Diagnostic Result</h2>
                </div>
                <p className="text-xs font-bold text-slate-400">v1.2.0</p>
            </div>

            {/* Giant Health Score Chart (matches middle screen in example) */}
            <div className="card-premium mb-8 text-center bg-gradient-to-br from-white to-slate-50 relative overflow-hidden">
                <p className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-6">Patient Health Index</p>
                <div className="relative w-40 h-40 mx-auto mb-6">
                    <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="45" fill="none" stroke="#f1f5f9" strokeWidth="8" />
                        <circle
                            cx="50" cy="50" r="45" fill="none"
                            stroke={isHighRisk ? "#ff6b35" : "#2563eb"}
                            strokeWidth="8"
                            strokeDasharray="283"
                            strokeDashoffset={283 - (283 * (1 - result.probability))}
                            strokeLinecap="round"
                            className="progress-ring"
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className={`text-4xl font-black ${isHighRisk ? 'text-brand-orange' : 'text-brand-blue'}`}>
                            {healthScore}%
                        </span>
                        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">Healthy</span>
                    </div>
                </div>
                <div className="inline-block px-4 py-1.5 rounded-full bg-slate-100 text-[10px] font-black uppercase tracking-widest text-slate-500">
                    Confidence: {result.confidence}
                </div>
            </div>

            {/* Recommendation List (matches right screen list style) */}
            <div className="mb-10">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="font-bold text-slate-800">Protocol Advice</h3>
                    <span className="text-xs font-bold text-brand-blue">View All</span>
                </div>

                <div className="space-y-4">
                    {result.recommendations.map((rec, index) => (
                        <div key={index} className="flex items-center p-4 bg-white border border-slate-50 rounded-2xl shadow-sm space-x-4">
                            <div className={`w-3 h-3 rounded-full ${isHighRisk ? 'bg-brand-orange' : 'bg-brand-blue'}`}></div>
                            <div className="flex-1">
                                <p className="text-sm font-bold text-slate-800">{rec}</p>
                                <p className="text-[10px] text-slate-400 font-medium">Standard medical guideline</p>
                            </div>
                            <div className="px-3 py-1 bg-slate-50 rounded-lg text-[10px] font-bold text-slate-400">
                                INFO
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Summary Boxes (matches small footer boxes in example) */}
            <div className="grid grid-cols-2 gap-4 mb-10">
                <div className="p-5 rounded-3xl bg-brand-lightblue">
                    <p className="text-[10px] font-black text-brand-blue uppercase mb-1">Status</p>
                    <p className="font-bold text-brand-navy leading-tight">{result.diagnosis}</p>
                </div>
                <div className={`p-5 rounded-3xl ${isHighRisk ? 'bg-brand-lightorange' : 'bg-slate-100'}`}>
                    <p className={`text-[10px] font-black ${isHighRisk ? 'text-brand-orange' : 'text-slate-400'} uppercase mb-1`}>Risk Level</p>
                    <p className={`font-bold ${isHighRisk ? 'text-brand-orange' : 'text-slate-600'} leading-tight`}>{result.risk_level}</p>
                </div>
            </div>

            <button onClick={onReset} className="w-full btn-secondary mb-10">
                New Patient Analysis
            </button>
        </div>
    );
};

export default ResultDisplay;
