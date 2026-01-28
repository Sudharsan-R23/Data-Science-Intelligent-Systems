"""
FastAPI Backend for Healthcare Decision Support System
Provides REST API endpoints for ML-based diagnosis predictions
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
import pickle
import json
import numpy as np
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Decision Support System API",
    description="ML-powered decision support for diabetes and heart disease diagnosis",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models and metadata on startup
MODELS = {}
SCALERS = {}
METADATA = {}

def load_model_artifacts():
    """Load trained models, scalers, and metadata"""
    model_types = ['diabetes', 'heart_disease']
    
    for model_type in model_types:
        try:
            # Load model
            model_path = f"models/{model_type}_model.pkl"
            with open(model_path, 'rb') as f:
                MODELS[model_type] = pickle.load(f)
            
            # Load scaler
            scaler_path = f"models/{model_type}_scaler.pkl"
            with open(scaler_path, 'rb') as f:
                SCALERS[model_type] = pickle.load(f)
            
            # Load metadata
            metadata_path = f"models/{model_type}_metadata.json"
            with open(metadata_path, 'r') as f:
                METADATA[model_type] = json.load(f)
            
            print(f"✓ Loaded {model_type} model successfully")
        except Exception as e:
            print(f"⚠️ Failed to load {model_type} model: {e}")

# Load models at startup
load_model_artifacts()

# Pydantic Models for Request/Response

class DiabetesInput(BaseModel):
    """Input schema for diabetes prediction"""
    Pregnancies: int = Field(..., ge=0, le=20, description="Number of pregnancies")
    Glucose: float = Field(..., ge=0, le=300, description="Glucose level (mg/dL)")
    BloodPressure: float = Field(..., ge=0, le=200, description="Blood pressure (mm Hg)")
    SkinThickness: float = Field(..., ge=0, le=100, description="Skin thickness (mm)")
    Insulin: float = Field(..., ge=0, le=1000, description="Insulin level (μU/mL)")
    BMI: float = Field(..., ge=0, le=70, description="Body Mass Index")
    DiabetesPedigreeFunction: float = Field(..., ge=0, le=3, description="Diabetes pedigree function")
    Age: int = Field(..., ge=1, le=120, description="Age in years")
    
    class Config:
        schema_extra = {
            "example": {
                "Pregnancies": 2,
                "Glucose": 138,
                "BloodPressure": 78,
                "SkinThickness": 32,
                "Insulin": 120,
                "BMI": 31.2,
                "DiabetesPedigreeFunction": 0.42,
                "Age": 47
            }
        }

class HeartDiseaseInput(BaseModel):
    """Input schema for heart disease prediction"""
    Age: int = Field(..., ge=1, le=120, description="Age in years")
    Sex: int = Field(..., ge=0, le=1, description="Sex (0=Female, 1=Male)")
    ChestPainType: int = Field(..., ge=0, le=3, description="Chest pain type (0-3)")
    RestingBP: float = Field(..., ge=0, le=250, description="Resting blood pressure (mm Hg)")
    Cholesterol: float = Field(..., ge=0, le=600, description="Cholesterol (mg/dL)")
    FastingBS: int = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dL (0=No, 1=Yes)")
    RestingECG: int = Field(..., ge=0, le=2, description="Resting ECG results (0-2)")
    MaxHR: float = Field(..., ge=0, le=250, description="Maximum heart rate")
    ExerciseAngina: int = Field(..., ge=0, le=1, description="Exercise-induced angina (0=No, 1=Yes)")
    Oldpeak: float = Field(..., ge=0, le=10, description="ST depression")
    ST_Slope: int = Field(..., ge=0, le=2, description="ST slope (0-2)")
    
    class Config:
        schema_extra = {
            "example": {
                "Age": 55,
                "Sex": 1,
                "ChestPainType": 2,
                "RestingBP": 140,
                "Cholesterol": 250,
                "FastingBS": 1,
                "RestingECG": 1,
                "MaxHR": 150,
                "ExerciseAngina": 1,
                "Oldpeak": 2.3,
                "ST_Slope": 1
            }
        }

class PredictionResponse(BaseModel):
    """Response schema for predictions"""
    diagnosis: str
    prediction: int
    probability: float
    confidence: str
    risk_level: str
    recommendations: List[str]
    model_used: str
    feature_values: Dict

class ModelInfoResponse(BaseModel):
    """Response schema for model information"""
    model_name: str
    dataset: str
    features: List[str]
    metrics: Dict
    training_date: str

# Helper Functions

def get_recommendations(model_type: str, prediction: int, probability: float, 
                       feature_values: Dict) -> List[str]:
    """
    Generate medical recommendations based on prediction and features
    """
    recommendations = []
    
    if model_type == "diabetes":
        if prediction == 1:
            recommendations.append("⚠️ High risk of diabetes detected. Consult with an endocrinologist.")
            if feature_values.get('Glucose', 0) > 140:
                recommendations.append("🔴 Elevated glucose levels. Monitor blood sugar regularly.")
            if feature_values.get('BMI', 0) > 30:
                recommendations.append("💪 BMI indicates obesity. Consider weight management program.")
            if feature_values.get('Age', 0) > 45:
                recommendations.append("📅 Age is a risk factor. Regular screening recommended.")
            recommendations.append("🥗 Adopt a balanced diet low in simple carbohydrates.")
            recommendations.append("🏃 Regular physical activity (150 min/week recommended).")
        else:
            recommendations.append("✅ Low risk of diabetes. Continue healthy lifestyle.")
            recommendations.append("🔍 Regular check-ups recommended for preventive care.")
            if feature_values.get('BMI', 0) > 25:
                recommendations.append("⚖️ Maintain healthy weight to reduce future risk.")
    
    elif model_type == "heart_disease":
        if prediction == 1:
            recommendations.append("⚠️ Elevated risk of heart disease. Consult a cardiologist urgently.")
            if feature_values.get('Cholesterol', 0) > 240:
                recommendations.append("🔴 High cholesterol detected. Lipid-lowering therapy may be needed.")
            if feature_values.get('RestingBP', 0) > 140:
                recommendations.append("🩺 High blood pressure. Antihypertensive treatment recommended.")
            if feature_values.get('ExerciseAngina', 0) == 1:
                recommendations.append("💔 Exercise-induced chest pain requires immediate medical attention.")
            recommendations.append("💊 Medication adherence is crucial if prescribed.")
            recommendations.append("🚭 Avoid smoking and limit alcohol consumption.")
            recommendations.append("🧘 Stress management and adequate sleep are important.")
        else:
            recommendations.append("✅ Low risk of heart disease detected.")
            recommendations.append("❤️ Continue heart-healthy lifestyle choices.")
            recommendations.append("🏥 Regular cardiovascular screenings recommended.")
    
    # Always add disclaimer
    recommendations.append("⚕️ IMPORTANT: This is a decision support tool, not a replacement for professional medical advice.")
    
    return recommendations

def get_risk_level(probability: float) -> str:
    """Determine risk level based on probability"""
    if probability < 0.3:
        return "Low"
    elif probability < 0.6:
        return "Moderate"
    elif probability < 0.8:
        return "High"
    else:
        return "Very High"

def get_confidence(probability: float) -> str:
    """Determine confidence level"""
    confidence_score = max(probability, 1 - probability)
    if confidence_score > 0.9:
        return "Very High"
    elif confidence_score > 0.75:
        return "High"
    elif confidence_score > 0.6:
        return "Moderate"
    else:
        return "Low"

# API Routes

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Healthcare Decision Support System API",
        "version": "1.0.0",
        "available_models": list(MODELS.keys())
    }

@app.post("/predict/diabetes", response_model=PredictionResponse)
async def predict_diabetes(input_data: DiabetesInput):
    """
    Predict diabetes risk based on patient data
    """
    try:
        # Convert input to array
        features = np.array([[
            input_data.Pregnancies,
            input_data.Glucose,
            input_data.BloodPressure,
            input_data.SkinThickness,
            input_data.Insulin,
            input_data.BMI,
            input_data.DiabetesPedigreeFunction,
            input_data.Age
        ]])
        
        # Scale features
        features_scaled = SCALERS['diabetes'].transform(features)
        
        # Make prediction
        prediction = int(MODELS['diabetes'].predict(features_scaled)[0])
        probability = float(MODELS['diabetes'].predict_proba(features_scaled)[0][1])
        
        # Get recommendations
        feature_dict = input_data.dict()
        recommendations = get_recommendations('diabetes', prediction, probability, feature_dict)
        
        return PredictionResponse(
            diagnosis="Diabetes" if prediction == 1 else "No Diabetes",
            prediction=prediction,
            probability=round(probability, 4),
            confidence=get_confidence(probability),
            risk_level=get_risk_level(probability),
            recommendations=recommendations,
            model_used=METADATA['diabetes']['model_name'],
            feature_values=feature_dict
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/predict/heart-disease", response_model=PredictionResponse)
async def predict_heart_disease(input_data: HeartDiseaseInput):
    """
    Predict heart disease risk based on patient data
    """
    try:
        # Convert input to array
        features = np.array([[
            input_data.Age,
            input_data.Sex,
            input_data.ChestPainType,
            input_data.RestingBP,
            input_data.Cholesterol,
            input_data.FastingBS,
            input_data.RestingECG,
            input_data.MaxHR,
            input_data.ExerciseAngina,
            input_data.Oldpeak,
            input_data.ST_Slope
        ]])
        
        # Scale features
        features_scaled = SCALERS['heart_disease'].transform(features)
        
        # Make prediction
        prediction = int(MODELS['heart_disease'].predict(features_scaled)[0])
        probability = float(MODELS['heart_disease'].predict_proba(features_scaled)[0][1])
        
        # Get recommendations
        feature_dict = input_data.dict()
        recommendations = get_recommendations('heart_disease', prediction, probability, feature_dict)
        
        return PredictionResponse(
            diagnosis="Heart Disease Risk" if prediction == 1 else "No Heart Disease",
            prediction=prediction,
            probability=round(probability, 4),
            confidence=get_confidence(probability),
            risk_level=get_risk_level(probability),
            recommendations=recommendations,
            model_used=METADATA['heart_disease']['model_name'],
            feature_values=feature_dict
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/model-info/{model_type}", response_model=ModelInfoResponse)
async def get_model_info(model_type: str):
    """
    Get information about a specific model
    """
    if model_type not in METADATA:
        raise HTTPException(status_code=404, detail=f"Model '{model_type}' not found")
    
    metadata = METADATA[model_type]
    return ModelInfoResponse(
        model_name=metadata['model_name'],
        dataset=metadata['dataset'],
        features=metadata['features'],
        metrics=metadata['metrics'],
        training_date=metadata['training_date']
    )

@app.get("/models")
async def list_models():
    """
    List all available models with their metrics
    """
    models_info = {}
    for model_type, metadata in METADATA.items():
        models_info[model_type] = {
            "model_name": metadata['model_name'],
            "accuracy": metadata['metrics']['Accuracy'],
            "features_count": len(metadata['features'])
        }
    return models_info

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*70)
    print("🏥 Starting Healthcare Decision Support System API")
    print("="*70)
    print("\n📍 API will be available at: http://localhost:8000")
    print("📚 Interactive docs at: http://localhost:8000/docs")
    print("📖 Alternative docs at: http://localhost:8000/redoc")
    print("\n" + "="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
