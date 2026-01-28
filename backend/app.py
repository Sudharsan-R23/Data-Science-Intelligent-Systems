"""
Flask Backend API for Healthcare Diagnosis Decision Support System
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import logging
from pathlib import Path
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load model and preprocessor
MODEL_PATH = Path("ml_models/models/best_model.pkl")
PREPROCESSOR_PATH = Path("ml_models/models/preprocessor.pkl")

model = None
preprocessor = None


def load_model():
    """Load the trained model."""
    global model
    try:
        if MODEL_PATH.exists():
            model = joblib.load(MODEL_PATH)
            logger.info(f"Model loaded from {MODEL_PATH}")
        else:
            logger.warning(f"Model not found at {MODEL_PATH}")
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")


def load_preprocessor():
    """Load the preprocessor."""
    global preprocessor
    try:
        if PREPROCESSOR_PATH.exists():
            preprocessor = joblib.load(PREPROCESSOR_PATH)
            logger.info(f"Preprocessor loaded from {PREPROCESSOR_PATH}")
        else:
            logger.warning(f"Preprocessor not found at {PREPROCESSOR_PATH}")
    except Exception as e:
        logger.error(f"Error loading preprocessor: {str(e)}")


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'preprocessor_loaded': preprocessor is not None
    })


@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict diagnosis based on patient data.
    
    Expected JSON format:
    {
        "features": {
            "feature1": value1,
            "feature2": value2,
            ...
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({'error': 'Invalid request. Expected "features" key.'}), 400
        
        features = data['features']
        
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # Check if model is loaded
        if model is None:
            return jsonify({
                'error': 'Model not loaded. Please train the model first. Make sure best_model.pkl exists in ml_models/models/'
            }), 500
        
        # Preprocess if preprocessor is available
        if preprocessor:
            try:
                # Apply preprocessing steps
                df_processed = preprocess_data(df, preprocessor)
            except Exception as preprocess_error:
                logger.error(f"Preprocessing error: {str(preprocess_error)}")
                return jsonify({
                    'error': f'Preprocessing failed: {str(preprocess_error)}. Check if feature names match the training data.'
                }), 500
        else:
            logger.warning("Preprocessor not loaded, using raw data")
            df_processed = df
        
        # Check if DataFrame has required columns
        if df_processed.empty:
            return jsonify({
                'error': 'Processed data is empty. Check feature names and values.'
            }), 500
        
        try:
            prediction = model.predict(df_processed)[0]
            prediction_proba = model.predict_proba(df_processed)[0]
        except Exception as predict_error:
            logger.error(f"Prediction error: {str(predict_error)}")
            logger.error(f"DataFrame columns: {df_processed.columns.tolist()}")
            logger.error(f"DataFrame shape: {df_processed.shape}")
            return jsonify({
                'error': f'Prediction failed: {str(predict_error)}. Expected features: {df_processed.columns.tolist()}'
            }), 500
        
        # Get feature importance if available
        feature_importance = None
        if hasattr(model, 'feature_importances_'):
            feature_names = df_processed.columns.tolist()
            importances = model.feature_importances_
            feature_importance = dict(zip(feature_names, importances.tolist()))
        
        # Generate recommendation
        probability = float(max(prediction_proba))
        recommendation = generate_recommendation(prediction, probability)
        
        response = {
            'prediction': int(prediction),
            'prediction_label': 'Positive' if prediction == 1 else 'Negative',
            'probability': probability,
            'probabilities': {
                'negative': float(prediction_proba[0]),
                'positive': float(prediction_proba[1]) if len(prediction_proba) > 1 else float(prediction_proba[0])
            },
            'recommendation': recommendation,
            'feature_importance': feature_importance,
            'disclaimer': 'This is a decision support system. All predictions should be reviewed by qualified healthcare professionals.'
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500


def preprocess_data(df, preprocessor_data):
    """
    Apply preprocessing steps to input data.
    
    Args:
        df (pd.DataFrame): Input dataframe
        preprocessor_data (dict): Preprocessor data loaded from file
    
    Returns:
        pd.DataFrame: Preprocessed dataframe
    """
    df_processed = df.copy()
    
    # Handle missing values
    if preprocessor_data.get('imputer'):
        numerical_cols = preprocessor_data.get('numerical_columns', [])
        if numerical_cols:
            df_processed[numerical_cols] = preprocessor_data['imputer'].transform(
                df_processed[numerical_cols]
            )
    
    # Encode categorical variables
    if preprocessor_data.get('label_encoders'):
        for col, encoder in preprocessor_data['label_encoders'].items():
            if col in df_processed.columns:
                df_processed[col] = encoder.transform(df_processed[col].astype(str))
    
    # Normalize features
    if preprocessor_data.get('scaler'):
        numerical_cols = preprocessor_data.get('numerical_columns', [])
        if numerical_cols:
            df_processed[numerical_cols] = preprocessor_data['scaler'].transform(
                df_processed[numerical_cols]
            )
    
    # Feature selection
    if preprocessor_data.get('feature_selector'):
        selected_features = preprocessor_data.get('selected_features')
        if selected_features:
            df_processed = df_processed[selected_features]
    
    return df_processed


def generate_recommendation(prediction, probability):
    """
    Generate medical recommendation based on prediction.
    
    Args:
        prediction (int): Predicted class (0 or 1)
        probability (float): Prediction probability
    
    Returns:
        str: Recommendation text
    """
    if prediction == 1:
        if probability >= 0.8:
            return "High probability of positive diagnosis. Immediate medical consultation recommended. Consider additional diagnostic tests."
        elif probability >= 0.6:
            return "Moderate probability of positive diagnosis. Medical consultation recommended. Monitor symptoms closely."
        else:
            return "Low-moderate probability. Consider follow-up tests and regular monitoring."
    else:
        if probability >= 0.8:
            return "Low probability of condition. Continue regular health monitoring. Maintain healthy lifestyle."
        else:
            return "Low probability, but regular check-ups are recommended. Monitor any changes in symptoms."


@app.route('/api/features', methods=['GET'])
def get_features():
    """Get list of required features for prediction."""
    # This should be dynamically generated based on the model
    # For now, return a sample structure
    return jsonify({
        'features': [
            {
                'name': 'age',
                'type': 'numeric',
                'description': 'Patient age',
                'required': True
            },
            {
                'name': 'gender',
                'type': 'categorical',
                'description': 'Patient gender',
                'required': True,
                'options': ['Male', 'Female']
            }
            # Add more features based on your dataset
        ]
    })


if __name__ == '__main__':
    # Load model and preprocessor on startup
    load_model()
    load_preprocessor()
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
