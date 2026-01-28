"""
Setup Diagnostic Script
Checks if all components are properly configured
"""

import sys
from pathlib import Path
import json

def check_file_exists(filepath, description):
    """Check if a file exists."""
    path = Path(filepath)
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    if exists:
        print(f"   Size: {path.stat().st_size} bytes")
    return exists

def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    path = Path(dirpath)
    exists = path.exists() and path.is_dir()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {dirpath}")
    return exists

def main():
    print("=" * 60)
    print("Healthcare Diagnosis DSS - Setup Diagnostic")
    print("=" * 60)
    print()
    
    issues = []
    
    # Check project structure
    print("📁 Project Structure:")
    print("-" * 60)
    dirs = [
        ("ml_models", "ML Models Directory"),
        ("backend", "Backend Directory"),
        ("frontend", "Frontend Directory"),
        ("data", "Data Directory"),
        ("docs", "Documentation Directory"),
    ]
    
    for dirpath, desc in dirs:
        if not check_directory_exists(dirpath, desc):
            issues.append(f"Missing directory: {dirpath}")
    
    print()
    
    # Check ML model files
    print("🤖 ML Model Files:")
    print("-" * 60)
    model_files = [
        ("ml_models/models/best_model.pkl", "Best Model"),
        ("ml_models/models/preprocessor.pkl", "Preprocessor"),
    ]
    
    models_exist = True
    for filepath, desc in model_files:
        if not check_file_exists(filepath, desc):
            models_exist = False
            issues.append(f"Missing model file: {filepath}. Train models first!")
    
    print()
    
    # Check backend files
    print("🔧 Backend Files:")
    print("-" * 60)
    backend_files = [
        ("backend/app.py", "Flask App"),
        ("backend/requirements.txt", "Requirements"),
    ]
    
    for filepath, desc in backend_files:
        check_file_exists(filepath, desc)
    
    print()
    
    # Check frontend files
    print("💻 Frontend Files:")
    print("-" * 60)
    frontend_files = [
        ("frontend/package.json", "Package.json"),
        ("frontend/src/App.js", "React App"),
        ("frontend/src/pages/DiagnosisForm.js", "Diagnosis Form"),
    ]
    
    for filepath, desc in frontend_files:
        check_file_exists(filepath, desc)
    
    print()
    
    # Check Python packages
    print("📦 Python Packages:")
    print("-" * 60)
    try:
        import flask
        print("✅ Flask:", flask.__version__)
    except ImportError:
        print("❌ Flask: Not installed")
        issues.append("Install Flask: pip install flask")
    
    try:
        import pandas
        print("✅ Pandas:", pandas.__version__)
    except ImportError:
        print("❌ Pandas: Not installed")
        issues.append("Install Pandas: pip install pandas")
    
    try:
        import sklearn
        print("✅ scikit-learn:", sklearn.__version__)
    except ImportError:
        print("❌ scikit-learn: Not installed")
        issues.append("Install scikit-learn: pip install scikit-learn")
    
    try:
        import xgboost
        print("✅ XGBoost:", xgboost.__version__)
    except ImportError:
        print("❌ XGBoost: Not installed")
        issues.append("Install XGBoost: pip install xgboost")
    
    try:
        import joblib
        print("✅ Joblib:", joblib.__version__)
    except ImportError:
        print("❌ Joblib: Not installed")
        issues.append("Install Joblib: pip install joblib")
    
    print()
    
    # Summary
    print("=" * 60)
    print("📊 Summary:")
    print("=" * 60)
    
    if not models_exist:
        print("⚠️  WARNING: Model files not found!")
        print("   → Train models first: python ml_models/training/main_training_pipeline.py --csv <dataset> --target <target>")
        print()
    
    if issues:
        print("❌ Issues Found:")
        for issue in issues:
            print(f"   - {issue}")
        print()
        print("💡 Solutions:")
        print("   1. Install missing packages: pip install -r backend/requirements.txt")
        print("   2. Train models if missing: See SETUP_INSTRUCTIONS.md")
        print("   3. Check TROUBLESHOOTING.md for common issues")
    else:
        print("✅ All checks passed!")
        print()
        print("🚀 Next Steps:")
        print("   1. Start backend: cd backend && python app.py")
        print("   2. Start frontend: cd frontend && npm start")
        print("   3. Open browser: http://localhost:3000")
    
    print()
    print("=" * 60)
    
    return len(issues) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
