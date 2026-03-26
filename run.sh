#!/bin/bash

echo "🛡️  Starting Smart SOC..."

# Activate virtual environment
source smart-soc-env/bin/activate

# Start FastAPI in background
echo "🚀 Starting API on port 8000..."
~/Smart-SOC/smart-soc-env/bin/uvicorn api.main:app --port 8000 &
API_PID=$!

sleep 2

# Start Streamlit dashboard
echo "🎨 Starting Dashboard on port 8501..."
~/Smart-SOC/smart-soc-env/bin/streamlit run dashboard/app.py

# Cleanup on exit
kill $API_PID
EOF
