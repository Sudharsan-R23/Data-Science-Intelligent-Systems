# System Architecture Document
## Decision Support System for Healthcare Diagnosis

### 1. Architecture Overview

The system follows a **three-tier architecture**:
1. **Presentation Layer**: React frontend
2. **Application Layer**: Flask/FastAPI backend
3. **Data/Model Layer**: ML models and preprocessing objects

### 2. System Components

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         React Frontend (Tailwind CSS)                │  │
│  │  - Diagnosis Form Component                          │  │
│  │  - Results Display Component                         │  │
│  │  - Feature Input Components                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/REST API
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Flask/FastAPI Backend                        │  │
│  │  - /api/predict endpoint                            │  │
│  │  - /api/health endpoint                             │  │
│  │  - /api/features endpoint                           │  │
│  │  - Request validation                               │  │
│  │  - Error handling                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Model Loading
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA/MODEL LAYER                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         ML Models & Preprocessors                   │  │
│  │  - Trained ML models (.pkl files)                  │  │
│  │  - Preprocessor objects                             │  │
│  │  - Feature importance data                          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 3. ML Training Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA EXTRACTION                           │
│  PDF Files → PDFExtractor → CSV Files                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA PREPROCESSING                        │
│  CSV Files → DataPreprocessor → Cleaned Data                │
│  - Missing value handling                                   │
│  - Categorical encoding                                     │
│  - Feature normalization                                    │
│  - Feature selection                                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODEL TRAINING                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Logistic     │  │ Random       │  │ SVM          │     │
│  │ Regression   │  │ Forest       │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐                                          │
│  │ XGBoost      │                                          │
│  └──────────────┘                                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODEL EVALUATION                          │
│  - Accuracy, Precision, Recall, F1-score                   │
│  - Cross-validation                                         │
│  - Best model selection                                     │
│  - Model saving                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    EXPLAINABLE AI                            │
│  - Feature importance calculation                           │
│  - SHAP values                                              │
│  - Visualization generation                                 │
└─────────────────────────────────────────────────────────────┘
```

### 4. Data Flow

#### 4.1 Training Phase
1. PDF datasets → Extraction → CSV files
2. CSV files → Preprocessing → Cleaned data
3. Cleaned data → Train/Test split
4. Training data → Model training → Trained models
5. Test data → Model evaluation → Metrics
6. Best model → Save to disk

#### 4.2 Prediction Phase
1. User input (Frontend) → HTTP POST request
2. Backend receives request → Validate input
3. Load preprocessor → Transform input data
4. Load model → Make prediction
5. Calculate probabilities → Generate recommendation
6. Return JSON response → Frontend displays results

### 5. Technology Stack

#### 5.1 Frontend
- **Framework**: React 18+
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Routing**: React Router

#### 5.2 Backend
- **Framework**: Flask/FastAPI
- **CORS**: flask-cors
- **Model Loading**: joblib
- **Data Processing**: pandas, numpy

#### 5.3 Machine Learning
- **Libraries**: scikit-learn, XGBoost
- **Preprocessing**: scikit-learn transformers
- **Explainability**: SHAP (optional)
- **Model Persistence**: joblib

#### 5.4 Data Extraction
- **PDF Processing**: pdfplumber, camelot-py

### 6. Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT BROWSER                           │
│  React Application (Static Files)                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTPS
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    WEB SERVER                               │
│  Nginx / Apache (Static File Serving)                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ Proxy
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION SERVER                       │
│  Flask/FastAPI (Gunicorn/uWSGI)                             │
│  Port: 5000                                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ File System
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    MODEL STORAGE                            │
│  File System: /ml_models/models/                            │
│  - best_model.pkl                                           │
│  - preprocessor.pkl                                         │
└─────────────────────────────────────────────────────────────┘
```

### 7. Security Architecture

- **Input Validation**: All inputs validated on backend
- **CORS**: Configured for specific origins
- **Error Handling**: No sensitive information in error messages
- **Data Privacy**: No patient data stored permanently
- **HTTPS**: Recommended for production deployment

### 8. Scalability Considerations

- **Horizontal Scaling**: Multiple backend instances behind load balancer
- **Model Caching**: Models loaded once at startup
- **Async Processing**: Consider async endpoints for heavy computations
- **Database**: Can add database for storing predictions/history

### 9. Monitoring and Logging

- **Application Logs**: Python logging module
- **Error Tracking**: Exception handling and logging
- **Performance Metrics**: Response time tracking
- **Health Checks**: `/api/health` endpoint

---

**Document Version**: 1.0  
**Date**: January 2026
