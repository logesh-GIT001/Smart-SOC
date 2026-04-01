import streamlit as st
import requests
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Smart SOC",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Smart SOC — ML Threat Triage")
st.markdown("Submit network traffic data to detect and explain threats in real time.")

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

    col1, col2 = st.columns(2)

    with col1:
        prediction = result['prediction']
        confidence = result['confidence']

        if prediction == "Normal":
            st.success(f"✅ {prediction}")
        else:
            st.error(f"🚨 {prediction} ATTACK DETECTED!")

        st.metric("Confidence", f"{confidence}%")

        # Show impact levels
        st.subheader("🔍 Why this decision?")
        for item in result['explanation']:
            st.write(f"**{item['feature']}** → {item['impact_level']} ({item['impact_score']})")

    with col2:
        explanation = result['explanation']
        df = pd.DataFrame(explanation)

        fig = px.bar(
            df,
            x='impact_score',
            y='feature',
            orientation='h',
            title='Feature Impact',
            color='impact_score',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📊 Full Response")
    st.json(result)

else:
    st.info("👈 Fill in the network flow details on the left and click Analyze!")
