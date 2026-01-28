import React, { useState, useEffect } from 'react';
import InputForm from './components/InputForm';
import ResultDisplay from './components/ResultDisplay';
import { checkHealth, predictDiabetes, predictHeartDisease } from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState('diabetes');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking');

  useEffect(() => {
    const verifyBackend = async () => {
      try {
        await checkHealth();
        setApiStatus('online');
      } catch (err) {
        setApiStatus('offline');
      }
    };
    verifyBackend();
  }, []);

  const handlePrediction = async (data) => {
    setLoading(true);
    try {
      let response;
      if (activeTab === 'diabetes') {
        response = await predictDiabetes(data);
      } else {
        response = await predictHeartDisease(data);
      }
      setResult(response);
    } catch (error) {
      alert("Error: " + (error.response?.data?.detail || "System offline"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-100 min-h-screen md:py-10">
      <div className="app-container">
        {/* Header Section */}
        <header className="px-8 pt-10 pb-6 flex items-center justify-between">
          <div>
            <p className="text-slate-400 font-medium text-sm">Good Day, Specialist!</p>
            <h1 className="text-2xl font-bold text-slate-800">Analyze Health Data</h1>
          </div>
          <div className="w-12 h-12 bg-slate-100 rounded-2xl flex items-center justify-center overflow-hidden border border-slate-200">
            <div className="w-full h-full bg-brand-blue flex items-center justify-center text-white">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          </div>
        </header>

        {/* Main Banner / Interactive Card */}
        {!result && (
          <div className="px-8 mb-8">
            <div className="bg-brand-lightblue p-6 rounded-4xl relative overflow-hidden group">
              <div className="relative z-10 w-2/3">
                <h2 className="text-xl font-bold text-brand-navy mb-2 leading-tight">Predict Disease Risk in Realtime.</h2>
                <p className="text-xs text-brand-blue mb-4 font-semibold uppercase tracking-wider">Clinical AI Engine</p>
                <button className="bg-white text-brand-blue px-6 py-2 rounded-xl text-xs font-bold shadow-sm">Learn More</button>
              </div>
              <div className="absolute right-0 bottom-0 top-0 w-1/3 flex items-center justify-center">
                <div className="w-20 h-20 bg-brand-blue/10 rounded-full animate-pulse blur-xl"></div>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-24 w-24 text-brand-blue/20 absolute -right-4 -bottom-4 rotate-12" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                </svg>
              </div>
            </div>
          </div>
        )}

        {/* Tab Selection */}
        {!result && (
          <div className="px-8 mb-6">
            <h3 className="text-lg font-bold text-slate-800 mb-4">Diagnosis Type</h3>
            <div className="flex space-x-6 border-b border-slate-100">
              <button
                onClick={() => setActiveTab('diabetes')}
                className={activeTab === 'diabetes' ? 'tab-active' : 'tab-inactive'}
              >
                Diabetes
              </button>
              <button
                onClick={() => setActiveTab('heart')}
                className={activeTab === 'heart' ? 'tab-active' : 'tab-inactive'}
              >
                Heart Disease
              </button>
            </div>
          </div>
        )}

        {/* Dynamic Content */}
        <div className="flex-1 px-8 pb-32">
          {!result ? (
            <InputForm
              modelType={activeTab}
              onSubmit={handlePrediction}
              loading={loading}
            />
          ) : (
            <ResultDisplay result={result} onReset={() => setResult(null)} />
          )}
        </div>

        {/* Bottom Navigation */}
        <nav className="absolute bottom-0 left-0 right-0 h-24 bg-white/80 backdrop-blur-lg border-t border-slate-100 px-8 flex items-center justify-between">
          <div className="nav-item-active" onClick={() => setResult(null)}>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="currentColor" viewBox="0 0 24 24">
              <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
            </svg>
          </div>
          <div className="nav-item">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <div className="nav-item">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <div className="nav-item">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
        </nav>
      </div>
    </div>
  );
}

export default App;
