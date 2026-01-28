# Software Requirements Specification (SRS)
## Decision Support System for Healthcare Diagnosis Using Machine Learning Models

### 1. Introduction

#### 1.1 Purpose
This document specifies the requirements for a Decision Support System (DSS) that assists healthcare professionals in medical diagnosis using machine learning models. The system processes patient data and provides diagnostic predictions with explainable AI features.

#### 1.2 Scope
The system includes:
- PDF data extraction and preprocessing
- Multiple ML model training and evaluation
- REST API backend
- Web-based frontend interface
- Explainable AI features (feature importance, SHAP values)

#### 1.3 Definitions and Acronyms
- **DSS**: Decision Support System
- **ML**: Machine Learning
- **API**: Application Programming Interface
- **SHAP**: SHapley Additive exPlanations
- **SVM**: Support Vector Machine
- **XGBoost**: Extreme Gradient Boosting

#### 1.4 References
- IEEE 830-1998 Standard for Software Requirements Specifications
- Healthcare Data Standards (HL7, FHIR)
- Machine Learning Best Practices

### 2. Overall Description

#### 2.1 Product Perspective
The system is a standalone web application consisting of:
- Machine Learning training pipeline
- Flask/FastAPI backend server
- React frontend application
- Database for storing models and preprocessing objects

#### 2.2 Product Functions
1. **Data Extraction**: Extract medical data from PDF datasets
2. **Data Preprocessing**: Clean, normalize, and encode data
3. **Model Training**: Train multiple ML models (LR, RF, SVM, XGBoost)
4. **Model Evaluation**: Compare models and select best performer
5. **Prediction API**: Provide REST endpoints for diagnosis predictions
6. **Web Interface**: User-friendly form for inputting patient data
7. **Results Display**: Show predictions with probabilities and recommendations
8. **Explainable AI**: Display feature importance and SHAP values

#### 2.3 User Classes and Characteristics
- **Primary Users**: Healthcare professionals (doctors, nurses)
- **Secondary Users**: Medical researchers, data scientists
- **System Administrators**: IT staff managing the system

#### 2.4 Operating Environment
- **Backend**: Python 3.8+, Flask/FastAPI
- **Frontend**: React 18+, Node.js 16+
- **ML Libraries**: scikit-learn, XGBoost, pandas, numpy
- **Deployment**: Cloud or on-premise servers

#### 2.5 Design and Implementation Constraints
- Must comply with healthcare data privacy regulations
- System is a decision support tool, not a replacement for medical professionals
- All predictions must include disclaimers
- Code must be modular and maintainable

### 3. System Features

#### 3.1 Data Extraction Module
**Description**: Extract tabular data from PDF medical datasets

**Inputs**: PDF file path
**Outputs**: CSV files with extracted tables

**Functional Requirements**:
- FR-1.1: System shall extract tables from PDF files
- FR-1.2: System shall support multiple extraction methods (pdfplumber, camelot)
- FR-1.3: System shall save extracted data as CSV files

#### 3.2 Data Preprocessing Module
**Description**: Clean and prepare data for ML training

**Inputs**: Raw CSV data
**Outputs**: Preprocessed CSV data

**Functional Requirements**:
- FR-2.1: System shall handle missing values
- FR-2.2: System shall encode categorical variables
- FR-2.3: System shall normalize numerical features
- FR-2.4: System shall perform feature selection (optional)

#### 3.3 Model Training Module
**Description**: Train and compare multiple ML models

**Inputs**: Preprocessed data, target column
**Outputs**: Trained models, evaluation metrics

**Functional Requirements**:
- FR-3.1: System shall train Logistic Regression model
- FR-3.2: System shall train Random Forest model
- FR-3.3: System shall train SVM model
- FR-3.4: System shall train XGBoost model
- FR-3.5: System shall evaluate models using accuracy, precision, recall, F1-score
- FR-3.6: System shall select best model based on evaluation metrics
- FR-3.7: System shall save trained models

#### 3.4 Prediction API
**Description**: REST API for making predictions

**Inputs**: Patient feature data (JSON)
**Outputs**: Prediction results (JSON)

**Functional Requirements**:
- FR-4.1: System shall provide `/api/predict` endpoint
- FR-4.2: System shall return prediction, probability, and recommendation
- FR-4.3: System shall include feature importance in response
- FR-4.4: System shall validate input data
- FR-4.5: System shall handle errors gracefully

#### 3.5 Web Interface
**Description**: User-friendly frontend for inputting patient data

**Inputs**: Patient information form
**Outputs**: Diagnosis results page

**Functional Requirements**:
- FR-5.1: System shall provide form for patient data input
- FR-5.2: System shall validate form inputs
- FR-5.3: System shall display prediction results
- FR-5.4: System shall show probability breakdown
- FR-5.5: System shall display medical recommendations
- FR-5.6: System shall show feature importance visualization

#### 3.6 Explainable AI Module
**Description**: Provide model interpretability features

**Functional Requirements**:
- FR-6.1: System shall calculate feature importance
- FR-6.2: System shall generate SHAP values (if available)
- FR-6.3: System shall visualize feature contributions
- FR-6.4: System shall generate confusion matrices
- FR-6.5: System shall generate ROC curves

### 4. Non-Functional Requirements

#### 4.1 Performance Requirements
- API response time: < 2 seconds
- Model training time: Acceptable for dataset size
- Frontend load time: < 3 seconds

#### 4.2 Security Requirements
- Input validation and sanitization
- CORS configuration for API
- Secure model storage

#### 4.3 Reliability Requirements
- System uptime: 99% availability
- Error handling and logging
- Data backup mechanisms

#### 4.4 Usability Requirements
- Intuitive user interface
- Clear error messages
- Responsive design (mobile-friendly)

#### 4.5 Maintainability Requirements
- Modular code structure
- Comprehensive documentation
- Version control

### 5. System Models

#### 5.1 Use Case Diagram
(See UML diagrams section)

#### 5.2 Sequence Diagram
(See UML diagrams section)

#### 5.3 Class Diagram
(See UML diagrams section)

### 6. Appendices

#### 6.1 Glossary
- **Feature**: Input variable used for prediction
- **Target**: Output variable to predict
- **Preprocessing**: Data cleaning and transformation
- **Model**: Trained ML algorithm

#### 6.2 Assumptions
- Users have basic medical knowledge
- Input data follows expected format
- System is used in controlled medical environment

---

**Document Version**: 1.0  
**Date**: January 2026  
**Author**: Project Team
