# System Flowcharts

## 1. Overall System Flow

```
START
  │
  ├─► [Upload PDF Dataset]
  │         │
  │         ▼
  │   [Extract Tables to CSV]
  │         │
  │         ▼
  │   [Preprocess Data]
  │         │
  │         ▼
  │   [Train ML Models]
  │         │
  │         ▼
  │   [Evaluate & Select Best Model]
  │         │
  │         ▼
  │   [Save Model & Preprocessor]
  │         │
  │         ▼
  ├─► [Start Backend API]
  │         │
  │         ▼
  ├─► [Start Frontend]
  │         │
  │         ▼
  │   [User Inputs Patient Data]
  │         │
  │         ▼
  │   [Backend Preprocesses Input]
  │         │
  │         ▼
  │   [Model Makes Prediction]
  │         │
  │         ▼
  │   [Calculate Probabilities]
  │         │
  │         ▼
  │   [Generate Recommendation]
  │         │
  │         ▼
  │   [Display Results to User]
  │         │
  │         ▼
END
```

## 2. ML Training Pipeline Flow

```
START Training Pipeline
  │
  ▼
[Load CSV Data]
  │
  ▼
[Identify Column Types]
  │
  ├─► Categorical ──► [Encode Categorical]
  │                         │
  └─► Numerical ────► [Handle Missing Values]
                            │
                            ▼
                    [Normalize Features]
                            │
                            ▼
                    [Feature Selection?]
                            │
                            ├─► Yes ──► [Select Features]
                            │              │
                            └─► No ───────┘
                                    │
                                    ▼
                            [Split Train/Test]
                                    │
                                    ▼
                            [Train Models]
                                    │
                                    ├─► [Logistic Regression]
                                    ├─► [Random Forest]
                                    ├─► [SVM]
                                    └─► [XGBoost]
                                            │
                                            ▼
                                    [Evaluate All Models]
                                            │
                                            ▼
                                    [Select Best Model]
                                            │
                                            ▼
                                    [Save Models]
                                            │
                                            ▼
                                    [Generate Reports]
                                            │
                                            ▼
END Training Pipeline
```

## 3. Prediction Flow

```
START Prediction Request
  │
  ▼
[User Fills Form]
  │
  ▼
[Validate Input]
  │
  ├─► Invalid ──► [Show Error] ──► END
  │
  └─► Valid
        │
        ▼
[Send POST to /api/predict]
        │
        ▼
[Backend Receives Request]
        │
        ▼
[Load Preprocessor]
        │
        ▼
[Transform Input Data]
        │
        ▼
[Load Trained Model]
        │
        ▼
[Make Prediction]
        │
        ▼
[Calculate Probabilities]
        │
        ▼
[Get Feature Importance]
        │
        ▼
[Generate Recommendation]
        │
        ▼
[Return JSON Response]
        │
        ▼
[Frontend Displays Results]
        │
        ▼
END Prediction Request
```

## 4. Data Preprocessing Flow

```
START Preprocessing
  │
  ▼
[Load Raw Data]
  │
  ▼
[Check for Missing Values]
  │
  ├─► Found ──► [Apply Imputation Strategy]
  │                 │
  └─► None ────────┘
            │
            ▼
[Identify Categorical Columns]
            │
            ▼
[Encode Categorical Variables]
            │
            ├─► Label Encoding
            └─► One-Hot Encoding
                    │
                    ▼
[Identify Numerical Columns]
            │
            ▼
[Normalize Numerical Features]
            │
            ├─► Standard Scaling (Z-score)
            └─► Min-Max Scaling (0-1)
                    │
                    ▼
[Feature Selection?]
            │
            ├─► Yes ──► [Select K Best Features]
            │              │
            └─► No ───────┘
                    │
                    ▼
[Save Preprocessed Data]
            │
            ▼
[Save Preprocessor Object]
            │
            ▼
END Preprocessing
```

## 5. Model Evaluation Flow

```
START Model Evaluation
  │
  ▼
[For Each Model]
  │
  ├─► [Make Predictions on Test Set]
  │         │
  │         ▼
  │   [Calculate Metrics]
  │         │
  │         ├─► Accuracy
  │         ├─► Precision
  │         ├─► Recall
  │         └─► F1-Score
  │                 │
  │                 ▼
  │         [Cross-Validation]
  │                 │
  │                 ▼
  │         [Generate Visualizations]
  │                 │
  │                 ├─► Confusion Matrix
  │                 ├─► ROC Curve
  │                 └─► Feature Importance
  │                         │
  │                         ▼
  │                 [Calculate SHAP Values]
  │                         │
  │                         ▼
  │                 [Save Evaluation Results]
  │
  ▼
[Compare All Models]
  │
  ▼
[Select Best Model]
  │
  ├─► Based on F1-Score (default)
  ├─► Based on Accuracy
  ├─► Based on Precision
  └─► Based on Recall
          │
          ▼
[Save Best Model]
          │
          ▼
END Model Evaluation
```

---

**Document Version**: 1.0  
**Date**: January 2026
