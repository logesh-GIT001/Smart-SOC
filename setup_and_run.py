import os
import sys
import subprocess
import urllib.request

print("=" * 50)
print("   Smart SOC — Automated Setup")
print("=" * 50)

# Step 1 — Install dependencies
print("\n📦 Step 1: Installing dependencies...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
print("✅ Dependencies installed!")

# Step 2 — Download dataset
print("\n📥 Step 2: Downloading NSL-KDD dataset...")
os.makedirs("data/raw", exist_ok=True)

train_url = "https://raw.githubusercontent.com/logesh-GIT001/Smart-SOC/main/data/raw/KDDTrain%2B.txt"
test_url  = "https://raw.githubusercontent.com/logesh-GIT001/Smart-SOC/main/data/raw/KDDTest%2B.txt"

if not os.path.exists("data/raw/KDDTrain+.txt"):
    print("  Downloading KDDTrain+.txt...")
    urllib.request.urlretrieve(train_url, "data/raw/KDDTrain+.txt")

if not os.path.exists("data/raw/KDDTest+.txt"):
    print("  Downloading KDDTest+.txt...")
    urllib.request.urlretrieve(test_url, "data/raw/KDDTest+.txt")

print("✅ Dataset ready!")

# Step 3 — Train model
print("\n🤖 Step 3: Training XGBoost model (3-4 minutes)...")

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
import joblib

columns = [
    'duration','protocol_type','service','flag','src_bytes',
    'dst_bytes','land','wrong_fragment','urgent','hot',
    'num_failed_logins','logged_in','num_compromised','root_shell',
    'su_attempted','num_root','num_file_creations','num_shells',
    'num_access_files','num_outbound_cmds','is_host_login',
    'is_guest_login','count','srv_count','serror_rate',
    'srv_serror_rate','rerror_rate','srv_rerror_rate','same_srv_rate',
    'diff_srv_rate','srv_diff_host_rate','dst_host_count',
    'dst_host_srv_count','dst_host_same_srv_rate','dst_host_diff_srv_rate',
    'dst_host_same_src_port_rate','dst_host_srv_diff_host_rate',
    'dst_host_serror_rate','dst_host_srv_serror_rate','dst_host_rerror_rate',
    'dst_host_srv_rerror_rate','label','difficulty'
]

train_df = pd.read_csv("data/raw/KDDTrain+.txt", names=columns)
test_df  = pd.read_csv("data/raw/KDDTest+.txt",  names=columns)

train_df.drop(columns=['num_outbound_cmds','difficulty'], inplace=True)
test_df.drop(columns=['num_outbound_cmds','difficulty'],  inplace=True)

le = LabelEncoder()
cat_cols = ['protocol_type','service','flag']
for col in cat_cols:
    all_values = pd.concat([train_df[col], test_df[col]])
    le.fit(all_values)
    train_df[col] = le.transform(train_df[col])
    test_df[col]  = le.transform(test_df[col])

def categorize(label):
    dos   = ['neptune','back','land','pod','smurf','teardrop']
    probe = ['ipsweep','nmap','portsweep','satan']
    r2l   = ['ftp_write','guess_passwd','imap','multihop','phf','spy','warezclient','warezmaster']
    u2r   = ['buffer_overflow','loadmodule','perl','rootkit']
    if label == 'normal': return 0
    elif label in dos:    return 1
    elif label in probe:  return 2
    elif label in r2l:    return 3
    elif label in u2r:    return 4
    else:                 return 1

train_df['label'] = train_df['label'].apply(categorize)
test_df['label']  = test_df['label'].apply(categorize)

X_train = train_df.drop(columns=['label'])
y_train = train_df['label']

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

smote = SMOTE(random_state=42)
X_train_bal, y_train_bal = smote.fit_resample(X_train_scaled, y_train)

model = XGBClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1,
    eval_metric='mlogloss'
)
model.fit(X_train_bal, y_train_bal)

# Step 4 — Save model files
print("\n💾 Step 4: Saving model files...")
os.makedirs("models/saved", exist_ok=True)
joblib.dump(model,  "models/saved/xgb_model.pkl")
joblib.dump(scaler, "models/saved/scaler.pkl")
pd.Series(list(X_train.columns)).to_csv("models/saved/feature_names.csv", index=False)
print("✅ Model saved!")

# Step 5 — Start API and Dashboard
print("\n🚀 Step 5: Starting Smart SOC...")
print("\n✅ Setup complete!")
print("=" * 50)
print("  Dashboard → http://localhost:8501")
print("  API       → http://localhost:8000")
print("  API Docs  → http://localhost:8000/docs")
print("=" * 50)

import threading
import time

def start_api():
    subprocess.call([
        sys.executable, "-m", "uvicorn",
        "api.main:app", "--port", "8000"
    ])

api_thread = threading.Thread(target=start_api, daemon=True)
api_thread.start()

time.sleep(2)

subprocess.call([
    sys.executable, "-m", "streamlit",
    "run", "dashboard/app.py"
])
