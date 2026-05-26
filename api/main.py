from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import shap
import pandas as pd

app = FastAPI(title="Smart SOC API", version="2.0")

# Load CICIDS model files
model   = joblib.load("models/saved/xgb_cicids_model.pkl")
scaler  = joblib.load("models/saved/cicids_scaler.pkl")
le      = joblib.load("models/saved/cicids_label_encoder.pkl")
feature_names = pd.read_csv("models/saved/cicids_feature_names.csv").iloc[:, 0].tolist()

# Label mapping from encoder
labels = {i: cls for i, cls in enumerate(le.classes_)}

class NetworkFlow(BaseModel):
    Src_Port: int = 80
    Dst_Port: int = 443
    Protocol: int = 6
    Flow_Duration: float = 0
    Total_Fwd_Packet: int = 0
    Total_Bwd_packets: int = 0
    Total_Length_of_Fwd_Packet: float = 0
    Total_Length_of_Bwd_Packet: float = 0
    Fwd_Packet_Length_Max: float = 0
    Fwd_Packet_Length_Min: float = 0
    Fwd_Packet_Length_Mean: float = 0
    Fwd_Packet_Length_Std: float = 0
    Bwd_Packet_Length_Max: float = 0
    Bwd_Packet_Length_Min: float = 0
    Bwd_Packet_Length_Mean: float = 0
    Bwd_Packet_Length_Std: float = 0
    Flow_Bytes_per_s: float = 0
    Flow_Packets_per_s: float = 0
    Flow_IAT_Mean: float = 0
    Flow_IAT_Std: float = 0
    Flow_IAT_Max: float = 0
    Flow_IAT_Min: float = 0
    Fwd_IAT_Total: float = 0
    Fwd_IAT_Mean: float = 0
    Fwd_IAT_Std: float = 0
    Fwd_IAT_Max: float = 0
    Fwd_IAT_Min: float = 0
    Bwd_IAT_Total: float = 0
    Bwd_IAT_Mean: float = 0
    Bwd_IAT_Std: float = 0
    Bwd_IAT_Max: float = 0
    Bwd_IAT_Min: float = 0
    Fwd_PSH_Flags: int = 0
    Bwd_PSH_Flags: int = 0
    Fwd_URG_Flags: int = 0
    Bwd_URG_Flags: int = 0
    Fwd_Header_Length: float = 0
    Bwd_Header_Length: float = 0
    Fwd_Packets_per_s: float = 0
    Bwd_Packets_per_s: float = 0
    Packet_Length_Min: float = 0
    Packet_Length_Max: float = 0
    Packet_Length_Mean: float = 0
    Packet_Length_Std: float = 0
    Packet_Length_Variance: float = 0
    FIN_Flag_Count: int = 0
    SYN_Flag_Count: int = 0
    RST_Flag_Count: int = 0
    PSH_Flag_Count: int = 0
    ACK_Flag_Count: int = 0
    URG_Flag_Count: int = 0
    CWE_Flag_Count: int = 0
    ECE_Flag_Count: int = 0
    Down_Up_Ratio: float = 0
    Average_Packet_Size: float = 0
    Fwd_Segment_Size_Avg: float = 0
    Bwd_Segment_Size_Avg: float = 0
    Fwd_Bytes_per_Bulk_Avg: float = 0
    Fwd_Packet_per_Bulk_Avg: float = 0
    Fwd_Bulk_Rate_Avg: float = 0
    Bwd_Bytes_per_Bulk_Avg: float = 0
    Bwd_Packet_per_Bulk_Avg: float = 0
    Bwd_Bulk_Rate_Avg: float = 0
    Subflow_Fwd_Packets: int = 0
    Subflow_Fwd_Bytes: float = 0
    Subflow_Bwd_Packets: int = 0
    Subflow_Bwd_Bytes: float = 0
    Fwd_Init_Win_Bytes: int = 0
    Bwd_Init_Win_Bytes: int = 0
    Fwd_Act_Data_Pkts: int = 0
    Fwd_Seg_Size_Min: int = 0
    Active_Mean: float = 0
    Active_Std: float = 0
    Active_Max: float = 0
    Active_Min: float = 0
    Idle_Mean: float = 0
    Idle_Std: float = 0
    Idle_Max: float = 0
    Idle_Min: float = 0
    ICMP_Code: int = -1
    ICMP_Type: int = -1
    Total_TCP_Flow_Time: float = 0

@app.get("/")
def home():
    return {"message": "Smart SOC API v2.0 — CICIDS-2017 Model 🚀"}

