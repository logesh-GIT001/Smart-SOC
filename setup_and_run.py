import os
import sys
import subprocess
import urllib.request

print("=" * 50)
print("   Smart SOC — Automated Setup v2.0")
print("   Powered by CICIDS-2017 + XGBoost")
print("=" * 50)

# ── Auto-detect venv or create one ──────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(BASE_DIR, "smart-soc-env")

if sys.platform == "win32":
    VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
    VENV_PIP    = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    VENV_UV     = os.path.join(VENV_DIR, "Scripts", "uvicorn.exe")
    VENV_ST     = os.path.join(VENV_DIR, "Scripts", "streamlit.exe")
else:
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python3")
    VENV_PIP    = os.path.join(VENV_DIR, "bin", "pip")
    VENV_UV     = os.path.join(VENV_DIR, "bin", "uvicorn")
    VENV_ST     = os.path.join(VENV_DIR, "bin", "streamlit")

# If not running inside venv, re-launch with venv Python
if os.path.exists(VENV_PYTHON) and sys.executable != VENV_PYTHON:
    print(f"\n🔄 Switching to venv Python...")
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

# If venv doesn't exist, create it
if not os.path.exists(VENV_PYTHON):
    print("\n🔧 Creating virtual environment...")
    subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    print("✅ Virtual environment created!")
    print("🔄 Restarting with venv Python...")
    os.execv(VENV_PYTHON, [VENV_PYTHON] + sys.argv)

# Step 1 — Install dependencies
print("\n📦 Step 1: Installing dependencies...")
subprocess.check_call([VENV_PYTHON, "-m", "pip", "install", "-r",
                       os.path.join(BASE_DIR, "requirements.txt"), "-q"])
print("✅ Dependencies installed!")

# Step 2 — Check model files
print("\n🔍 Step 2: Checking model files...")
os.makedirs("models/saved", exist_ok=True)

required_files = [
    "models/saved/xgb_cicids_model.pkl",
    "models/saved/cicids_scaler.pkl",
    "models/saved/cicids_label_encoder.pkl",
    "models/saved/cicids_feature_names.csv",
]

missing = [f for f in required_files if not os.path.exists(f)]

if missing:
    print("\n⚠️  Model files not found:")
    for f in missing:
        print(f"   ❌ {f}")
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
To generate model files:
1. Open Google Colab → https://colab.research.google.com
2. Run notebook: notebooks/06_cicids_preprocessing.ipynb
3. Download these 4 files:
   - xgb_cicids_model.pkl
   - cicids_scaler.pkl
   - cicids_label_encoder.pkl
   - cicids_feature_names.csv
4. Place them in models/saved/
5. Run this script again
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    sys.exit(1)

print("✅ All model files found!")

# Step 3 — Verify model loads correctly
print("\n🤖 Step 3: Verifying model...")
try:
    import joblib
    import pandas as pd
    model   = joblib.load("models/saved/xgb_cicids_model.pkl")
    scaler  = joblib.load("models/saved/cicids_scaler.pkl")
    le      = joblib.load("models/saved/cicids_label_encoder.pkl")
    features = pd.read_csv("models/saved/cicids_feature_names.csv").iloc[:, 0].tolist()
    print(f"✅ Model loaded — {len(features)} features")
    print(f"✅ Classes: {list(le.classes_)}")
except Exception as e:
    print(f"❌ Model verification failed: {e}")
    sys.exit(1)

# Step 4 — Start API and Dashboard
print("\n🚀 Step 4: Starting Smart SOC...")
print("\n✅ Setup complete!")
print("=" * 50)
print("  Dashboard → http://localhost:8501")
print("  API       → http://localhost:8000")
print("  API Docs  → http://localhost:8000/docs")
print("=" * 50)
print("\nPress Ctrl+C to stop.\n")

import threading
import time

os.chdir(BASE_DIR)

def start_api():
    subprocess.call([VENV_UV, "api.main:app", "--port", "8000"])

api_thread = threading.Thread(target=start_api, daemon=True)
api_thread.start()

time.sleep(3)

subprocess.call([VENV_ST, "run", os.path.join(BASE_DIR, "dashboard/app.py")])
