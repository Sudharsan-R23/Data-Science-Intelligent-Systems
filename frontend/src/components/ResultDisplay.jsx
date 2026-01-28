import React from 'react';

const ResultDisplay = ({ result, onReset }) => {
    if (!result) return null;

    const isHighRisk = result.prediction === 1;
    const healthScore = Math.round((1 - result.probability) * 100);

    return (
        <div className="animate-fade-in lg:grid lg:grid-cols-2 lg:gap-12">
            {/* Left Column: Result Summary */}
            <div className="space-y-8">
                <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4">
                        <button onClick={onReset} className="w-12 h-12 rounded-2xl bg-brand-surface/50 border border-white/5 flex items-center justify-center text-brand-accent hover:bg-brand-surface transition-all">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 19l-7-7 7-7" />
                            </svg>
                        </button>
                        <h2 className="text-2xl font-bold text-brand-text">Diagnostic Report</h2>
                    </div>
                </div>

                <div className="card-premium text-center relative overflow-hidden bg-brand-surface/40">
                    <p className="text-[10px] font-black text-brand-accent/40 uppercase tracking-[0.2em] mb-8">Patient Health Index</p>
                    <div className="relative w-48 h-48 mx-auto mb-8">
                        <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
                            <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth="6" />
                            <circle
                                cx="50" cy="50" r="45" fill="none"
                                stroke={isHighRisk ? "var(--color-brand-primary)" : "var(--color-brand-accent)"}
                                strokeWidth="6"
                                strokeDasharray="283"
                                strokeDashoffset={283 - (283 * (1 - result.probability))}
                                strokeLinecap="round"
                                className="progress-ring shadow-lg"
                            />
                        </svg>
                        <div className="absolute inset-0 flex flex-col items-center justify-center">
                            <span className={`text-5xl font-black ${isHighRisk ? 'text-brand-primary' : 'text-brand-accent'}`}>
                                {healthScore}%
                            </span>
                            <span className="text-[10px] font-black text-brand-accent/40 uppercase tracking-[0.2em] mt-1">Status OK</span>
                        </div>
                    </div>
                    <div className="inline-block px-6 py-2 rounded-full bg-brand-bg/40 border border-white/5 text-[10px] font-black uppercase tracking-widest text-brand-accent/60">
                        Reliability: {(result.confidence * 100).toFixed(1)}%
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-6">
                    <div className="p-6 rounded-4xl bg-brand-surface/30 border border-white/5">
                        <p className="text-[10px] font-black text-brand-accent/40 uppercase mb-2 tracking-widest">Diagnosis</p>
                        <p className="font-bold text-brand-text leading-tight text-lg">{result.diagnosis}</p>
                    </div>
                    <div className={`p-6 rounded-4xl border border-white/5 ${isHighRisk ? 'bg-brand-primary/10' : 'bg-brand-accent/10'}`}>
                        <p className={`text-[10px] font-black ${isHighRisk ? 'text-brand-primary' : 'text-brand-accent'} uppercase mb-2 tracking-widest`}>Risk Assessment</p>
                        <p className={`font-bold ${isHighRisk ? 'text-brand-primary' : 'text-brand-accent'} leading-tight text-lg`}>{result.risk_level}</p>
                    </div>
                </div>
            </div>

            {/* Right Column: Recommendations */}
            <div className="mt-12 lg:mt-0 flex flex-col justify-between">
                <div>
                    <div className="flex items-center justify-between mb-8">
                        <h3 className="text-xl font-bold text-brand-text">Medical Protocols</h3>
                        <span className="text-xs font-black text-brand-primary uppercase tracking-widest">v4.0.2</span>
                    </div>

                    <div className="space-y-4">
                        {result.recommendations.map((rec, index) => (
                            <div key={index} className="flex items-center p-5 bg-brand-surface/20 border border-white/5 rounded-3xl group hover:bg-brand-surface/40 transition-all">
                                <div className={`w-2 h-2 rounded-full mr-5 ${isHighRisk ? 'bg-brand-primary' : 'bg-brand-accent'}`}></div>
                                <div className="flex-1">
                                    <p className="text-sm font-bold text-brand-text/90 group-hover:text-white transition-colors">{rec}</p>
                                    <p className="text-[10px] text-brand-accent/30 font-bold uppercase tracking-tighter mt-1">Clinical Directive</p>
                                </div>
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-brand-accent/20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                                </svg>
                            </div>
                        ))}
                    </div>
                </div>

                <button onClick={onReset} className="w-full btn-secondary mt-12 py-5 lg:mb-0 mb-10 group">
                    <span className="flex items-center justify-center space-x-3">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 group-hover:-rotate-45 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                        </svg>
                        <span className="uppercase tracking-[0.2em] text-xs font-black">Begin New Diagnosis</span>
                    </span>
                </button>
            </div>
        </div>

    );
};

export default ResultDisplay;
