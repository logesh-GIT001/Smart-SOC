import streamlit as st
import requests
import plotly.express as px
import pandas as pd

# Page config
st.set_page_config(
    page_title="Smart SOC",
    page_icon="🛡️",
    layout="wide"
)

# Title
st.title("🛡️ Smart SOC — ML Threat Triage")
st.markdown("Submit network traffic data to detect and explain threats in real time.")

# Sidebar inputs
st.sidebar.header("📥 Network Flow Input")

duration = st.sidebar.number_input("Duration", value=0)
protocol_type = st.sidebar.selectbox("Protocol Type", [0, 1, 2], format_func=lambda x: ["icmp","tcp","udp"][x])
service = st.sidebar.number_input("Service", value=24)
flag = st.sidebar.number_input("Flag", value=9)
src_bytes = st.sidebar.number_input("Src Bytes", value=215)
dst_bytes = st.sidebar.number_input("Dst Bytes", value=45076)
logged_in = st.sidebar.selectbox("Logged In", [0, 1])
count = st.sidebar.number_input("Count", value=1)
srv_count = st.sidebar.number_input("Srv Count", value=1)
serror_rate = st.sidebar.slider("Serror Rate", 0.0, 1.0, 0.0)
dst_host_count = st.sidebar.number_input("Dst Host Count", value=255)
dst_host_srv_count = st.sidebar.number_input("Dst Host Srv Count", value=255)

# Analyze button
if st.sidebar.button("🔍 Analyze Traffic"):
    payload = {
        "duration": duration,
        "protocol_type": protocol_type,
        "service": service,
        "flag": flag,
        "src_bytes": src_bytes,
        "dst_bytes": dst_bytes,
        "logged_in": logged_in,
        "count": count,
        "srv_count": srv_count,
        "serror_rate": serror_rate,
        "dst_host_count": dst_host_count,
        "dst_host_srv_count": dst_host_srv_count
    }

    with st.spinner("Analyzing..."):
        response = requests.post("http://127.0.0.1:8000/triage", json=payload)
        result = response.json()

    # Results
    col1, col2 = st.columns(2)

    with col1:
        prediction = result['prediction']
        confidence = result['confidence']

        if prediction == "Normal":
            st.success(f"✅ {prediction}")
        else:
            st.error(f"🚨 {prediction} ATTACK DETECTED!")

        st.metric("Confidence", f"{confidence}%")

    with col2:
        # Explanation chart
        explanation = result['explanation']
        df = pd.DataFrame(explanation)

        fig = px.bar(
            df,
            x='impact',
            y='feature',
            orientation='h',
            title='Top Features — Why this decision?',
            color='impact',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    # Raw result
    st.subheader("📊 Full Response")
    st.json(result)

else:
    st.info("👈 Fill in the network flow details on the left and click Analyze!")
