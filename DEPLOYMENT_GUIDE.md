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

## 6. Online Deployment (Production)

To make your system accessible worldwide, follow these steps to host both the Backend and Frontend for free.

### Phase 1: Preparation
1. **Push your code to GitHub**: Create a repository and push this entire project to it.

### Phase 2: Host the Backend (API) on Render
[Render](https://render.com) is excellent for Python applications.
1. Sign up/Log in to Render and click **New > Web Service**.
2. Connect your GitHub repository.
3. Configure the following settings:
   - **Name**: `healthcare-api` (or any name)
   - **Root Directory**: `(leave empty)`
   - **Environment**: `Python`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port 10000`
4. Click **Deploy**. Once finished, copy your service URL (e.g., `https://healthcare-api.onrender.com`).

### Phase 3: Host the Frontend (UI) on Vercel
[Vercel](https://vercel.com) is the preferred choice for React/Vite.
1. Sign up/Log in to Vercel and click **Add New > Project**.
2. Connect the same GitHub repository.
3. In the project settings:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Environment Variables**: Add a new variable:
     - **Key**: `VITE_API_URL`
     - **Value**: Your Render Backend URL (without a trailing slash)
4. Click **Deploy**. Vercel will provide a public link (e.g., `https://frontend-name.vercel.app`).

### Phase 4: Verification
1. Open your Vercel URL.
2. The Dashboard should load, and the "System Status" at the bottom should show **ONLINE** (if linked correctly to Render).
3. Try running an analysis to confirm data flows correctly through the web.

> [!IMPORTANT]
> Render's free tier "spins down" after inactivity. The first request after a break might take 30-60 seconds to respond as the server wakes up.
