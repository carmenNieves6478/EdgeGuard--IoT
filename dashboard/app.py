import os
import requests
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------------------------
# STREAMLIT PAGE CONFIGURATION
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="EdgeGuard-IoT | Cyber Intrusion Detection",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# ADVANCED DARK NEON CYBERSECURITY STYLING (CSS)
# ------------------------------------------------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #0B0F19;
        color: #E2E8F0;
    }

    /* Main Container Background */
    .stApp {
        background-color: #0B0F19;
    }

    /* Header Styling */
    .cyber-title {
        font-size: 2.2rem;
        font-weight: 900;
        letter-spacing: 1.5px;
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 50%, #00FF87 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        margin-bottom: 0.2rem;
    }

    .cyber-subtitle {
        font-size: 0.95rem;
        color: #94A3B8;
        font-weight: 400;
        letter-spacing: 0.5px;
        margin-bottom: 1.8rem;
    }

    /* Cyber Card Container */
    .cyber-card {
        background: rgba(17, 24, 39, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 254, 0.2);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.05);
        margin-bottom: 20px;
    }

    /* Threat Status Banners */
    .threat-clean {
        background: rgba(0, 255, 135, 0.1);
        border: 1px solid #00FF87;
        border-radius: 8px;
        padding: 16px;
        color: #00FF87;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1.25rem;
        box-shadow: 0 0 15px rgba(0, 255, 135, 0.2);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .threat-critical {
        background: rgba(255, 0, 85, 0.12);
        border: 1px solid #FF0055;
        border-radius: 8px;
        padding: 16px;
        color: #FF0055;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        font-size: 1.25rem;
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Metric Cards */
    .cyber-metric-card {
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 14px 18px;
        text-align: center;
    }

    .cyber-metric-label {
        font-size: 0.75rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        margin-bottom: 6px;
    }

    .cyber-metric-value {
        font-size: 1.5rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
        color: #00F2FE;
    }

    /* Pulsing Connection Status */
    .status-pulse-online {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #00FF87;
        box-shadow: 0 0 8px #00FF87;
        margin-right: 8px;
    }

    .status-pulse-offline {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #FF0055;
        box-shadow: 0 0 8px #FF0055;
        margin-right: 8px;
    }

    /* Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #070A12;
        border-right: 1px solid rgba(0, 242, 254, 0.15);
    }

    /* Form & Input Adjustments */
    .stButton > button {
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 100%);
        color: #070A12;
        font-weight: 800;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        box-shadow: 0 0 20px rgba(0, 242, 254, 0.6);
        transform: translateY(-1px);
        color: #070A12;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SIDEBAR NAVIGATION & ENGINE CONFIGURATION
# ------------------------------------------------------------------------------
st.sidebar.markdown('<div style="font-size: 1.1rem; font-weight: 900; letter-spacing: 2px; color: #00F2FE; margin-bottom: 12px;">EDGEGUARD SYSTEM</div>', unsafe_allow_html=True)
api_url = st.sidebar.text_input("Backend API Endpoint", os.getenv("API_URL", "http://localhost:8000"))

model_choice = st.sidebar.radio(
    "Inference Engine Mode",
    ["Cloud Stacking Ensemble (LGBM Meta-Learner)", "Edge AI Engine (VAE-MLP INT8 ONNX)"]
)
use_stacking = "Stacking" in model_choice

st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
st.sidebar.markdown('<div style="font-size: 0.8rem; font-weight: 700; color: #64748B; letter-spacing: 1px; margin-bottom: 8px;">SYSTEM CONNECTIVITY</div>', unsafe_allow_html=True)

# Connection Test
api_online = False
try:
    r_health = requests.get(f"{api_url}/health", timeout=2)
    if r_health.status_code == 200 and r_health.json().get("status") == "healthy":
        api_online = True
except Exception:
    api_online = False

if api_online:
    st.sidebar.markdown('<div><span class="status-pulse-online"></span><span style="color: #00FF87; font-weight: 600; font-size: 0.9rem;">SYSTEM ONLINE</span></div>', unsafe_allow_html=True)
else:
    st.sidebar.markdown('<div><span class="status-pulse-offline"></span><span style="color: #FF0055; font-weight: 600; font-size: 0.9rem;">DISCONNECTED</span></div>', unsafe_allow_html=True)

st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style="font-size: 0.75rem; color: #64748B; line-height: 1.6;">
    <b>Architecture Specs:</b><br>
    - Model: VAE-MLP INT8 / Stacking<br>
    - Quantization: Dynamic QUInt8<br>
    - Footprint: 21.67 KB (Edge AI)<br>
    - Benchmark Acc: 77.18% (Cloud)
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# MAIN DASHBOARD HEADER
# ------------------------------------------------------------------------------
st.markdown('<div class="cyber-title">EDGEGUARD-IOT | INTRUSION DETECTION SYSTEM</div>', unsafe_allow_html=True)
st.markdown('<div class="cyber-subtitle">Adaptive Multiclass Botnet Threat Detection Platform & Real-Time XAI Telemetry</div>', unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TWO COLUMN LAYOUT: INPUT TELEMETRY & DIAGNOSTICS
# ------------------------------------------------------------------------------
col_input, col_diag = st.columns([1, 1.8])

with col_input:
    st.markdown('<div style="font-size: 1.0rem; font-weight: 700; color: #00F2FE; letter-spacing: 1px; margin-bottom: 12px;">NETWORK TELEMETRY GENERATOR</div>', unsafe_allow_html=True)
    
    preset = st.selectbox(
        "Attack Scenario Presets",
        [
            "DDoS Packet Flood Attack",
            "Mirai IoT Botnet Infection",
            "Reconnaissance / PortScan",
            "Spoofing / ARP Poisoning",
            "Brute Force Authentication Attack",
            "Web-Based Vulnerability Attack",
            "Benign Network Traffic"
        ]
    )

    # Preset Parameters Mapping
    if preset == "DDoS Packet Flood Attack":
        def_header, def_proto, def_rate, def_psh, def_syn, def_tot_sum, def_tot_size = 20.0, 6.0, 1250.0, 1.0, 1.0, 15000.0, 18000.0
    elif preset == "Mirai IoT Botnet Infection":
        def_header, def_proto, def_rate, def_psh, def_syn, def_tot_sum, def_tot_size = 0.0, 47.0, 850.0, 0.0, 0.0, 2304.0, 3000.0
    elif preset == "Reconnaissance / PortScan":
        def_header, def_proto, def_rate, def_psh, def_syn, def_tot_sum, def_tot_size = 19.92, 6.0, 45.0, 1.0, 0.0, 500.0, 600.0
    elif preset == "Spoofing / ARP Poisoning":
        def_header, def_proto, def_rate, def_psh, def_syn, def_tot_sum, def_tot_size = 32.0, 1.0, 120.0, 0.0, 0.0, 800.0, 1000.0
    elif preset == "Brute Force Authentication Attack":
        def_header, def_proto, def_rate, def_psh, def_syn, def_tot_sum, def_tot_size = 40.0, 6.0, 95.0, 1.0, 0.0, 1200.0, 1400.0
    elif preset == "Web-Based Vulnerability Attack":
        def_header, def_proto, def_rate, def_psh, def_syn, def_tot_sum, def_tot_size = 64.0, 6.0, 35.0, 1.0, 0.0, 3500.0, 4000.0
    else:  # Benign Traffic
        def_header, def_proto, def_rate, def_psh, def_syn, def_tot_sum, def_tot_size = 54.0, 6.0, 2.5, 0.0, 0.0, 120.0, 150.0

    st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
    header_len = st.number_input("Header Length (Bytes)", value=float(def_header))
    protocol = st.number_input("Protocol ID (TCP=6, UDP=17, ICMP=1)", value=float(def_proto))
    rate = st.number_input("Transmission Rate (Packets/sec)", value=float(def_rate))
    psh_flag = st.slider("PSH Flag State", 0.0, 1.0, float(def_psh))
    syn_flag = st.slider("SYN Flag State", 0.0, 1.0, float(def_syn))
    tot_sum = st.number_input("Total Header Sum", value=float(def_tot_sum))
    tot_size = st.number_input("Total Flow Packet Size", value=float(def_tot_size))

    btn_eval = st.button("EXECUTE THREAT ANALYSIS", use_container_width=True)

with col_diag:
    st.markdown('<div style="font-size: 1.0rem; font-weight: 700; color: #00F2FE; letter-spacing: 1px; margin-bottom: 12px;">THREAT DIAGNOSTICS & XAI TELEMETRY</div>', unsafe_allow_html=True)

    if btn_eval or "last_prediction" in st.session_state:
        payload = {
            "Header_Length": header_len,
            "Protocol Type": protocol,
            "Time_To_Live": 64.0,
            "Rate": rate,
            "fin_flag_number": 0.0,
            "syn_flag_number": syn_flag,
            "rst_flag_number": 0.0,
            "psh_flag_number": psh_flag,
            "ack_flag_number": 0.0,
            "ece_flag_number": 0.0,
            "cwr_flag_number": 0.0,
            "ack_count": 0.0,
            "syn_count": syn_flag,
            "fin_count": 0.0,
            "rst_count": 0.0,
            "HTTP": 1.0 if preset == "Web-Based Vulnerability Attack" else 0.0,
            "HTTPS": 0.0,
            "DNS": 0.0,
            "Telnet": 1.0 if preset == "Mirai IoT Botnet Infection" else 0.0,
            "SMTP": 0.0,
            "SSH": 0.0,
            "IRC": 0.0,
            "TCP": 1.0 if protocol == 6.0 else 0.0,
            "UDP": 1.0 if protocol == 17.0 else 0.0,
            "DHCP": 0.0,
            "ARP": 0.0,
            "ICMP": 1.0 if protocol == 1.0 else 0.0,
            "IGMP": 0.0,
            "IPv": 1.0,
            "LLC": 1.0,
            "Tot sum": tot_sum,
            "Min": 64.0,
            "Max": 1500.0,
            "AVG": 400.0,
            "Std": 100.0,
            "Tot size": tot_size,
            "IAT": 0.01,
            "Number": 10.0,
            "Variance": 1000.0,
            "use_stacking_ensemble": use_stacking
        }

        try:
            with st.spinner("Analyzing network payload..."):
                r = requests.post(f"{api_url}/predict", json=payload, timeout=5)
            if r.status_code == 200:
                data = r.json()
                st.session_state["last_prediction"] = data
            else:
                st.error(f"API Error {r.status_code}: {r.text}")
                data = st.session_state.get("last_prediction", None)
        except Exception as err:
            st.error(f"Unable to reach API backend at {api_url}. Detail: {err}")
            data = st.session_state.get("last_prediction", None)

        if data:
            pred_class = data["predicted_class"]
            confidence = data["confidence"] * 100.0
            latency = data["inference_time_ms"]
            top_shap = data["top_3_shap_features"]
            probs = data["all_class_probabilities"]
            model_used = data.get("model_used", "VAE-MLP INT8")

            is_clean = pred_class.upper() == "BENIGN"

            # Status Banner
            if is_clean:
                st.markdown(f'<div class="threat-clean">STATUS: CLEAN TELEMETRY | CLASS: {pred_class.upper()}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="threat-critical">CRITICAL THREAT DETECTED | CATEGORY: {pred_class.upper()}</div>', unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

            # Metric Cards Row
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'''
                <div class="cyber-metric-card">
                    <div class="cyber-metric-label">Classification</div>
                    <div class="cyber-metric-value" style="color: {'#00FF87' if is_clean else '#FF0055'};">{pred_class}</div>
                </div>
                ''', unsafe_allow_html=True)

            with m2:
                st.markdown(f'''
                <div class="cyber-metric-card">
                    <div class="cyber-metric-label">Confidence</div>
                    <div class="cyber-metric-value">{confidence:.1f}%</div>
                </div>
                ''', unsafe_allow_html=True)

            with m3:
                st.markdown(f'''
                <div class="cyber-metric-card">
                    <div class="cyber-metric-label">Latency</div>
                    <div class="cyber-metric-value" style="color: #4FACFE;">{latency:.2f} ms</div>
                </div>
                ''', unsafe_allow_html=True)

            st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

            # Tabbed View for Detailed Analytics
            tab_shap, tab_spectrum, tab_raw = st.tabs(["XAI SHAP Explainability", "Multiclass Probability Spectrum", "Raw Packet Telemetry"])

            with tab_shap:
                df_shap = pd.DataFrame(top_shap)
                
                fig_shap = px.bar(
                    df_shap,
                    x="impact",
                    y="feature",
                    orientation="h",
                    color="impact",
                    color_continuous_scale=[[0, "#111827"], [1, "#00FF87"]] if is_clean else [[0, "#111827"], [1, "#FF0055"]],
                    labels={"impact": "Absolute SHAP Impact", "feature": "Network Feature"}
                )
                fig_shap.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif", color="#E2E8F0"),
                    yaxis=dict(autorange="reversed"),
                    height=280,
                    margin=dict(l=10, r=10, t=20, b=10),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_shap, use_container_width=True)

            with tab_spectrum:
                df_probs = pd.DataFrame(list(probs.items()), columns=["Category", "Probability"])
                df_probs["Percentage"] = df_probs["Probability"] * 100.0

                fig_probs = px.bar(
                    df_probs,
                    x="Category",
                    y="Percentage",
                    text="Percentage",
                    color="Percentage",
                    color_continuous_scale=[[0, "#111827"], [0.5, "#00F2FE"], [1, "#FF0055"]],
                    labels={"Percentage": "Probability (%)", "Category": "Attack Class"}
                )
                fig_probs.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig_probs.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif", color="#E2E8F0"),
                    yaxis=dict(range=[0, 115]),
                    height=280,
                    margin=dict(l=10, r=10, t=20, b=10),
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_probs, use_container_width=True)

            with tab_raw:
                st.json(payload)
