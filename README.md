# 🛡️ Smart SOC — AI-Powered Threat Triage with Explainable AI

> Automatically detect, classify, prioritize, and explain network threats using Machine Learning and Explainable AI (XAI). Built with CICIDS2017, XGBoost, SHAP, FastAPI, and Streamlit.

[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)](https://python.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML-green?style=flat-square)](https://xgboost.readthedocs.io)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST-teal?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-SOC%20Dashboard-red?style=flat-square&logo=streamlit)](https://streamlit.io)
[![SHAP](https://img.shields.io/badge/XAI-SHAP-orange?style=flat-square)](https://shap.readthedocs.io)
[![Dataset](https://img.shields.io/badge/Dataset-CICIDS2017-purple?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## 🔍 What This Does

Security Operations Centers (SOCs) receive thousands of alerts every day. Analysts need to quickly identify real threats, understand why they were detected, and prioritize investigation efforts.

**Smart SOC provides:**

- Multi-class network threat classification
- Real-time threat triage using FastAPI
- Explainable AI using SHAP
- SOC-style analyst dashboard
- Confidence-based severity scoring
- Threat distribution analytics
- Feature impact visualization
- Human-readable alert explanations

---

## 🏗️ System Architecture

```text
CICIDS2017 Dataset
        │
        ▼
┌─────────────────────────────────────────────────┐
│                 Data Pipeline                   │
│      Cleaning → Encoding → Training             │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│                XGBoost Model                    │
│         Multi-Class Classification              │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│              SHAP Explainability                │
│         Feature Impact Analysis                 │
└─────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────┐     ┌────────────────────────┐
│     FastAPI      │     │  Streamlit Dashboard   │
│   POST /triage   │◄───►│   SOC Analyst View     │
└──────────────────┘     └────────────────────────┘
        │
        ▼
Prediction + Confidence + SHAP Explanation
```

---

## ⚙️ Tech Stack

| Layer | Technology | Purpose |
|---------|------------|---------|
| ML Model | XGBoost | Attack classification |
| Explainable AI | SHAP TreeExplainer | Prediction explanation |
| Backend API | FastAPI + Uvicorn | Real-time inference |
| Dashboard | Streamlit | SOC interface |
| Visualization | Plotly | Charts & analytics |
| Dataset | CICIDS2017 | Network intrusion dataset |
| Language | Python 3.10+ | Core implementation |

---

## 🎯 Supported Threat Classes

| Class | Description |
|---------|-------------|
| Normal | Legitimate traffic |
| DoS | Denial of Service attacks |
| Probe | Network reconnaissance |
| Brute Force | Password guessing attacks |
| Web Attack | Web exploitation attempts |
| Botnet | Command-and-control traffic |

---

## 📊 Dashboard Features

### Alert Queue
- Real-time alert list
- Severity-based coloring
- Confidence scoring
- Attack categorization

### Alert Investigation
- SHAP feature importance
- Impact score visualization
- Analyst-friendly explanations
- Attack reasoning

### Analytics
- Threat distribution charts
- Attack frequency tracking
- Confidence metrics
- Alert statistics

### Quick Simulation
- Normal Traffic
- DoS Attack
- Probe Attack
- Brute Force Attack
- Web Attack
- Botnet Traffic

---

## 🔬 Explainable AI (SHAP)

Traditional ML systems only provide a prediction.

Smart SOC explains:

- Why the model generated an alert
- Which features influenced the decision
- How strongly each feature contributed
- Which indicators analysts should investigate first

Example response:

```json
{
  "prediction": "DoS",
  "confidence": 99.4,
  "explanation": [
    {
      "feature": "Flow_Packets_per_s",
      "impact_score": 4.38,
      "impact_level": "CRITICAL"
    },
    {
      "feature": "Packet_Length_Mean",
      "impact_score": 2.11,
      "impact_level": "HIGH"
    },
    {
      "feature": "Flow_Duration",
      "impact_score": 1.24,
      "impact_level": "MEDIUM"
    }
  ]
}
```

---

## 📁 Project Structure

```text
Smart-SOC/
├── api/
│   └── main.py
│
├── dashboard/
│   └── app.py
│
├── models/
│   ├── model.pkl
│   ├── scaler.pkl
│   └── feature_names.pkl
│
├── notebooks/
│   ├── eda.ipynb
│   ├── preprocessing.ipynb
│   ├── training.ipynb
│   └── shap_analysis.ipynb
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── requirements.txt
├── setup_and_run.py
└── README.md
```

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/logesh-GIT001/Smart-SOC.git
cd Smart-SOC
```

### Create Virtual Environment

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Project

```bash
python setup_and_run.py
```

---

## 🌐 Services

| Service | URL |
|----------|-----|
| Dashboard | http://localhost:8501 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 📡 API Reference

### GET /

Health check

```json
{
  "message": "Smart SOC API is running!"
}
```

### POST /triage

Submit network flow features for classification.

Example response:

```json
{
  "prediction": "Botnet",
  "confidence": 98.72,
  "severity": "critical",
  "explanation": [
    {
      "feature": "Flow_Packets_per_s",
      "impact_score": 4.21,
      "impact_level": "CRITICAL"
    }
  ]
}
```

---

## 🗂️ Dataset

### CICIDS2017

The model is trained using the CICIDS2017 dataset, which contains realistic network traffic and modern attack scenarios.

Includes:

- Benign Traffic
- DoS / DDoS
- Port Scanning
- Brute Force
- Web Attacks
- Botnet Activity

---

## 🛣️ Roadmap

- [x] CICIDS2017 preprocessing
- [x] XGBoost classification
- [x] SHAP explainability
- [x] FastAPI inference API
- [x] Streamlit SOC dashboard
- [x] Alert severity scoring
- [x] Threat distribution analytics
- [ ] Live packet capture
- [ ] Real network flow monitoring
- [ ] Suricata integration
- [ ] Zeek integration
- [ ] Docker deployment
- [ ] Cloud deployment
- [ ] SIEM integration

---

## 📚 References

- CICIDS2017 Dataset
- XGBoost Documentation
- SHAP Documentation
- FastAPI Documentation
- Streamlit Documentation
- Plotly Documentation

---

## 📄 License

MIT License

Free to use, modify, and distribute.
