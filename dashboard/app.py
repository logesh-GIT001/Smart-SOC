import streamlit as st
import requests
from datetime import datetime
import plotly.graph_objects as go

st.set_page_config(page_title="Smart SOC", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif!important;background:#080b12!important;color:#c9d1e0!important;}
#MainMenu,footer{visibility:hidden;}
.block-container{padding:2rem 2.5rem!important;max-width:100%!important;}
[data-testid="stSidebar"]{background:#0b0e17!important;border-right:1px solid #161b2e!important;}
[data-testid="stSidebar"]>div{padding:1.5rem 1rem!important;}
[data-testid="stSidebar"] *{color:#8893a8!important;}
[data-testid="stSidebar"] .stButton>button{background:transparent!important;border:1px solid #161b2e!important;color:#8893a8!important;border-radius:8px!important;width:100%!important;text-align:left!important;padding:9px 12px!important;margin-bottom:5px!important;font-size:13px!important;transition:all 0.15s!important;}
[data-testid="stSidebar"] .stButton>button:hover{background:#161b2e!important;color:#c9d1e0!important;}
</style>
""", unsafe_allow_html=True)

PRESETS = {
    "🟢  Normal traffic": {"Src_Port":56664,"Dst_Port":443,"Protocol":6,"Flow_Duration":115426452,"Total_Fwd_Packet":23,"Total_Bwd_packets":22,"Total_Length_of_Fwd_Packet":699,"Total_Length_of_Bwd_Packet":6797,"Fwd_Packet_Length_Max":342,"Fwd_Packet_Length_Mean":30.39,"Fwd_Packet_Length_Std":82.10,"Bwd_Packet_Length_Max":2636,"Bwd_Packet_Length_Mean":308.95,"Bwd_Packet_Length_Std":728.92,"Flow_Bytes_per_s":64.94,"Flow_Packets_per_s":0.389,"Flow_IAT_Mean":2623328.45,"Flow_IAT_Std":4371348.81,"Flow_IAT_Max":10005116,"Flow_IAT_Min":1,"Fwd_IAT_Total":115426452,"Fwd_IAT_Mean":5246656.91,"Fwd_IAT_Std":4994391.46,"Fwd_IAT_Max":10028546,"Fwd_IAT_Min":3,"Bwd_IAT_Total":115402692,"Bwd_IAT_Mean":5495366.29,"Bwd_IAT_Std":4978568.51,"Bwd_IAT_Max":10028788,"Bwd_IAT_Min":1,"Fwd_PSH_Flags":4,"Bwd_PSH_Flags":5,"Fwd_Header_Length":472,"Bwd_Header_Length":584,"Fwd_Packets_per_s":0.199,"Bwd_Packets_per_s":0.191,"Packet_Length_Max":2636,"Packet_Length_Mean":166.58,"Packet_Length_Std":526.10,"Packet_Length_Variance":276784.75,"FIN_Flag_Count":2,"SYN_Flag_Count":2,"RST_Flag_Count":1,"PSH_Flag_Count":9,"ACK_Flag_Count":44,"Down_Up_Ratio":0.957,"Average_Packet_Size":166.58,"Fwd_Segment_Size_Avg":30.39,"Bwd_Segment_Size_Avg":308.95,"Subflow_Fwd_Bytes":15,"Subflow_Bwd_Bytes":151,"Fwd_Init_Win_Bytes":8192,"Bwd_Init_Win_Bytes":980,"Fwd_Act_Data_Pkts":15,"Fwd_Seg_Size_Min":20,"Active_Mean":40148.18,"Active_Std":54945.63,"Active_Max":205815,"Active_Min":23430,"Idle_Mean":10000721.91,"Idle_Max":10005116,"Idle_Min":9999543,"ICMP_Code":-1,"ICMP_Type":-1,"Total_TCP_Flow_Time":115426452},
    "🔴  DoS attack": {"Src_Port":56684,"Dst_Port":80,"Protocol":6,"Flow_Duration":4041333,"Total_Fwd_Packet":8,"Total_Bwd_packets":6,"Total_Length_of_Fwd_Packet":20,"Total_Length_of_Bwd_Packet":11595,"Fwd_Packet_Length_Max":20,"Fwd_Packet_Length_Mean":2.5,"Fwd_Packet_Length_Std":7.07,"Bwd_Packet_Length_Max":10220,"Bwd_Packet_Length_Mean":1932.5,"Bwd_Packet_Length_Std":4097.11,"Flow_Bytes_per_s":2874.05,"Flow_Packets_per_s":3.46,"Flow_IAT_Mean":310871.77,"Flow_IAT_Std":1090788.39,"Flow_IAT_Max":3940901,"Flow_IAT_Min":1,"Fwd_IAT_Total":4041333,"Fwd_IAT_Mean":577333.29,"Fwd_IAT_Std":1483593.13,"Fwd_IAT_Max":3940901,"Fwd_IAT_Min":1,"Bwd_IAT_Total":59556,"Bwd_IAT_Mean":11911.2,"Bwd_IAT_Std":19452.34,"Bwd_IAT_Max":45246,"Bwd_IAT_Min":1,"Fwd_PSH_Flags":1,"Bwd_PSH_Flags":1,"Fwd_Header_Length":172,"Bwd_Header_Length":132,"Fwd_Packets_per_s":1.98,"Bwd_Packets_per_s":1.48,"Packet_Length_Max":10220,"Packet_Length_Mean":829.64,"Packet_Length_Std":2727.4,"Packet_Length_Variance":7438701.79,"FIN_Flag_Count":2,"SYN_Flag_Count":2,"RST_Flag_Count":1,"PSH_Flag_Count":2,"ACK_Flag_Count":13,"Down_Up_Ratio":0.75,"Average_Packet_Size":829.64,"Fwd_Segment_Size_Avg":2.5,"Bwd_Segment_Size_Avg":1932.5,"Subflow_Fwd_Bytes":1,"Subflow_Bwd_Bytes":828,"Fwd_Init_Win_Bytes":8192,"Bwd_Init_Win_Bytes":229,"Fwd_Act_Data_Pkts":1,"Fwd_Seg_Size_Min":20,"ICMP_Code":-1,"ICMP_Type":-1,"Total_TCP_Flow_Time":4041333},
    "🟡  Probe attack": {"Src_Port":49548,"Dst_Port":2048,"Protocol":6,"Flow_Duration":38,"Total_Fwd_Packet":1,"Total_Bwd_packets":1,"Flow_Packets_per_s":52631.57,"Flow_IAT_Mean":38.0,"Flow_IAT_Max":38,"Flow_IAT_Min":38,"Fwd_Header_Length":40,"Bwd_Header_Length":20,"Fwd_Packets_per_s":26315.78,"Bwd_Packets_per_s":26315.78,"SYN_Flag_Count":1,"RST_Flag_Count":1,"ACK_Flag_Count":1,"Down_Up_Ratio":1.0,"Fwd_Init_Win_Bytes":29200,"Fwd_Seg_Size_Min":40,"Total_TCP_Flow_Time":38,"ICMP_Code":-1,"ICMP_Type":-1},
    "🟠  Brute force": {"Src_Port":60102,"Dst_Port":21,"Protocol":6,"Flow_Duration":8806899,"Total_Fwd_Packet":11,"Total_Bwd_packets":17,"Total_Length_of_Fwd_Packet":123,"Total_Length_of_Bwd_Packet":188,"Fwd_Packet_Length_Max":25,"Fwd_Packet_Length_Mean":11.18,"Fwd_Packet_Length_Std":9.66,"Bwd_Packet_Length_Max":34,"Bwd_Packet_Length_Mean":11.06,"Bwd_Packet_Length_Std":14.23,"Flow_Bytes_per_s":35.31,"Flow_Packets_per_s":3.17,"Flow_IAT_Mean":326181.44,"Flow_IAT_Std":924770.41,"Flow_IAT_Max":3111114,"Flow_IAT_Min":4,"Fwd_IAT_Total":8806844,"Fwd_IAT_Mean":880684.4,"Fwd_IAT_Std":1420112.82,"Fwd_IAT_Max":3154648,"Fwd_IAT_Min":4,"Bwd_IAT_Total":8806846,"Bwd_IAT_Mean":550427.88,"Bwd_IAT_Std":1162195.55,"Bwd_IAT_Max":3111114,"Bwd_IAT_Min":5,"Fwd_PSH_Flags":7,"Bwd_PSH_Flags":7,"Fwd_Header_Length":360,"Bwd_Header_Length":528,"Fwd_Packets_per_s":1.25,"Bwd_Packets_per_s":1.93,"Packet_Length_Max":34,"Packet_Length_Mean":11.11,"Packet_Length_Std":12.43,"Packet_Length_Variance":154.62,"FIN_Flag_Count":2,"SYN_Flag_Count":2,"RST_Flag_Count":2,"PSH_Flag_Count":14,"ACK_Flag_Count":25,"Down_Up_Ratio":1.55,"Average_Packet_Size":11.11,"Fwd_Segment_Size_Avg":11.18,"Bwd_Segment_Size_Avg":11.06,"Subflow_Fwd_Bytes":4,"Subflow_Bwd_Bytes":6,"Fwd_Init_Win_Bytes":29200,"Fwd_Act_Data_Pkts":7,"Fwd_Seg_Size_Min":32,"ICMP_Code":-1,"ICMP_Type":-1,"Total_TCP_Flow_Time":8806899},
    "🟣  Web attack": {"Src_Port":46468,"Dst_Port":80,"Protocol":6,"Flow_Duration":5211399,"Total_Fwd_Packet":4,"Total_Bwd_packets":2,"Flow_Packets_per_s":1.15,"Flow_IAT_Mean":1042279.8,"Flow_IAT_Max":5209600,"Flow_IAT_Min":91,"Fwd_IAT_Total":5211399,"Fwd_IAT_Mean":1737133.0,"Fwd_IAT_Std":3007244.64,"Fwd_IAT_Max":5209600,"Fwd_IAT_Min":866,"Bwd_IAT_Total":5210524,"Bwd_IAT_Mean":5210524.0,"Bwd_IAT_Max":5210524,"Bwd_IAT_Min":5210524,"Fwd_Header_Length":136,"Bwd_Header_Length":72,"Fwd_Packets_per_s":0.767,"Bwd_Packets_per_s":0.384,"FIN_Flag_Count":2,"SYN_Flag_Count":2,"ACK_Flag_Count":5,"Down_Up_Ratio":0.5,"Fwd_Init_Win_Bytes":29200,"Bwd_Init_Win_Bytes":227,"Fwd_Seg_Size_Min":32,"Active_Mean":866.0,"Active_Max":866,"Active_Min":866,"Idle_Mean":5209600.0,"Idle_Max":5209600,"Idle_Min":5209600,"Total_TCP_Flow_Time":5211399,"ICMP_Code":-1,"ICMP_Type":-1},
    "🔵  Botnet": {"Src_Port":51307,"Dst_Port":8080,"Protocol":6,"Flow_Duration":709,"Total_Fwd_Packet":1,"Total_Bwd_packets":1,"Flow_Packets_per_s":2820.87,"Flow_IAT_Mean":709.0,"Flow_IAT_Max":709,"Flow_IAT_Min":709,"Fwd_Header_Length":32,"Bwd_Header_Length":20,"Fwd_Packets_per_s":1410.43,"Bwd_Packets_per_s":1410.43,"SYN_Flag_Count":1,"RST_Flag_Count":1,"ACK_Flag_Count":1,"Down_Up_Ratio":1.0,"Fwd_Init_Win_Bytes":8192,"Fwd_Seg_Size_Min":32,"Total_TCP_Flow_Time":709,"ICMP_Code":-1,"ICMP_Type":-1},
}

SEV_COLOR  = {"critical":"#ef4444","high":"#f97316","medium":"#eab308","normal":"#22c55e"}
SEV_BG     = {"critical":"#160808","high":"#160d06","medium":"#141100","normal":"#061410"}
SEV_BORDER = {"critical":"#2d1010","high":"#2d1a08","medium":"#2d2600","normal":"#0d2820"}

def get_sev(pred, conf):
    if pred == "Normal": return "normal"
    if conf >= 90: return "critical"
    if conf >= 65: return "high"
    return "medium"

def call_api(payload):
    try:
        r = requests.post("http://127.0.0.1:8000/triage", json=payload, timeout=15)
        return r.json()
    except Exception as e:
        return {"error": str(e)}

if "alerts" not in st.session_state:
    st.session_state.alerts = []

# Sidebar
with st.sidebar:
    st.markdown("<div style='font-size:17px;font-weight:600;color:#e8edf5;padding-bottom:16px;border-bottom:1px solid #161b2e;margin-bottom:16px;'>🛡️ Smart SOC<br><span style='font-size:11px;color:#2d3554;font-weight:400;'>ML Threat Triage · v2.0</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:10px;font-weight:600;color:#2d3554;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;'>Quick Test</div>", unsafe_allow_html=True)

    for label, payload in PRESETS.items():
        if st.button(label, key=f"btn_{label}"):
            result = call_api(payload)
            if "error" not in result:
                sev = get_sev(result["prediction"], result["confidence"])
                st.session_state.alerts.insert(0, {
                    "prediction": result["prediction"],
                    "confidence": result["confidence"],
                    "explanation": result["explanation"],
                    "severity": sev,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "dst_port": payload.get("Dst_Port", "-"),
                    "protocol": payload.get("Protocol", "-"),
                })
            else:
                st.error(f"❌ {result['error']}")

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    if st.button("🗑️  Clear alerts", key="clear"):
        st.session_state.alerts = []

    st.markdown("<hr style='border:none;border-top:1px solid #161b2e;margin:16px 0;'><div style='font-size:11px;color:#2d3554;line-height:2;'>Dataset · CICIDS-2017<br>Model · XGBoost<br>Accuracy · 99.99%<br>Classes · 6</div>", unsafe_allow_html=True)

# Main
alerts = st.session_state.alerts
total   = len(alerts)
threats = sum(1 for a in alerts if a["severity"] != "normal")
normals = total - threats
avg_c   = round(sum(a["confidence"] for a in alerts) / total, 1) if total else 0.0

# Header
col_h1, col_h2 = st.columns([4,1])
with col_h1:
    st.markdown("<h2 style='color:#e8edf5;font-size:22px;font-weight:600;margin:0;'>🛡️ Smart SOC — ML Threat Triage</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#4a5568;font-size:12px;margin:4px 0 0;'>Powered by CICIDS-2017 · XGBoost · SHAP Explainability</p>", unsafe_allow_html=True)
with col_h2:
    st.markdown("<div style='background:#061410;border:1px solid #0d2b22;border-radius:20px;padding:6px 14px;font-size:12px;color:#34d399;font-weight:500;text-align:center;margin-top:8px;'>● API online · 8000</div>", unsafe_allow_html=True)

st.markdown("<hr style='border:none;border-top:1px solid #161b2e;margin:16px 0 20px;'>", unsafe_allow_html=True)

# Stats
c1,c2,c3,c4 = st.columns(4)
for col, label, value, color, hint in [
    (c1,"Total Alerts",    str(total),   "#e8edf5", "this session"),
    (c2,"Threats",         str(threats), "#ef4444", "require attention"),
    (c3,"Normal Traffic",  str(normals), "#22c55e", "benign flows"),
    (c4,"Avg Confidence",  f"{avg_c}%",  "#eab308", "model certainty"),
]:
    with col:
        st.markdown(f"""
        <div style='background:#0b0e17;border:1px solid #161b2e;border-radius:12px;padding:18px 20px;'>
            <div style='font-size:11px;font-weight:500;color:#4a5568;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;'>{label}</div>
            <div style='font-size:32px;font-weight:600;color:{color};line-height:1;'>{value}</div>
            <div style='font-size:11px;color:#4a5568;margin-top:6px;'>{hint}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

# Two columns
col_left, col_right = st.columns([55,45], gap="large")

with col_left:
    st.markdown("<div style='font-size:11px;font-weight:600;color:#4a5568;text-transform:uppercase;letter-spacing:0.1em;padding-bottom:10px;border-bottom:1px solid #161b2e;margin-bottom:14px;'>Alert Queue</div>", unsafe_allow_html=True)

    if not alerts:
        st.markdown("""
        <div style='background:#0b0e17;border:1px dashed #161b2e;border-radius:12px;padding:4rem 2rem;text-align:center;'>
            <div style='font-size:36px;opacity:0.3;margin-bottom:12px;'>🛡️</div>
            <div style='font-size:14px;color:#4a5568;'>No alerts yet</div>
            <div style='font-size:12px;color:#2d3554;margin-top:6px;'>Click a Quick Test button on the left</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for a in alerts:
            sev   = a["severity"]
            color = SEV_COLOR[sev]
            bg    = SEV_BG[sev]
            bd    = SEV_BORDER[sev]
            conf  = a["confidence"]
            tags  = "".join([
                f"<span style='font-size:11px;padding:3px 9px;border-radius:5px;background:{'#150f0f' if 'CRITICAL' in e['impact_level'] else '#111520'};color:{'#ef4444' if 'CRITICAL' in e['impact_level'] else '#6b7a99'};border:1px solid {'#2d1515' if 'CRITICAL' in e['impact_level'] else '#1e2540'};'>{e['feature']}</span>"
                for e in a["explanation"][:3]
            ])
            st.markdown(f"""
            <div style='background:{bg};border:1px solid {bd};border-radius:12px;padding:16px 18px;margin-bottom:10px;position:relative;overflow:hidden;'>
                <div style='position:absolute;left:0;top:0;bottom:0;width:4px;background:{color};border-radius:12px 0 0 12px;'></div>
                <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;'>
                    <div style='font-size:14px;font-weight:500;color:#e8edf5;padding-left:4px;'>{a['prediction']} detected</div>
                    <span style='font-size:10px;font-weight:700;padding:3px 10px;border-radius:20px;background:{bg};color:{color};border:1px solid {bd};letter-spacing:0.07em;'>{sev.upper()}</span>
                </div>
                <div style='font-size:11px;color:#4a5568;margin-bottom:10px;padding-left:4px;'>Port {a['dst_port']} · Protocol {a['protocol']} · {a['time']}</div>
                <div style='display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px;'>{tags}</div>
                <div style='display:flex;align-items:center;gap:10px;padding-left:4px;'>
                    <div style='font-size:11px;color:#4a5568;width:72px;'>Confidence</div>
                    <div style='flex:1;height:3px;background:#161b2e;border-radius:2px;overflow:hidden;'>
                        <div style='width:{conf}%;height:100%;background:{color};opacity:0.8;border-radius:2px;'></div>
                    </div>
                    <div style='font-size:11px;color:#6b7a99;width:38px;text-align:right;'>{conf}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with col_right:
    st.markdown("<div style='font-size:11px;font-weight:600;color:#4a5568;text-transform:uppercase;letter-spacing:0.1em;padding-bottom:10px;border-bottom:1px solid #161b2e;margin-bottom:14px;'>Latest Alert Detail</div>", unsafe_allow_html=True)

    if not alerts:
        st.markdown("""
        <div style='background:#0b0e17;border:1px dashed #161b2e;border-radius:12px;padding:4rem 2rem;text-align:center;'>
            <div style='font-size:36px;opacity:0.3;margin-bottom:12px;'>🔍</div>
            <div style='font-size:14px;color:#4a5568;'>No alert selected</div>
            <div style='font-size:12px;color:#2d3554;margin-top:6px;'>Run a test to see SHAP explanation</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        latest = alerts[0]
        sev    = latest["severity"]
        color  = SEV_COLOR[sev]
        bg     = SEV_BG[sev]
        bd     = SEV_BORDER[sev]

        st.markdown(f"""
        <div style='background:{bg};border:1px solid {bd};border-radius:12px;padding:18px 20px;margin-bottom:14px;'>
            <div style='display:flex;align-items:center;justify-content:space-between;'>
                <div>
                    <div style='font-size:20px;font-weight:600;color:{color};'>{latest['prediction']}</div>
                    <div style='font-size:12px;color:#4a5568;margin-top:4px;'>Confidence: {latest['confidence']}% · {latest['time']}</div>
                </div>
                <div style='font-size:36px;opacity:0.5;'>{'✅' if sev=='normal' else '🚨'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        exp      = latest["explanation"]
        features = [e["feature"] for e in exp]
        impacts  = [e["impact_score"] for e in exp]
        levels   = [e["impact_level"] for e in exp]
        bcolors  = ["#ef4444" if "CRITICAL" in l else "#f97316" if "HIGH" in l else "#eab308" if "MEDIUM" in l else "#3b82f6" for l in levels]

        fig = go.Figure(go.Bar(
            x=impacts[::-1], y=features[::-1], orientation='h',
            marker=dict(color=bcolors[::-1], line=dict(width=0)),
            text=[f"{v:.3f}" for v in impacts[::-1]],
            textposition='outside', textfont=dict(size=11, color='#6b7a99'),
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0,r=50,t=6,b=6), height=200,
            xaxis=dict(showgrid=True,gridcolor='#111520',color='#4a5568',tickfont=dict(size=10),zeroline=False),
            yaxis=dict(color='#8893a8',tickfont=dict(size=11),automargin=True),
            font=dict(family='Inter, sans-serif'),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})

        st.markdown("<div style='font-size:11px;font-weight:600;color:#4a5568;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;'>Why this decision?</div>", unsafe_allow_html=True)
        for item in exp:
            lvl = item["impact_level"]
            c   = "#ef4444" if "CRITICAL" in lvl else "#f97316" if "HIGH" in lvl else "#eab308" if "MEDIUM" in lvl else "#3b82f6"
            st.markdown(f"""
            <div style='display:flex;align-items:center;justify-content:space-between;padding:9px 12px;border-radius:8px;background:#080b12;border:1px solid #161b2e;margin-bottom:6px;'>
                <span style='font-size:13px;color:#c9d1e0;'>{item['feature']}</span>
                <div style='display:flex;align-items:center;gap:10px;'>
                    <span style='font-size:12px;color:#4a5568;'>{item['impact_score']:.3f}</span>
                    <span style='font-size:11px;font-weight:500;color:{c};'>{lvl}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Distribution
if len(alerts) >= 2:
    st.markdown("<hr style='border:none;border-top:1px solid #161b2e;margin:24px 0 16px;'>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:11px;font-weight:600;color:#4a5568;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;'>Attack Distribution</div>", unsafe_allow_html=True)
    from collections import Counter
    counts = Counter(a["prediction"] for a in alerts)
    cmap   = {"Normal":"#22c55e","DoS":"#ef4444","Probe":"#eab308","BruteForce":"#f97316","WebAttack":"#a855f7","Botnet":"#3b82f6"}
    lbls   = list(counts.keys())
    vals   = list(counts.values())
    fig2 = go.Figure(go.Pie(
        labels=lbls, values=vals,
        marker=dict(colors=[cmap.get(l,"#64748b") for l in lbls], line=dict(color='#080b12',width=3)),
        textinfo='label+percent', textfont=dict(size=12,color='#c9d1e0'), hole=0.55,
    ))
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=0,r=0,t=10,b=10),height=260,showlegend=True,legend=dict(font=dict(size=12,color='#8893a8'),bgcolor='rgba(0,0,0,0)'),font=dict(family='Inter, sans-serif',color='#8893a8'))
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
