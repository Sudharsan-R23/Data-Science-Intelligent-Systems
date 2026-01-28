import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DiagnosisForm from './pages/DiagnosisForm';
import Results from './pages/Results';
import './App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <header className="bg-white shadow-md">
          <div className="container mx-auto px-4 py-6">
            <h1 className="text-3xl font-bold text-gray-800">
              Healthcare Diagnosis Decision Support System
            </h1>
            <p className="text-gray-600 mt-2">
              AI-Powered Medical Diagnosis Assistant
            </p>
          </div>
        </header>
        
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<DiagnosisForm />} />
            <Route path="/results" element={<Results />} />
          </Routes>
        </main>
        
        <footer className="bg-white mt-12 py-6 border-t">
          <div className="container mx-auto px-4 text-center text-gray-600">
            <p className="text-sm">
              ⚠️ This is a Decision Support System. All predictions must be reviewed by qualified healthcare professionals.
            </p>
            <p className="text-xs mt-2">
              Academic Project - For Educational Purposes Only
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
