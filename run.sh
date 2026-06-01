#!/bin/bash
echo "🛡️ Starting Smart SOC..."
source ~/projects/Smart-SOC/smart-soc-env/bin/activate
echo "🚀 Starting API on port 8000..."
~/projects/Smart-SOC/smart-soc-env/bin/uvicorn api.main:app --port 8000 &
API_PID=$!
sleep 2
echo "🎨 Starting Dashboard on port 8501..."
~/projects/Smart-SOC/smart-soc-env/bin/streamlit run dashboard/app.py
kill $API_PID