@app.post("/triage")
def triage(flow: NetworkFlow):
    # Map field names to feature names
    field_map = {
        "Src_Port": "Src Port",
        "Dst_Port": "Dst Port",
        "Protocol": "Protocol",
        "Flow_Duration": "Flow Duration",
        "Total_Fwd_Packet": "Total Fwd Packet",
        "Total_Bwd_packets": "Total Bwd packets",
        "Total_Length_of_Fwd_Packet": "Total Length of Fwd Packet",
        "Total_Length_of_Bwd_Packet": "Total Length of Bwd Packet",
        "Fwd_Packet_Length_Max": "Fwd Packet Length Max",
        "Fwd_Packet_Length_Min": "Fwd Packet Length Min",
        "Fwd_Packet_Length_Mean": "Fwd Packet Length Mean",
        "Fwd_Packet_Length_Std": "Fwd Packet Length Std",
        "Bwd_Packet_Length_Max": "Bwd Packet Length Max",
        "Bwd_Packet_Length_Min": "Bwd Packet Length Min",
        "Bwd_Packet_Length_Mean": "Bwd Packet Length Mean",
        "Bwd_Packet_Length_Std": "Bwd Packet Length Std",
        "Flow_Bytes_per_s": "Flow Bytes/s",
        "Flow_Packets_per_s": "Flow Packets/s",
        "Flow_IAT_Mean": "Flow IAT Mean",
        "Flow_IAT_Std": "Flow IAT Std",
        "Flow_IAT_Max": "Flow IAT Max",
        "Flow_IAT_Min": "Flow IAT Min",
        "Fwd_IAT_Total": "Fwd IAT Total",
        "Fwd_IAT_Mean": "Fwd IAT Mean",
        "Fwd_IAT_Std": "Fwd IAT Std",
        "Fwd_IAT_Max": "Fwd IAT Max",
        "Fwd_IAT_Min": "Fwd IAT Min",
        "Bwd_IAT_Total": "Bwd IAT Total",
        "Bwd_IAT_Mean": "Bwd IAT Mean",
        "Bwd_IAT_Std": "Bwd IAT Std",
        "Bwd_IAT_Max": "Bwd IAT Max",
        "Bwd_IAT_Min": "Bwd IAT Min",
        "Fwd_PSH_Flags": "Fwd PSH Flags",
        "Bwd_PSH_Flags": "Bwd PSH Flags",
        "Fwd_URG_Flags": "Fwd URG Flags",
        "Bwd_URG_Flags": "Bwd URG Flags",
        "Fwd_Header_Length": "Fwd Header Length",
        "Bwd_Header_Length": "Bwd Header Length",
        "Fwd_Packets_per_s": "Fwd Packets/s",
        "Bwd_Packets_per_s": "Bwd Packets/s",
        "Packet_Length_Min": "Packet Length Min",
        "Packet_Length_Max": "Packet Length Max",
        "Packet_Length_Mean": "Packet Length Mean",
        "Packet_Length_Std": "Packet Length Std",
        "Packet_Length_Variance": "Packet Length Variance",
        "FIN_Flag_Count": "FIN Flag Count",
        "SYN_Flag_Count": "SYN Flag Count",
        "RST_Flag_Count": "RST Flag Count",
        "PSH_Flag_Count": "PSH Flag Count",
        "ACK_Flag_Count": "ACK Flag Count",
        "URG_Flag_Count": "URG Flag Count",
        "CWE_Flag_Count": "CWE Flag Count",
        "ECE_Flag_Count": "ECE Flag Count",
        "Down_Up_Ratio": "Down/Up Ratio",
        "Average_Packet_Size": "Average Packet Size",
        "Fwd_Segment_Size_Avg": "Fwd Segment Size Avg",
        "Bwd_Segment_Size_Avg": "Bwd Segment Size Avg",
        "Fwd_Bytes_per_Bulk_Avg": "Fwd Bytes/Bulk Avg",
        "Fwd_Packet_per_Bulk_Avg": "Fwd Packet/Bulk Avg",
        "Fwd_Bulk_Rate_Avg": "Fwd Bulk Rate Avg",
        "Bwd_Bytes_per_Bulk_Avg": "Bwd Bytes/Bulk Avg",
        "Bwd_Packet_per_Bulk_Avg": "Bwd Packet/Bulk Avg",
        "Bwd_Bulk_Rate_Avg": "Bwd Bulk Rate Avg",
        "Subflow_Fwd_Packets": "Subflow Fwd Packets",
        "Subflow_Fwd_Bytes": "Subflow Fwd Bytes",
        "Subflow_Bwd_Packets": "Subflow Bwd Packets",
        "Subflow_Bwd_Bytes": "Subflow Bwd Bytes",
        "Fwd_Init_Win_Bytes": "Fwd Init Win Bytes",
        "Bwd_Init_Win_Bytes": "Bwd Init Win Bytes",
        "Fwd_Act_Data_Pkts": "Fwd Act Data Pkts",
        "Fwd_Seg_Size_Min": "Fwd Seg Size Min",
        "Active_Mean": "Active Mean",
        "Active_Std": "Active Std",
        "Active_Max": "Active Max",
        "Active_Min": "Active Min",
        "Idle_Mean": "Idle Mean",
        "Idle_Std": "Idle Std",
        "Idle_Max": "Idle Max",
        "Idle_Min": "Idle Min",
        "ICMP_Code": "ICMP Code",
        "ICMP_Type": "ICMP Type",
        "Total_TCP_Flow_Time": "Total TCP Flow Time"
    }

    # Build input row
    row = {feature_names[i]: 0 for i in range(len(feature_names))}
    for field, feature in field_map.items():
        if feature in row:
            row[feature] = getattr(flow, field)

    input_data = pd.DataFrame([row], columns=feature_names)
    input_scaled = scaler.transform(input_data)

    # Predict
    prediction = model.predict(input_scaled)[0]
    confidence = float(model.predict_proba(input_scaled).max())

    # SHAP
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(input_data)
    class_shap = shap_values[0, :, prediction]

    top_features = pd.DataFrame({
        "feature": feature_names,
        "impact": np.abs(class_shap)
    }).sort_values("impact", ascending=False).head(5)

    def impact_label(score):
        if score >= 2.0:   return "🔴 CRITICAL"
        elif score >= 1.0: return "🟠 HIGH"
        elif score >= 0.5: return "🟡 MEDIUM"
        else:              return "🟢 LOW"

    explanation = []
    for _, row in top_features.iterrows():
        explanation.append({
            "feature": row["feature"],
            "impact_score": round(row["impact"], 3),
            "impact_level": impact_label(row["impact"])
        })

    return {
        "prediction": labels[prediction],
        "confidence": round(confidence * 100, 2),
        "explanation": explanation
    }
