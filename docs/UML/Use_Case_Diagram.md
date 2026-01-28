# Use Case Diagram

## Use Case: Healthcare Diagnosis Decision Support System

```
                    ┌─────────────────────────────┐
                    │   Healthcare Professional    │
                    └──────────────┬───────────────┘
                                   │
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│ Input Patient │         │ View Diagnosis│         │ View Feature  │
│    Data       │         │    Results    │         │  Importance   │
└───────────────┘         └───────────────┘         └───────────────┘
        │                          │                          │
        │                          │                          │
        └──────────────────────────┼──────────────────────────┘
                                   │
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
                    ▼                              ▼
        ┌──────────────────────┐      ┌──────────────────────┐
        │  Get Recommendations │      │  View Probabilities  │
        └──────────────────────┘      └──────────────────────┘


                    ┌─────────────────────────────┐
                    │      Data Scientist         │
                    └──────────────┬───────────────┘
                                   │
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│ Extract PDF   │         │ Preprocess    │         │ Train Models  │
│    Data       │         │    Data       │         │               │
└───────────────┘         └───────────────┘         └───────────────┘
        │                          │                          │
        │                          │                          │
        └──────────────────────────┼──────────────────────────┘
                                   │
                                   │
                    ┌──────────────┴───────────────┐
                    │                              │
                    ▼                              ▼
        ┌──────────────────────┐      ┌──────────────────────┐
        │  Evaluate Models    │      │  Generate Reports    │
        └──────────────────────┘      └──────────────────────┘
```

## Use Case Descriptions

### UC-1: Input Patient Data
- **Actor**: Healthcare Professional
- **Description**: User enters patient information through web form
- **Preconditions**: System is running, user has access
- **Main Flow**: 
  1. User opens diagnosis form
  2. User enters patient data
  3. User submits form
  4. System validates input
  5. System sends request to backend
- **Postconditions**: Prediction request sent to backend

### UC-2: View Diagnosis Results
- **Actor**: Healthcare Professional
- **Description**: User views prediction results with probabilities
- **Preconditions**: Prediction request completed
- **Main Flow**:
  1. System displays prediction (Positive/Negative)
  2. System shows probability percentages
  3. System displays recommendation
- **Postconditions**: Results displayed to user

### UC-3: View Feature Importance
- **Actor**: Healthcare Professional
- **Description**: User views which features contributed most to prediction
- **Preconditions**: Prediction completed
- **Main Flow**:
  1. System calculates feature importance
  2. System displays top contributing features
  3. User reviews feature contributions
- **Postconditions**: Feature importance displayed

### UC-4: Extract PDF Data
- **Actor**: Data Scientist
- **Description**: Extract tables from PDF medical datasets
- **Preconditions**: PDF file available
- **Main Flow**:
  1. System reads PDF file
  2. System extracts tables
  3. System saves as CSV files
- **Postconditions**: CSV files created

### UC-5: Train Models
- **Actor**: Data Scientist
- **Description**: Train multiple ML models on preprocessed data
- **Preconditions**: Preprocessed data available
- **Main Flow**:
  1. System splits data into train/test
  2. System trains each model
  3. System evaluates models
  4. System selects best model
  5. System saves models
- **Postconditions**: Trained models saved

---

**Document Version**: 1.0  
**Date**: January 2026
