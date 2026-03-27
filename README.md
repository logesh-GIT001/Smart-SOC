# 🛡️ Smart SOC — ML-Based Threat Triage with Explainable AI

> Automatically classify and prioritize network threats using machine learning, with SHAP-powered explanations so analysts understand *why* each alert was flagged.

---

## Architecture

```
 Network Traffic        Preprocessing           XGBoost Model
 ┌─────────────┐       ┌─────────────┐         ┌─────────────┐
 │  NSL-KDD    │──────▶│   Encode    │────────▶│  74.78%     │
 │  125,973    │       │   Scale     │         │  accuracy   │
 │  records    │       │   SMOTE     │         └──────┬──────┘
 └─────────────┘       └─────────────┘                │
                                                       ▼
 Streamlit UI           FastAPI                 SHAP Explainer
 ┌─────────────┐       ┌─────────────┐         ┌─────────────┐
 │  Alert      │◀──────│  POST       │◀────────│  Feature    │
 │  review     │       │  /triage    │         │  impact     │
 │  dashboard  │       └─────────────┘         └─────────────┘
 └─────────────┘
        │
        ▼
 ┌─────────────────────────────────┐
 │  Analyst output                 │
 │  Prediction + confidence + why  │
 └─────────────────────────────────┘
```

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
| Language | Python 3.10+ |

---

## Project Structure

```
Smart-SOC/
├── data/
│   ├── raw/                  # NSL-KDD dataset
│   ├── processed/            # Cleaned, scaled, balanced data
│   └── samples/
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_model_training.ipynb
│   └── 04_xai_shap.ipynb
├── models/
│   └── saved/
│       ├── xgb_model.pkl
│       ├── scaler.pkl
│       └── feature_names.csv
├── api/
│   └── main.py               # FastAPI triage endpoint
├── dashboard/
│   └── app.py                # Streamlit dashboard
├── docs/
├── scripts/
├── tests/
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

| Service | URL |
|---|---|
| Dashboard | http://localhost:8501 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## API Reference

### `POST /triage`

Submit a network flow for real-time threat classification.

**Request**
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

**Response**
```json
{
  "prediction": "DoS",
  "confidence": 99.95,
  "explanation": [
    { "feature": "src_bytes",     "impact": 3.46 },
    { "feature": "count",         "impact": 1.17 },
    { "feature": "serror_rate",   "impact": 1.07 },
    { "feature": "dst_bytes",     "impact": 1.05 },
    { "feature": "protocol_type", "impact": 0.89 }
  ]
}
```

**Attack categories**

| Label | Type | Description |
|---|---|---|
| `Normal` | — | Legitimate traffic |
| `DoS` | Denial of Service | Flood-based attacks — neptune, smurf, teardrop |
| `Probe` | Reconnaissance | Port scans — ipsweep, nmap, portsweep |
| `R2L` | Remote to Local | Unauthorized access — guess_passwd, ftp_write |
| `U2R` | User to Root | Privilege escalation — buffer_overflow, rootkit |

---

## Dataset

**NSL-KDD** — refined version of the KDD Cup 1999 dataset.

| Property | Value |
|---|---|
| Training records | 125,973 |
| Test records | 22,544 |
| Features | 41 |
| After SMOTE | 336,715 |
| Classes | Normal, DoS, Probe, R2L, U2R |
| Missing values | 0 |

---

## Model Results

| Model | Accuracy | Notes |
|---|---|---|
| Random Forest | 73.17% | Strong on Normal + Probe |
| **XGBoost** | **74.78%** | **Winner — better R2L and U2R detection** |

**XGBoost classification report (test set)**

| Class | Precision | Recall | F1 |
|---|---|---|---|
| Normal | 0.68 | 0.97 | 0.80 |
| DoS | 0.99 | 0.63 | 0.77 |
| Probe | 0.50 | 1.00 | 0.67 |
| R2L | 0.99 | 0.16 | 0.27 |
| U2R | 0.38 | 0.30 | 0.33 |

---

## XAI — Why This Matters

Traditional ML models are black boxes. Smart SOC uses **SHAP (SHapley Additive exPlanations)** to give analysts a clear reason for every alert. Instead of just "this is a DoS attack", the system tells you exactly which network features triggered that decision.

**Key findings per attack type**

| Attack | Top contributing features |
|---|---|
| DoS | `count`, `flag`, `dst_host_rerror_rate` |
| Probe | `src_bytes`, `dst_host_diff_srv_rate` |
| R2L | `src_bytes`, `dst_host_same_src_port_rate` |
| U2R | `dst_host_srv_count`, `duration`, `dst_bytes` |

This makes Smart SOC useful not just as a detector, but as a tool that helps analysts understand and verify every alert — reducing false positive fatigue.

---

## Development Log

| Day | Work done |
|---|---|
| Day 1 | Repo setup, folder structure, requirements |
| Day 2 | EDA on NSL-KDD — attack distribution, feature analysis |
| Day 3 | Preprocessing pipeline — encoding, scaling, SMOTE balancing |
| Day 4 | Trained Random Forest and XGBoost, compared results |
| Day 5 | SHAP integration — feature importance per attack type |
| Day 6 | FastAPI REST endpoint with real-time triage |
| Day 7 | Streamlit dashboard with Plotly explanation chart |
| Day 8 | Final cleanup, run script, documentation |

---

## References

- [NSL-KDD Dataset — University of New Brunswick](https://www.unb.ca/cic/datasets/nsl.html)
- [SHAP Documentation](https://shap.readthedocs.io)
- [XGBoost](https://xgboost.readthedocs.io)
- [FastAPI](https://fastapi.tiangolo.com)
- [Streamlit](https://streamlit.io)
