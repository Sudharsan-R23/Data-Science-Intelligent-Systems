import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import FeatureInput from '../components/FeatureInput';

// API Configuration
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function DiagnosisForm() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    age: '',
    gender: '',
    // Add more fields based on your dataset
    // Example for diabetes:
    pregnancies: '',
    glucose: '',
    blood_pressure: '',
    skin_thickness: '',
    insulin: '',
    bmi: '',
    diabetes_pedigree: '',
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Convert form data to numeric values
      const features = {};
      Object.keys(formData).forEach(key => {
        const value = formData[key];
        if (value === '') {
          features[key] = null;
        } else if (key === 'gender') {
          features[key] = value; // Keep as string for categorical
        } else {
          features[key] = parseFloat(value);
        }
      });

      const response = await axios.post(`${API_URL}/api/predict`, {
        features: features
      });

      // Store results and navigate
      localStorage.setItem('diagnosisResult', JSON.stringify(response.data));
      navigate('/results');
    } catch (err) {
      let errorMessage = 'An error occurred. Please try again.';
      
      if (err.response) {
        // Server responded with error
        errorMessage = err.response.data?.error || `Server error: ${err.response.status}`;
      } else if (err.request) {
        // Request made but no response
        errorMessage = 'Cannot connect to server. Please make sure the backend is running on http://localhost:5000';
      } else {
        // Something else happened
        errorMessage = err.message || 'An unexpected error occurred';
      }
      
      setError(errorMessage);
      console.error('Prediction error:', err);
      console.error('Error details:', {
        message: err.message,
        response: err.response?.data,
        status: err.response?.status
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-xl p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">
          Patient Information Form
        </h2>
        
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <FeatureInput
              label="Age"
              name="age"
              type="number"
              value={formData.age}
              onChange={handleChange}
              required
              min="0"
              max="120"
            />

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Gender
              </label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>

            {/* Add more feature inputs based on your dataset */}
            {/* Example fields for diabetes dataset */}
            <FeatureInput
              label="Glucose Level (mg/dL)"
              name="glucose"
              type="number"
              value={formData.glucose}
              onChange={handleChange}
              min="0"
              step="0.1"
            />

            <FeatureInput
              label="Blood Pressure (mmHg)"
              name="blood_pressure"
              type="number"
              value={formData.blood_pressure}
              onChange={handleChange}
              min="0"
            />

            <FeatureInput
              label="BMI"
              name="bmi"
              type="number"
              value={formData.bmi}
              onChange={handleChange}
              min="0"
              step="0.1"
            />

            <FeatureInput
              label="Insulin Level (μU/mL)"
              name="insulin"
              type="number"
              value={formData.insulin}
              onChange={handleChange}
              min="0"
            />
          </div>

          <div className="flex justify-end space-x-4 pt-4">
            <button
              type="button"
              onClick={() => setFormData({
                age: '', gender: '', pregnancies: '', glucose: '',
                blood_pressure: '', skin_thickness: '', insulin: '',
                bmi: '', diabetes_pedigree: ''
              })}
              className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition"
            >
              Clear
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {loading ? 'Processing...' : 'Get Diagnosis'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default DiagnosisForm;
