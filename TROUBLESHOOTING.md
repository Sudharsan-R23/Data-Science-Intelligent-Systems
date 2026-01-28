# Troubleshooting Guide
## Common Issues and Solutions

---

## Issue: "An error occurred. Please try again." when submitting form

### Possible Causes and Solutions:

#### 1. Backend Not Running
**Symptoms**: Error message appears immediately, no server response

**Solution**:
```bash
# Check if backend is running
# Open a new terminal and run:
cd backend
python app.py

# You should see:
# * Running on http://0.0.0.0:5000
```

**Verify Backend is Running**:
- Open browser: http://localhost:5000/api/health
- Should return: `{"status": "healthy", "model_loaded": true/false, "preprocessor_loaded": true/false}`

---

#### 2. Model Files Not Found
**Symptoms**: Error says "Model not loaded" or "Model not found"

**Solution**:
```bash
# Check if model files exist
ls ml_models/models/

# Should see:
# - best_model.pkl
# - preprocessor.pkl
# - model_evaluation_results.json

# If files don't exist, train the model first:
python ml_models/training/main_training_pipeline.py --csv data/processed/your_dataset.csv --target diagnosis
```

---

#### 3. Feature Mismatch
**Symptoms**: Error about missing columns or feature names

**Solution**:
- The form fields must match the features your model was trained on
- Check what features your model expects:
  - Look at `ml_models/models/model_evaluation_results.json`
  - Or check the training dataset columns

**Update Form Fields**:
Edit `frontend/src/pages/DiagnosisForm.js` to match your dataset features.

---

#### 4. CORS Error
**Symptoms**: Browser console shows CORS error

**Solution**:
- Backend already has CORS enabled
- Make sure backend is running on port 5000
- Check API URL in frontend matches backend URL

---

#### 5. Port Already in Use
**Symptoms**: Backend won't start, port 5000 in use

**Solution**:

**Windows**:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Linux/macOS**:
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

**Or change port**:
Edit `backend/app.py`:
```python
port = int(os.environ.get('PORT', 5001))  # Change to 5001
```

And update frontend `.env`:
```env
REACT_APP_API_URL=http://localhost:5001
```

---

## Issue: "Cannot connect to server"

### Solution:
1. **Check Backend Status**:
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Check Firewall**: Make sure port 5000 is not blocked

3. **Check API URL**: Verify `REACT_APP_API_URL` in `frontend/.env`

---

## Issue: "Preprocessing failed"

### Solution:
1. **Check Feature Names**: Form fields must match training data columns
2. **Check Data Types**: Ensure numeric fields are numbers, categorical are strings
3. **Check Missing Values**: Some models don't handle missing values well

**Debug Steps**:
```python
# In backend/app.py, add logging:
logger.info(f"Received features: {features}")
logger.info(f"DataFrame columns: {df.columns.tolist()}")
```

---

## Issue: Form fields don't match model features

### Solution:

**Step 1**: Check what features your model expects
```python
# After training, check the model:
import joblib
model = joblib.load('ml_models/models/best_model.pkl')
preprocessor = joblib.load('ml_models/models/preprocessor.pkl')

# Check selected features
if 'selected_features' in preprocessor:
    print("Required features:", preprocessor['selected_features'])
```

**Step 2**: Update form in `frontend/src/pages/DiagnosisForm.js`
- Add/remove fields to match your dataset
- Update formData state
- Update form JSX

---

## Quick Diagnostic Steps

### 1. Check Backend Health
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "preprocessor_loaded": true
}
```

### 2. Check Model Files
```bash
# List model files
ls -la ml_models/models/

# Should see:
# best_model.pkl
# preprocessor.pkl
```

### 3. Check Browser Console
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab for API calls

### 4. Check Backend Logs
- Look at terminal where backend is running
- Check for error messages
- Look for preprocessing/prediction errors

---

## Step-by-Step Debugging

### Step 1: Verify Backend is Running
```bash
cd backend
python app.py
# Should see: * Running on http://0.0.0.0:5000
```

### Step 2: Test API Endpoint
```bash
# Test health endpoint
curl http://localhost:5000/api/health

# Test predict endpoint (example)
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"features": {"age": 45, "glucose": 150, "blood_pressure": 85, "bmi": 29.5, "insulin": 140, "gender": "Male"}}'
```

### Step 3: Check Frontend Connection
- Open browser DevTools (F12)
- Go to Network tab
- Submit form
- Check if request reaches backend
- Check response status and body

### Step 4: Verify Model Files
```bash
# Check if files exist
python -c "from pathlib import Path; print(Path('ml_models/models/best_model.pkl').exists())"
python -c "from pathlib import Path; print(Path('ml_models/models/preprocessor.pkl').exists())"
```

---

## Common Error Messages and Fixes

| Error Message | Cause | Solution |
|--------------|-------|----------|
| "Cannot connect to server" | Backend not running | Start backend: `python backend/app.py` |
| "Model not loaded" | Model file missing | Train model first |
| "Preprocessing failed" | Feature mismatch | Update form fields to match training data |
| "CORS error" | CORS not configured | Already configured, check backend is running |
| "Port 5000 in use" | Another process using port | Kill process or change port |
| "Feature not found" | Wrong feature names | Check training data columns |

---

## Still Having Issues?

1. **Check Logs**: Look at backend terminal output
2. **Check Browser Console**: Look for JavaScript errors
3. **Check Network Tab**: See if API calls are being made
4. **Verify Model Training**: Make sure models were trained successfully
5. **Check Feature Names**: Ensure form fields match model features

---

## Need More Help?

1. Check `SETUP_INSTRUCTIONS.md` for setup steps
2. Check `deployment/DEPLOYMENT_GUIDE.md` for detailed setup
3. Review backend logs for specific error messages
4. Check browser console for frontend errors

---

**Last Updated**: January 2026
