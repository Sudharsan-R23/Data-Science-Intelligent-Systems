# Software Requirements Specification (SRS)
## Decision Support System for Healthcare Diagnosis

### 1. Introduction
#### 1.1 Purpose
The purpose of this document is to define the software requirements for the "Decision Support System for Healthcare Diagnosis Using Machine Learning Models". This system aims to assist medical professionals in early detection and diagnosis of diseases like Diabetes and Heart Disease using advanced machine learning algorithms.

#### 1.2 Scope
The system will accept patient medical records as input, process the data using trained ML models, and provide a diagnostic prediction with a probability score and medical recommendations. It serves as a decision support tool, not a replacement for medical professionals.

#### 1.3 Definitions, Acronyms, and Abbreviations
- **DSS**: Decision Support System
- **ML**: Machine Learning
- **API**: Application Programming Interface
- **UI**: User Interface
- **SRS**: Software Requirements Specification
- **SVM**: Support Vector Machine
- **XGBoost**: Extreme Gradient Boosting

### 2. Overall Description
#### 2.1 Product Perspective
This is a web-based application consisting of a React-based frontend and a Python FastAPI backend. The system integrates machine learning models trained on standard healthcare datasets.

#### 2.2 Product Functions
- **Data Input**: User-friendly form for entering patient vitals and medical history.
- **Prediction**: Real-time disease risk assessment using ML models.
- **Multimodal Support**: Support for multiple diseases (Diabetes, Heart Disease).
- **Explainability**: Display of prediction confidence, key feature importance, and actionable recommendations.
- **Reporting**: Visual representation of risk analysis.

#### 2.3 User Characteristics
- **Primary Users**: Doctors, Nurses, and Healthcare Providers.
- **Secondary Users**: Medical Researchers and Administrators.
- **Knowledge Level**: Basic computer literacy and medical domain knowledge required.

### 3. Specific Requirements
#### 3.1 Functional Requirements
**FR1: Patient Data Entry**
- The system shall allow users to select the disease type for diagnosis.
- The system shall validate all input fields (e.g., age must be positive, glucose levels within physiological ranges).

**FR2: Diagnosis & Prediction**
- The system shall use the Random Forest/XGBoost model to predict disease presence.
- The system shall return a binary classification (Positive/Negative) along with a probability score (0-100%).

**FR3: Recommendations**
- The system shall provide at least 3 context-aware medical recommendations based on the prediction and specific risk factors (e.g., "High BMI detected - Weight management recommended").

**FR4: API Integration**
- The frontend shall communicate with the backend via RESTful API endpoints.
- The system shall handle API errors gracefully and display user-friendly messages.

#### 3.2 Non-Functional Requirements
**NFR1: Performance**
- Predictions shall be generated in under 2 seconds.
- Experimental accuracy of models shall be above 80%.

**NFR2: Security**
- Input data shall be sanitized to prevent injection attacks.
- HTTPS shall be used for all data transmission (in production).

**NFR3: Usability**
- The UI shall be responsive and accessible on desktop and tablet devices.
- Medical terminology shall be accurate and standard.

**NFR4: Reliability**
- The system shall be available 99.9% of the time during business hours.

### 4. System Interface
#### 4.1 User Interface
- **Dashboard**: Minimalist design with clear navigation between disease modules.
- **Input Forms**: Labeled fields with placeholder text and validation feedback.
- **Result Screen**: Color-coded indicators (Green for Low Risk, Red for High Risk) and visual gauges.

#### 4.2 Hardware Interfaces
- The system requires a standard server or cloud instance for the backend.
- Users can access the system via any standard web browser on PC or Tablet.

#### 4.3 Software Interfaces
- **OS**: Windows/Linux/MacOS
- **Database**: CSV/Pandas (Prototype), SQL Database (Future Scope)
- **Frameworks**: React (Frontend), FastAPI (Backend), Scikit-Learn (ML)
