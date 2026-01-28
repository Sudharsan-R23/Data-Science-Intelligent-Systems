# Deployment Guide
## Decision Support System for Healthcare Diagnosis

---

## Prerequisites

### System Requirements
- **Operating System**: Windows 10+, Linux, or macOS
- **Python**: 3.8 or higher
- **Node.js**: 16.x or higher
- **npm**: 8.x or higher (comes with Node.js)
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space

### Software Installation

#### 1. Install Python
```bash
# Download from python.org or use package manager
python --version  # Should show 3.8+
```

#### 2. Install Node.js
```bash
# Download from nodejs.org
node --version  # Should show 16.x or higher
npm --version   # Should show 8.x or higher
```

---

## Step 1: Clone/Download Project

```bash
# If using git
git clone <repository-url>
cd Data-Science-Intelligent-Systems

# Or extract downloaded ZIP file
```

---

## Step 2: Backend Setup

### 2.1 Create Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.2 Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**If you encounter issues, install individually:**
```bash
pip install flask==3.0.0
pip install flask-cors==4.0.0
pip install pandas==2.1.4
pip install numpy==1.26.2
pip install scikit-learn==1.3.2
pip install joblib==1.3.2
pip install xgboost==2.0.3
pip install pdfplumber
pip install camelot-py[cv]
```

**For SHAP (optional):**
```bash
pip install shap
```

---

## Step 3: Frontend Setup

### 3.1 Install Node Dependencies

```bash
cd frontend
npm install
```

**If npm install fails, try:**
```bash
npm install --legacy-peer-deps
```

### 3.2 Install Tailwind CSS

Tailwind should be installed via npm. If not:
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

---

## Step 4: Prepare Data and Train Models

### 4.1 Place Your Dataset

**Option A: If you have a CSV file:**
```bash
# Place your CSV file in data/processed/
# Example: data/processed/diabetes_dataset.csv
```

**Option B: If you have a PDF file:**
```bash
# Place PDF in data/raw/
# Example: data/raw/medical_data.pdf
```

### 4.2 Extract Data from PDF (if needed)

```bash
python ml_models/data_extraction/extract_pdf.py data/raw/medical_data.pdf data/processed pdfplumber
```

### 4.3 Train Models

```bash
# If using CSV directly
python ml_models/training/main_training_pipeline.py --csv data/processed/dataset.csv --target diagnosis

# If extracting from PDF first
python ml_models/training/main_training_pipeline.py --pdf data/raw/medical_data.pdf --target diagnosis
```

**Expected Output:**
- Trained models saved in `ml_models/models/`
- Best model: `ml_models/models/best_model.pkl`
- Preprocessor: `ml_models/models/preprocessor.pkl`
- Evaluation results: `ml_models/models/model_evaluation_results.json`

---

## Step 5: Configure Backend

### 5.1 Update Model Paths (if needed)

Edit `backend/app.py` and verify paths:
```python
MODEL_PATH = Path("ml_models/models/best_model.pkl")
PREPROCESSOR_PATH = Path("ml_models/models/preprocessor.pkl")
```

### 5.2 Create .env file (Optional)

Create `backend/.env`:
```env
PORT=5000
FLASK_ENV=development
API_URL=http://localhost:5000
```

---

## Step 6: Run Backend Server

### 6.1 Start Flask Server

```bash
cd backend
python app.py
```

**Expected Output:**
```
 * Running on http://0.0.0.0:5000
```

**Test Backend:**
```bash
# Open browser or use curl
curl http://localhost:5000/api/health
```

---

## Step 7: Run Frontend

### 7.1 Start React Development Server

**In a new terminal:**
```bash
cd frontend
npm start
```

**Expected Output:**
```
Compiled successfully!
You can now view the app in the browser.
Local: http://localhost:3000
```

### 7.2 Configure API URL (if needed)

Create `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:5000
```

---

## Step 8: Access Application

1. **Open Browser**: Navigate to `http://localhost:3000`
2. **Fill Form**: Enter patient information
3. **Get Prediction**: Click "Get Diagnosis"
4. **View Results**: See prediction, probabilities, and recommendations

---

## Production Deployment

### Option 1: Deploy Backend (Flask)

#### Using Gunicorn (Linux/macOS):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Using Waitress (Windows):
```bash
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

### Option 2: Deploy Frontend

#### Build for Production:
```bash
cd frontend
npm run build
```

**Deploy `build/` folder to:**
- Netlify
- Vercel
- AWS S3 + CloudFront
- GitHub Pages
- Any static hosting service

### Option 3: Docker Deployment

#### Create Dockerfile for Backend:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "backend/app.py"]
```

#### Create Dockerfile for Frontend:
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/build /usr/share/nginx/html
```

#### Docker Compose:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
  frontend:
    build: ./frontend
    ports:
      - "80:80"
```

---

## Troubleshooting

### Issue: Module not found errors
**Solution:**
```bash
pip install <module-name>
# Or reinstall requirements
pip install -r backend/requirements.txt
```

### Issue: Port already in use
**Solution:**
```bash
# Change port in backend/app.py or frontend/.env
# Or kill process using port:
# Windows: netstat -ano | findstr :5000
# Linux: lsof -i :5000
```

### Issue: CORS errors
**Solution:**
- Verify CORS is enabled in `backend/app.py`
- Check API URL in frontend matches backend URL

### Issue: Model not found
**Solution:**
- Ensure models are trained first
- Check file paths in `backend/app.py`
- Verify `ml_models/models/` directory exists

### Issue: Frontend build fails
**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

---

## Environment Variables

### Backend (.env)
```env
PORT=5000
FLASK_ENV=production
DEBUG=False
```

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000
```

---

## Security Checklist for Production

- [ ] Use HTTPS (SSL/TLS certificates)
- [ ] Set `DEBUG=False` in production
- [ ] Configure CORS for specific origins
- [ ] Implement authentication (if needed)
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting
- [ ] Set up logging and monitoring
- [ ] Regular security updates

---

## Monitoring

### Health Check Endpoint
```bash
curl http://localhost:5000/api/health
```

### Logs
- Backend logs: Console output
- Frontend logs: Browser console
- Production: Use logging services (e.g., Loggly, Papertrail)

---

## Backup and Recovery

### Backup:
- Trained models: `ml_models/models/*.pkl`
- Preprocessor: `ml_models/models/preprocessor.pkl`
- Configuration files
- Source code

### Recovery:
- Restore models and preprocessor files
- Reinstall dependencies
- Restart services

---

## Support

For issues or questions:
1. Check this deployment guide
2. Review error logs
3. Check GitHub issues (if applicable)
4. Contact project team

---

**Last Updated**: January 2026
