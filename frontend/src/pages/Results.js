import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Results() {
  const navigate = useNavigate();
  const [result, setResult] = useState(null);

  useEffect(() => {
    const storedResult = localStorage.getItem('diagnosisResult');
    if (storedResult) {
      setResult(JSON.parse(storedResult));
    } else {
      navigate('/');
    }
  }, [navigate]);

  if (!result) {
    return <div className="text-center py-12">Loading...</div>;
  }

  const { prediction_label, probability, probabilities, recommendation, feature_importance, disclaimer } = result;
  const isPositive = prediction_label === 'Positive';

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-xl p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">
          Diagnosis Results
        </h2>

        {/* Prediction Card */}
        <div className={`rounded-lg p-6 mb-6 ${
          isPositive ? 'bg-red-50 border-2 border-red-200' : 'bg-green-50 border-2 border-green-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-700 mb-2">
                Prediction: <span className={isPositive ? 'text-red-700' : 'text-green-700'}>
                  {prediction_label}
                </span>
              </h3>
              <p className="text-gray-600">
                Confidence: {(probability * 100).toFixed(2)}%
              </p>
            </div>
            <div className={`text-4xl ${isPositive ? 'text-red-500' : 'text-green-500'}`}>
              {isPositive ? '⚠️' : '✓'}
            </div>
          </div>
        </div>

        {/* Probability Breakdown */}
        <div className="bg-gray-50 rounded-lg p-6 mb-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">
            Probability Breakdown
          </h3>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm text-gray-600">Negative</span>
                <span className="text-sm font-medium text-gray-700">
                  {(probabilities.negative * 100).toFixed(2)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-gray-600 h-2 rounded-full"
                  style={{ width: `${probabilities.negative * 100}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-sm text-gray-600">Positive</span>
                <span className="text-sm font-medium text-gray-700">
                  {(probabilities.positive * 100).toFixed(2)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className={`h-2 rounded-full ${isPositive ? 'bg-red-500' : 'bg-green-500'}`}
                  style={{ width: `${probabilities.positive * 100}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Recommendation */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
          <h3 className="text-lg font-semibold text-blue-800 mb-2">
            Medical Recommendation
          </h3>
          <p className="text-blue-700">{recommendation}</p>
        </div>

        {/* Feature Importance */}
        {feature_importance && (
          <div className="bg-gray-50 rounded-lg p-6 mb-6">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">
              Key Contributing Factors
            </h3>
            <div className="space-y-2">
              {Object.entries(feature_importance)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 5)
                .map(([feature, importance]) => (
                  <div key={feature} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 capitalize">
                      {feature.replace(/_/g, ' ')}
                    </span>
                    <div className="flex items-center space-x-2">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: `${importance * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-gray-500 w-12 text-right">
                        {(importance * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}

        {/* Disclaimer */}
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <p className="text-sm text-yellow-800">
            <strong>⚠️ Important:</strong> {disclaimer}
          </p>
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-4">
          <button
            onClick={() => navigate('/')}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            New Diagnosis
          </button>
        </div>
      </div>
    </div>
  );
}

export default Results;
