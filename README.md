# Decision Support System for Healthcare Diagnosis Using Machine Learning Models

## Project Overview

This is a comprehensive end-to-end intelligent web application that assists healthcare professionals in diagnosis decision-making using machine learning models. The system processes medical datasets, trains multiple ML models, and provides diagnosis predictions with explainable AI features.

## Project Structure

```
Data-Science-Intelligent-Systems/
├── ml_models/              # Machine Learning training and evaluation
│   ├── data_extraction/    # PDF to CSV conversion
│   ├── preprocessing/      # Data cleaning and preprocessing
│   ├── training/           # Model training scripts
│   ├── evaluation/         # Model evaluation and comparison
│   └── models/             # Saved trained models
├── backend/                # Flask/FastAPI REST API
│   ├── app.py             # Main application file
│   ├── models/            # Model loading utilities
│   └── requirements.txt   # Python dependencies
├── frontend/              # React + Tailwind CSS UI
│   ├── src/
│   ├── public/
│   └── package.json
├── docs/                  # Documentation
│   ├── SRS/              # Software Requirements Specification
│   ├── Architecture/     # System architecture diagrams
│   ├── UML/             # UML diagrams
│   ├── Flowcharts/      # Process flowcharts
│   └── Reports/         # Project reports
├── data/                 # Datasets (CSV files)
├── notebooks/           # Jupyter notebooks for analysis
└── deployment/          # Deployment scripts and configs
```

## Features

- **PDF Data Extraction**: Extract medical data from PDF datasets
- **Data Preprocessing**: Automated cleaning, normalization, and encoding
- **Multiple ML Models**: Logistic Regression, Random Forest, SVM, XGBoost
- **Model Evaluation**: Comprehensive metrics (Accuracy, Precision, Recall, F1-score)
- **REST API**: Flask/FastAPI backend for predictions
- **Modern UI**: React frontend with Tailwind CSS
- **Explainable AI**: Feature importance and SHAP values
- **Academic Documentation**: Complete SRS, Architecture, UML diagrams

## Technology Stack

- **ML/AI**: scikit-learn, XGBoost, pandas, numpy, SHAP
- **Backend**: Flask/FastAPI
- **Frontend**: React, Tailwind CSS
- **Data Processing**: pandas, pdfplumber/camelot
- **Documentation**: Markdown, PlantUML, Draw.io

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. Clone the repository
2. Install Python dependencies: `pip install -r backend/requirements.txt`
3. Install frontend dependencies: `cd frontend && npm install`

### Usage

1. Upload PDF datasets to `data/raw/`
2. Run data extraction: `python ml_models/data_extraction/extract_pdf.py`
3. Train models: `python ml_models/training/train_models.py`
4. Start backend: `python backend/app.py`
5. Start frontend: `cd frontend && npm start`

## Important Notes

- This is a **Decision Support System**, not a replacement for medical professionals
- All predictions should be reviewed by qualified healthcare providers
- The system provides probabilities and recommendations, not definitive diagnoses

## License

Academic Project - For Educational Purposes Only
