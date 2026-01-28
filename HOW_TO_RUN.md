# How to Run the Healthcare Decision Support System

## Prerequisites
- Python 3.8+
- Node.js & npm

## 1. Start the Backend API
The backend serves the Machine Learning models.

```bash
# Open a terminal in the project root
cd d:\Data-Science-Intelligent-Systems

# Activate virtual environment (if using one)
# .venv\Scripts\activate

# Run the FastAPI server
python backend/main.py
```
*The API will start at http://localhost:8000*
*(Note: Swagger UI docs available at http://localhost:8000/docs)*

## 2. Start the Frontend Application
The frontend provides the user interface for doctors.

```bash
# Open a NEW terminal
cd d:\Data-Science-Intelligent-Systems/frontend

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```
*The application will open at http://localhost:5173*

## 3. Usage
1. Open http://localhost:5173 in your browser
2. Select the disease type (Diabetes or Heart Disease)
3. Enter patient details
4. Click "Predict" to see results and recommendations
