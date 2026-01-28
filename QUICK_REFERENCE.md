# Quick Reference Guide
## Healthcare Diagnosis DSS - Command Cheat Sheet

---

## 🚀 Common Commands

### Setup
```bash
# Backend dependencies
cd backend && pip install -r requirements.txt

# Frontend dependencies
cd frontend && npm install
```

### Data Extraction
```bash
# Extract from PDF
python ml_models/data_extraction/extract_pdf.py <pdf_path> <output_dir> <method>

# Example
python ml_models/data_extraction/extract_pdf.py data/raw/medical_data.pdf data/processed pdfplumber
```

### Model Training
```bash
# Train with CSV
python ml_models/training/main_training_pipeline.py --csv data/processed/dataset.csv --target diagnosis

# Train with PDF
python ml_models/training/main_training_pipeline.py --pdf data/raw/medical_data.pdf --target diagnosis
```

### Run Application
```bash
# Terminal 1: Backend
cd backend && python app.py

# Terminal 2: Frontend
cd frontend && npm start
```

---

## 📁 Important File Locations

| Component | Location |
|-----------|----------|
| Backend API | `backend/app.py` |
| Frontend App | `frontend/src/App.js` |
| Training Pipeline | `ml_models/training/main_training_pipeline.py` |
| Models | `ml_models/models/` |
| Documentation | `docs/` |
| Datasets | `data/processed/` |

---

## 🔧 Configuration

### Backend Port
Edit: `backend/app.py`
```python
port = int(os.environ.get('PORT', 5000))
```

### Frontend API URL
Create: `frontend/.env`
```env
REACT_APP_API_URL=http://localhost:5000
```

---

## 📊 Model Files

After training, you'll have:
- `ml_models/models/best_model.pkl` - Best trained model
- `ml_models/models/preprocessor.pkl` - Preprocessor object
- `ml_models/models/model_evaluation_results.json` - Evaluation metrics
- Individual model files (logistic_regression_model.pkl, etc.)

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r backend/requirements.txt` |
| Port in use | Change port or kill process |
| Model not found | Train models first |
| CORS error | Check CORS in `backend/app.py` |
| npm install fails | `npm install --legacy-peer-deps` |

---

## 📝 Dataset Format

Your CSV should have:
- Patient features (columns)
- Target column (e.g., 'diagnosis' with 0/1 or Positive/Negative)
- No missing values in target column

---

## 🎯 Workflow

1. **Prepare Data** → Place CSV/PDF in `data/`
2. **Extract** → Run extraction (if PDF)
3. **Train** → Run training pipeline
4. **Start Backend** → `python backend/app.py`
5. **Start Frontend** → `npm start` in frontend/
6. **Test** → Open `http://localhost:3000`

---

## 📚 Documentation Quick Links

- **Setup**: `SETUP_INSTRUCTIONS.md`
- **Deployment**: `deployment/DEPLOYMENT_GUIDE.md`
- **SRS**: `docs/SRS/Software_Requirements_Specification.md`
- **Architecture**: `docs/Architecture/System_Architecture.md`
- **Report**: `docs/Reports/Project_Report.md`
- **PPT**: `docs/Reports/PPT_Outline.md`
- **Viva**: `docs/Reports/Viva_Questions_and_Answers.md`

---

**Keep this file handy for quick reference!**
