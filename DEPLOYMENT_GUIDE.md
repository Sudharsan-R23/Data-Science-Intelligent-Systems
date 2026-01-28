# Deployment and Setup Guide

Follow these steps to deploy and run the project locally.

## 1. System Requirements
- OS: Windows 10/11, Linux, or macOS.
- Python: 3.8 or higher.
- Node.js: 16.x or higher.

## 2. Backend Setup (FastAPI)
1. **Navigate to the project root**:
   ```bash
   cd d:\Data-Science-Intelligent-Systems
   ```
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   ```
3. **Install Python dependencies**:
   ```bash
   pip install fastapi uvicorn pandas scikit-learn xgboost pydantic python-multipart
   ```
4. **Run the backend server**:
   ```bash
   python backend/main.py
   ```
   *Server will run at http://localhost:8000*

## 3. Frontend Setup (React + Tailwind)
1. **Open a new terminal and navigate to the frontend folder**:
   ```bash
   cd d:\Data-Science-Intelligent-Systems/frontend
   ```
2. **Install Node dependencies**:
   ```bash
   npm install
   ```
3. **Run the development server**:
   ```bash
   npm run dev
   ```
   *Application will be accessible at http://localhost:5173*

## 4. Verification Check
- Visit `http://localhost:8000/docs` to see the interactive API documentation.
- Visit `http://localhost:5173` to use the Healthcare Diagnosis Dashboard.

## 6. Online Deployment (Cloud)
To host this application online so anyone can access it via a URL, follow these recommendations:

### A. Backend (Python API) - Use **Render** or **Railway**
1. Push your code to a **GitHub repository**.
2. Create a "Web Service" on [Render.com](https://render.com).
3. **Build Command**: `pip install -r backend/requirements.txt` (Move requirements to root if needed).
4. **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.

### B. Frontend (UI) - Use **Vercel** or **Netlify**
1. Connect your GitHub repo to [Vercel](https://vercel.com).
2. Set the **Root Directory** to `frontend`.
3. Add an Environment Variable `VITE_API_URL` pointing to your Render backend URL.
4. Vercel will build and give you a public `.vercel.app` link.

> [!TIP]
> For a free academic project, **Render** and **Vercel** are the most popular choices as they offer free tiers for students.
