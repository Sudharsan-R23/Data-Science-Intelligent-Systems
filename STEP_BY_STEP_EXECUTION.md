# Step-by-Step Execution Guide
## Healthcare Diagnosis DSS - Complete Run Instructions

---

## Prerequisites Check

Before running, you need:
- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)

---

## Part 1: Fix Python Issues (If "Python was not found")

### Step 1.1: Install Python (Windows)

1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Download **Python 3.11** or **Python 3.12** (latest stable)
   - Run the installer

2. **During Installation - IMPORTANT:**
   - ✅ **Check** "Add Python to PATH" (at the bottom)
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation:**
   - **Close and reopen** your terminal (PowerShell/CMD)
   - Run:
   ```powershell
   python --version
   ```
   - You should see: `Python 3.11.x` or similar

**Alternative if `python` doesn't work:** Use the Python Launcher:
```powershell
py --version
```
If `py` works, use `py` instead of `python` in all commands below.

---

### Step 1.2: Fix "Python was not found" (If Python is already installed)

If Python is installed but terminal says "not found":

1. **Disable Microsoft Store alias:**
   - Press `Win + I` → **Apps** → **Advanced app settings** → **App execution aliases**
   - Turn **OFF** the toggles for:
     - `python.exe`
     - `python3.exe`

2. **Add Python to PATH manually:**
   - Find where Python is installed (e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`)
   - Press `Win + R`, type `sysdm.cpl`, press Enter
   - **Advanced** tab → **Environment Variables**
   - Under "User variables", select **Path** → **Edit** → **New**
   - Add: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\`
   - And: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\Scripts\`
   - Click OK, then **restart your terminal**

---

## Part 2: Run the Backend (Step by Step)

### Step 2.1: Open Terminal in Project Root

```powershell
# Navigate to project folder
cd D:\Data-Science-Intelligent-Systems
```

### Step 2.2: Go to Backend Folder

```powershell
cd backend
```

### Step 2.3: Install Python Dependencies (REQUIRED - Fixes "No module named 'flask'")

```powershell
# Use whichever works on your system:
pip install -r requirements.txt

# OR if you use 'py' launcher:
py -m pip install -r requirements.txt

# OR if pip doesn't work:
python -m pip install -r requirements.txt
```

**Wait for all packages to install.** You should see:
```
Successfully installed flask-3.0.0 flask-cors-4.0.0 pandas-2.1.4 ...
```

### Step 2.4: Start the Backend Server

```powershell
# Use whichever works:
python app.py

# OR:
py app.py
```

**Expected output:**
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

**Leave this terminal open.** The backend must keep running.

### Step 2.5: Verify Backend

- Open browser: **http://localhost:5000/api/health**
- You should see: `{"status":"healthy","model_loaded":false,"preprocessor_loaded":false}`
- (model_loaded can be false until you train models)

---

## Part 3: Run the Frontend (Step by Step)

### Step 3.1: Open a NEW Terminal

- Keep the backend terminal running
- Open a **second** terminal (PowerShell or CMD)

### Step 3.2: Go to Project and Frontend Folder

```powershell
cd D:\Data-Science-Intelligent-Systems
cd frontend
```

### Step 3.3: Install Frontend Dependencies (First Time Only)

```powershell
npm install
```

**Wait for installation.** You may see:
```
added 1500 packages in 2m
```

### Step 3.4: Start the Frontend

```powershell
npm start
```

**Expected output:**
```
Compiled successfully!
You can now view the app in the browser.
Local: http://localhost:3000
```

The browser should open automatically at **http://localhost:3000**.

---

## Part 4: Quick Reference - Copy-Paste Commands

### Terminal 1 (Backend)

```powershell
cd D:\Data-Science-Intelligent-Systems\backend
pip install -r requirements.txt
python app.py
```
*(Use `py app.py` if `python` doesn't work)*

### Terminal 2 (Frontend)

```powershell
cd D:\Data-Science-Intelligent-Systems\frontend
npm install
npm start
```

---

## Summary: Order of Execution

| Step | Command | Where |
|------|---------|--------|
| 1 | Install Python (if needed) | - |
| 2 | `cd D:\Data-Science-Intelligent-Systems\backend` | Terminal 1 |
| 3 | `pip install -r requirements.txt` | Terminal 1 |
| 4 | `python app.py` or `py app.py` | Terminal 1 |
| 5 | `cd D:\Data-Science-Intelligent-Systems\frontend` | Terminal 2 |
| 6 | `npm install` | Terminal 2 |
| 7 | `npm start` | Terminal 2 |
| 8 | Open http://localhost:3000 in browser | Browser |

---

## Troubleshooting

### "Python was not found"
→ Follow **Part 1** to install Python or fix PATH.

### "No module named 'flask'"
→ Run `pip install -r requirements.txt` inside the `backend` folder (Step 2.3).

### "pip is not recognized"
→ Use: `py -m pip install -r requirements.txt`

### "npm is not recognized"
→ Install Node.js from https://nodejs.org/ (LTS version). Restart terminal after install.

### Port 5000 or 3000 already in use
→ Close other apps using those ports, or see RUN_COMMANDS.md for changing ports.

---

## Stop the Project

- In **Terminal 1** (backend): Press `Ctrl + C`
- In **Terminal 2** (frontend): Press `Ctrl + C`

---

**Last Updated:** January 2026
