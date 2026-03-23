from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import shap
import pandas as pd

app = FastAPI(title="Smart SOC API", version="1.0")

# Load model and scaler
model = joblib.load("models/saved/xgb_model.pkl")
scaler = joblib.load("models/saved/scaler.pkl")
feature_names = pd.read_csv("models/saved/feature_names.csv").iloc[:, 0].tolist()

# Label mapping
labels = {0: "Normal", 1: "DoS", 2: "Probe", 3: "R2L", 4: "U2R"}

# Input schema
class NetworkFlow(BaseModel):
    duration: float = 0
    protocol_type: int = 1
    service: int = 24
    flag: int = 9
    src_bytes: float = 215
    dst_bytes: float = 45076
    land: int = 0
    wrong_fragment: int = 0
    urgent: int = 0
    hot: int = 0
    num_failed_logins: int = 0
    logged_in: int = 1
    num_compromised: int = 0
    root_shell: int = 0
    su_attempted: int = 0
    num_root: int = 0
    num_file_creations: int = 0
    num_shells: int = 0
    num_access_files: int = 0
    is_host_login: int = 0
    is_guest_login: int = 0
    count: float = 1
    srv_count: float = 1
    serror_rate: float = 0
    srv_serror_rate: float = 0
    rerror_rate: float = 0
    srv_rerror_rate: float = 0
    same_srv_rate: float = 1
    diff_srv_rate: float = 0
    srv_diff_host_rate: float = 0
    dst_host_count: float = 255
    dst_host_srv_count: float = 255
    dst_host_same_srv_rate: float = 1
    dst_host_diff_srv_rate: float = 0
    dst_host_same_src_port_rate: float = 0
    dst_host_srv_diff_host_rate: float = 0
    dst_host_serror_rate: float = 0
    dst_host_srv_serror_rate: float = 0
    dst_host_rerror_rate: float = 0
    dst_host_srv_rerror_rate: float = 0

@app.get("/")
def home():
    return {"message": "Smart SOC API is running! 🚀"}

@app.post("/triage")
def triage(flow: NetworkFlow):
    # Prepare input
    input_data = pd.DataFrame([flow.dict()], columns=feature_names)
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)[0]
    confidence = float(model.predict_proba(input_scaled).max())

    # SHAP explanation
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(input_data)
    class_shap = shap_values[0, :, prediction]

    top_features = pd.DataFrame({
        "feature": feature_names,
        "impact": np.abs(class_shap)
    }).sort_values("impact", ascending=False).head(5)

    return {
        "prediction": labels[prediction],
        "confidence": round(confidence * 100, 2),
        "explanation": top_features.to_dict(orient="records")
    }
