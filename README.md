# 🛡️ Smart SOC — ML-Based Threat Triage with Explainable AI

> Automatically classify and prioritize network threats using machine learning, with SHAP-powered explanations so analysts understand *why* each alert was flagged — not just *what* it is.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-74.78%25-green?style=flat-square)](https://xgboost.readthedocs.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST-teal?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)](https://streamlit.io)
[![SHAP](https://img.shields.io/badge/XAI-SHAP-orange?style=flat-square)](https://shap.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## 🔍 What This Does

Security Operations Centers are flooded with alerts — most of which are false positives. Analysts waste hours manually investigating noise.

**Smart SOC solves this with:**
- Multi-class threat classification — Normal, DoS, Probe, R2L, U2R
- Real-time triage via FastAPI (REST endpoint)
- SHAP explainability — shows analysts *why* each alert was flagged
- Human-readable impact levels — CRITICAL / HIGH / MEDIUM / LOW
- Streamlit dashboard for visual alert review

---

## 🏗️ System Architecture

```
NSL-KDD Dataset
      │
      ▼
 ┌─────────────────────────────────────────────────┐
 │               Data Pipeline                     │
 │  EDA → Encoding → Scaling → SMOTE Balancing     │
 └─────────────────────────────────────────────────┘
      │
      ▼
 ┌─────────────────────────────────────────────────┐
 │               ML + XAI Layer                    │
 │  XGBoost Classifier + SHAP TreeExplainer        │
 └─────────────────────────────────────────────────┘
      │
      ▼
 ┌──────────────────┐    ┌──────────────────────────┐
 │   FastAPI        │    │   Streamlit Dashboard     │
 │   POST /triage   │◄───│   calls /triage           │
 └──────────────────┘    └──────────────────────────┘
      │
      ▼
 {prediction, confidence, explanation}
 CRITICAL / HIGH / MEDIUM / LOW
```

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| ML Model | XGBoost | Threat classification |
| XAI | SHAP TreeExplainer | Feature-level explanations |
| API | FastAPI + Uvicorn | Real-time triage endpoint |
| Dashboard | Streamlit + Plotly | Visual alert interface |
| Balancing | SMOTE | Handle class imbalance |
| Dataset | NSL-KDD | Network intrusion data |
| Language | Python 3.10+ | Core implementation |

---

## 📊 ML Pipeline Results

| Step | Action | Result |
|---|---|---|
| EDA | Explored 125,973 records | Found 23 attack types across 5 categories |
| Preprocessing | Encode + Scale + SMOTE | Balanced to 336,715 training records |
| Baseline | Random Forest | 73.17% accuracy |
| Final model | XGBoost | **74.78% accuracy** |
| XAI | SHAP TreeExplainer | Per-feature impact on every prediction |
| API | FastAPI endpoint | Real-time triage + explanation |
| Dashboard | Streamlit + Plotly | Visual interface with impact levels |

### Attack categories

| Category | Examples | Records |
|---|---|---|
| Normal | Normal traffic | 67,343 |
| DoS | neptune, smurf, teardrop | 45,927 |
| Probe | ipsweep, nmap, portsweep | 11,656 |
| R2L | ftp_write, guess_passwd | 995 |
| U2R | buffer_overflow, rootkit | 52 |

---

## 🔬 XAI — Why This Matters

Traditional ML models are black boxes. A SOC analyst can't act on "this is DoS" without knowing *why*.

Smart SOC uses **SHAP (SHapley Additive exPlanations)** to give a clear reason for every alert:

| Attack | Top contributing features |
|---|---|
| DoS | `count`, `flag`, `dst_host_rerror_rate` |
| Probe | `src_bytes`, `dst_host_diff_srv_rate` |
| R2L | `src_bytes`, `dst_host_same_src_port_rate` |
| U2R | `dst_host_srv_count`, `duration` |

Every API response includes human-readable impact levels:

```json
{
  "prediction": "DoS",
  "confidence": 99.95,
  "explanation": [
    { "feature": "count",    "impact_score": 4.34, "impact_level": "🔴 CRITICAL" },
    { "feature": "flag",     "impact_score": 1.58, "impact_level": "🟠 HIGH" },
    { "feature": "serror_rate", "impact_score": 0.87, "impact_level": "🟡 MEDIUM" }
  ]
}
```

---

## 📁 Project Structure

```
Smart-SOC/
├── data/
│   ├── raw/                   # NSL-KDD dataset files
│   ├── processed/             # Cleaned, scaled, balanced data
│   └── samples/               # Small sample files for tests
├── notebooks/
│   ├── 01_eda.ipynb           # Exploratory data analysis
│   ├── 02_preprocessing.ipynb # Data cleaning pipeline
│   ├── 03_model_training.ipynb # RF vs XGBoost comparison
│   └── 04_xai_shap.ipynb      # SHAP explanation analysis
├── models/
│   └── saved/
│       ├── xgb_model.pkl      # Trained XGBoost model
│       ├── scaler.pkl         # StandardScaler
│       └── feature_names.csv  # Feature list
├── api/
│   └── main.py                # FastAPI triage endpoint
├── dashboard/
│   └── app.py                 # Streamlit dashboard
├── scripts/                   # Utility scripts
├── tests/                     # Unit tests
├── docs/                      # Architecture diagrams
├── requirements.txt
├── .env.example
├── run.sh                     # Start everything with one command
└── README.md
```

---

## 🚀 Getting Started

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

### 3. Add model files

Train the model by running all cells in `notebooks/03_model_training.ipynb` on Google Colab, then download:
- `models/saved/xgb_model.pkl`
- `models/saved/scaler.pkl`
- `models/saved/feature_names.csv`

### 4. Start everything

```bash
chmod +x run.sh
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

## 📡 API Reference

### `GET /`

Health check.

```json
{ "message": "Smart SOC API is running! 🚀" }
```

### `POST /triage`

Submit a network flow for classification and explanation.

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

**Response — Normal traffic:**
```json
{
  "prediction": "Normal",
  "confidence": 94.24,
  "explanation": [
    { "feature": "dst_host_srv_count", "impact_score": 2.166, "impact_level": "🔴 CRITICAL" },
    { "feature": "hot",                "impact_score": 1.886, "impact_level": "🟠 HIGH" },
    { "feature": "duration",           "impact_score": 0.839, "impact_level": "🟡 MEDIUM" }
  ]
}
```

**Response — DoS attack:**
```json
{
  "prediction": "DoS",
  "confidence": 99.95,
  "explanation": [
    { "feature": "src_bytes", "impact_score": 3.867, "impact_level": "🔴 CRITICAL" },
    { "feature": "count",     "impact_score": 1.172, "impact_level": "🟠 HIGH" },
    { "feature": "duration",  "impact_score": 1.073, "impact_level": "🟠 HIGH" }
  ]
}
```

**Impact levels:**

| Level | Score | Meaning |
|---|---|---|
| 🔴 CRITICAL | ≥ 2.0 | Primary trigger for this alert |
| 🟠 HIGH | ≥ 1.0 | Strong contributing factor |
| 🟡 MEDIUM | ≥ 0.5 | Moderate contribution |
| 🟢 LOW | < 0.5 | Minor influence |

---

## 📓 Notebooks

| Notebook | Description |
|---|---|
| `01_eda.ipynb` | Data exploration — class distribution, feature types, missing values |
| `02_preprocessing.ipynb` | Encoding, scaling, SMOTE balancing |
| `03_model_training.ipynb` | Train RF and XGBoost, compare metrics, save best model |
| `04_xai_shap.ipynb` | SHAP analysis — global and per-record explanations |

---

## 🗂️ Dataset

**NSL-KDD** — refined version of the KDD Cup 1999 dataset.

| Property | Value |
|---|---|
| Training records | 125,973 |
| Test records | 22,544 |
| Features | 41 |
| Classes | Normal, DoS, Probe, R2L, U2R |
| After SMOTE | 336,715 balanced records |

Download from: [Kaggle — NSL-KDD](https://www.kaggle.com/datasets/hassan06/nslkdd)


## 🗺️ Roadmap

- [x] Repo setup and project structure
- [x] NSL-KDD dataset download and EDA
- [x] Feature engineering and preprocessing
- [x] Baseline model — Random Forest (73.17%)
- [x] XGBoost model (74.78%)
- [x] SHAP integration — global and per-record
- [x] FastAPI triage endpoint
- [x] Streamlit dashboard
- [x] Human-readable impact levels
- [ ] LIME explanations (secondary XAI)
- [ ] Unit tests
- [ ] Docker containerization
- [ ] Deploy to cloud (Render / HuggingFace Spaces)

---

## 📚 References

- [NSL-KDD Dataset](https://www.unb.ca/cic/datasets/nsl.html)
- [SHAP Documentation](https://shap.readthedocs.io)
- [XGBoost Documentation](https://xgboost.readthedocs.io)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Streamlit Documentation](https://streamlit.io)
- [SMOTE — imbalanced-learn](https://imbalanced-learn.org)
- [LIME Paper](https://arxiv.org/abs/1602.04938)

---

## 📄 License

MIT License — free to use, modify, and distribute with attribution.
