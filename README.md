# Smart SOC — ML-Based Threat Triage with Explainable AI

> Automatically classify and prioritize security alerts using machine learning, with SHAP-powered explanations so analysts understand *why* each alert was flagged.

---

## What This Does

Security Operations Centers are flooded with alerts — most of which are false positives. Smart SOC uses ML to triage incoming alerts by severity (Critical / High / Medium / Low / Benign), and uses Explainable AI (XAI) to show analysts the top contributing features behind each decision.

**Core capabilities:**
- Multi-class threat classification (attack type + severity)
- Real-time triage via REST API
- SHAP force plots and feature importance for every prediction
- Streamlit dashboard for alert review and model monitoring

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML Models | Scikit-learn, XGBoost, (optional) PyTorch LSTM |
| XAI | SHAP, LIME |
| API | FastAPI + Uvicorn |
| Dashboard | Streamlit + Plotly |
| Dataset | NSL-KDD / CICIDS-2017 |
| Testing | Pytest |

---

## Project Structure

```
Smart-SOC/
├── data/
│   ├── raw/             # Original datasets (not committed — too large)
│   ├── processed/       # Cleaned, feature-engineered data
│   └── samples/         # Small sample files for tests
├── notebooks/           # EDA, model experiments, XAI exploration
├── models/
│   ├── saved/           # Trained model artifacts (.pkl, .pt)
│   └── experiments/     # MLflow or manual experiment logs
├── api/
│   ├── routes/          # FastAPI route handlers
│   └── schemas/         # Pydantic request/response models
├── dashboard/           # Streamlit app
│   ├── components/      # Reusable UI components
│   └── pages/           # Dashboard pages
├── tests/               # Pytest unit + integration tests
├── scripts/             # Data download, preprocessing scripts
├── docs/                # Architecture diagrams, reports
├── requirements.txt
├── .env.example
└── README.md
```

---

## Getting Started

### 1. Clone and install

```bash
git clone https://github.com/logesh-GIT001/Smart-SOC.git
cd Smart-SOC
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set up environment

```bash
cp .env.example .env
# Edit .env with your paths
```

### 3. Download dataset

```bash
# NSL-KDD
python scripts/download_data.py --dataset nsl-kdd

# Or CICIDS-2017 (larger, more realistic)
python scripts/download_data.py --dataset cicids2017
```

### 4. Run preprocessing

```bash
python scripts/preprocess.py
```

### 5. Train a model

```bash
python scripts/train.py --model xgboost
```

### 6. Start the API

```bash
uvicorn api.main:app --reload --port 8000
```

### 7. Launch dashboard

```bash
streamlit run dashboard/app.py
```

---

## API Reference

### `POST /triage`

Submit a network flow for classification.

**Request:**
```json
{
  "duration": 0,
  "protocol_type": "tcp",
  "service": "http",
  "flag": "SF",
  "src_bytes": 215,
  "dst_bytes": 45076
}
```

**Response:**
```json
{
  "alert_id": "uuid",
  "severity": "High",
  "attack_type": "DoS",
  "confidence": 0.92,
  "explanation": {
    "top_features": [
      { "feature": "src_bytes", "impact": 0.43 },
      { "feature": "flag", "impact": 0.31 }
    ],
    "shap_plot_url": "/explain/uuid"
  }
}
```

---

## Team

| Name | Role |
|---|---|
| (your name) | ML lead / model training |
| Teammate 2 | Data pipeline & EDA |
| Teammate 3 | XAI integration & explanations |
| Teammate 4 | API & dashboard |

---

## Roadmap

- [x] Repo setup and project structure
- [ ] Dataset download and EDA
- [ ] Feature engineering pipeline
- [ ] Baseline model (Random Forest)
- [ ] XGBoost + hyperparameter tuning
- [ ] SHAP integration
- [ ] FastAPI triage endpoint
- [ ] Streamlit dashboard
- [ ] LIME explanations
- [ ] Unit tests
- [ ] Final report and demo

---

## Dataset Info

**NSL-KDD** — refined version of the KDD Cup 1999 dataset. 125,973 training records. 41 features. 5 classes: Normal, DoS, Probe, R2L, U2R.

**CICIDS-2017** — more modern, 15 attack types, generated from real network traffic. Recommended for more realistic results.

---

## References

- [NSL-KDD Dataset](https://www.unb.ca/cic/datasets/nsl.html)
- [CICIDS-2017 Dataset](https://www.unb.ca/cic/datasets/ids-2017.html)
- [SHAP Documentation](https://shap.readthedocs.io)
- [LIME Paper](https://arxiv.org/abs/1602.04938)
