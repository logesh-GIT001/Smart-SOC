# 🛡️ Smart SOC — ML-Based Threat Triage with Explainable AI

> Automatically classify and prioritize network threats using machine learning, with SHAP-powered explanations so analysts understand *why* each alert was flagged.

---

## What This Does

Security Operations Centers are flooded with alerts — most of which are false positives. Smart SOC uses ML to triage incoming network traffic by attack type, and uses Explainable AI (XAI) to show analysts the top contributing features behind each decision.

**Core capabilities:**
- Multi-class threat classification — Normal, DoS, Probe, R2L, U2R
- Real-time triage via REST API
- SHAP feature importance for every prediction
- Streamlit dashboard for alert review

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML Model | XGBoost |
| XAI | SHAP |
| API | FastAPI + Uvicorn |
| Dashboard | Streamlit + Plotly |
| Dataset | NSL-KDD |

---

## Project Structure
```
Smart-SOC/
├── data/
│   ├── raw/             # NSL-KDD dataset
│   ├── processed/       # Cleaned, scaled, balanced data
│   └── samples/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_xai_shap.ipynb
├── models/
│   └── saved/           # xgb_model.pkl, scaler.pkl, feature_names.csv
├── api/
│   └── main.py          # FastAPI triage endpoint
├── dashboard/
│   └── app.py           # Streamlit dashboard
├── scripts/
├── tests/
├── docs/
├── requirements.txt
├── .env.example
├── run.sh
└── README.md
```

---

## ML Pipeline

| Step | What | Result |
|---|---|---|
| EDA | Explored 125,973 records | 23 attack types across 5 categories |
| Preprocessing | Encoding + Scaling + SMOTE | Balanced to 336,715 records |
| Model Training | Random Forest vs XGBoost | XGBoost — 74.78% accuracy |
| XAI | SHAP TreeExplainer | Per-feature impact on every prediction |
| API | FastAPI REST endpoint | Real-time triage with explanation |
| Dashboard | Streamlit + Plotly | Visual alert review interface |

---

## Getting Started

### 1. Clone and install
```bash
git clone https://github.com/logesh-GIT001/Smart-SOC.git
cd Smart-SOC
python3 -m venv smart-soc-env
source smart-soc-env/bin/activate
pip install -r requirements.txt
```

### 2. Set up environment
```bash
cp .env.example .env
```

### 3. Start everything
```bash
./run.sh
```

Or manually:
```bash
# Terminal 1 — API
uvicorn api.main:app --reload --port 8000

# Terminal 2 — Dashboard
streamlit run dashboard/app.py
```

- API → http://localhost:8000
- Dashboard → http://localhost:8501
- API Docs → http://localhost:8000/docs

---

## API Reference

### `POST /triage`

Submit a network flow for classification.

**Request:**
```json
{
  "duration": 0,
  "protocol_type": 1,
  "service": 24,
  "flag": 9,
  "src_bytes": 215,
  "dst_bytes": 45076,
  "logged_in": 1,
  "count": 1,
  "srv_count": 1
}
```

**Response:**
```json
{
  "prediction": "DoS",
  "confidence": 99.95,
  "explanation": [
    { "feature": "src_bytes",   "impact": 3.46 },
    { "feature": "count",       "impact": 1.17 },
    { "feature": "serror_rate", "impact": 1.07 }
  ]
}
```

---

## Dataset

**NSL-KDD** — refined version of the KDD Cup 1999 dataset.

| Property | Value |
|---|---|
| Training records | 125,973 |
| Test records | 22,544 |
| Features | 41 |
| Classes | Normal, DoS, Probe, R2L, U2R |

After SMOTE balancing: **336,715 training records**

---

## XAI — Why This Matters

Traditional ML models are black boxes. Smart SOC uses **SHAP (SHapley Additive exPlanations)** to give analysts a clear reason for every alert:

- **DoS** → `count` and `flag` are biggest factors
- **Probe** → `src_bytes` matters most
- **R2L** → `src_bytes` and `dst_host_same_src_port_rate`
- **U2R** → `dst_host_srv_count` and `duration`

---

## References

- [NSL-KDD Dataset](https://www.unb.ca/cic/datasets/nsl.html)
- [SHAP Documentation](https://shap.readthedocs.io)
- [XGBoost](https://xgboost.readthedocs.io)
- [FastAPI](https://fastapi.tiangolo.com)
- [Streamlit](https://streamlit.io)
  
