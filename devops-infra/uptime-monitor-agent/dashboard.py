import streamlit as st
import pandas as pd
import sys
import os
import time

# Add parent directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.storage import get_latest_results, get_results_by_endpoint, MonitorResult, engine
from sqlalchemy.orm import sessionmaker

# Set page config
st.set_page_config(
    page_title="Uptime Monitor",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stMetric {
        background-color: #262730;
        padding: 10px;
        border-radius: 5px;
    }
    .status-up {
        color: #2ecc71;
        font-weight: bold;
    }
    .status-down {
        color: #e74c3c;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🟢 Uptime Monitor Agent")

# Sidebar
st.sidebar.header("Configuration")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 5, 60, 10)

if st.sidebar.button("Refresh Now"):
    st.rerun()

# Auto refresh
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > refresh_rate:
    st.session_state.last_refresh = time.time()
    st.rerun()

# Get Data
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Fetch latest results per endpoint (distinct endpoint)
    # This is complex in SQL, easiest is to get recent results and group in Pandas
    results = session.query(MonitorResult).order_by(MonitorResult.timestamp.desc()).limit(1000).all()

    data = []
    for r in results:
        data.append({
            "endpoint": r.endpoint,
            "status_code": r.status_code,
            "response_time": r.response_time,
            "timestamp": r.timestamp,
            "error_message": r.error_message,
            "ssl_expiry_days": r.ssl_expiry_days,
            "ai_diagnosis": r.ai_diagnosis
        })

    df = pd.DataFrame(data)

finally:
    session.close()

if df.empty or 'endpoint' not in df.columns:
    st.warning("No monitoring data available yet. Please start the monitor agent: `python main.py`")
    st.info("The dashboard will automatically refresh once data is collected.")
    time.sleep(5)
    st.rerun()

# Overview Metrics
st.header("Overview")

unique_endpoints = df['endpoint'].unique()
if len(unique_endpoints) == 0:
    st.warning("No endpoints found in data.")
    st.stop()

cols = st.columns(min(len(unique_endpoints), 4))

for i, endpoint in enumerate(unique_endpoints):
    endpoint_data = df[df['endpoint'] == endpoint].sort_values('timestamp', ascending=False)
    if endpoint_data.empty:
        continue

    latest = endpoint_data.iloc[0]
    is_up = latest['status_code'] == 200
    status_text = "UP" if is_up else "DOWN"
    status_color = "normal" if is_up else "inverse"
    delta_color = "normal" if is_up else "inverse"

    with cols[i % 4]:
        st.metric(
            label=endpoint,
            value=f"{status_text} ({latest['status_code']})",
            delta=f"{latest['response_time']:.2f}s",
            delta_color=delta_color
        )

# Charts & History
st.header("Response Time History")

chart_data = df.pivot(index='timestamp', columns='endpoint', values='response_time')
st.line_chart(chart_data)

# Recent Failures
st.header("Recent Failures & AI Diagnostics")
failures = df[df['status_code'] != 200].sort_values('timestamp', ascending=False).head(10)

if not failures.empty:
    for _, row in failures.iterrows():
        with st.expander(f"🔴 {row['endpoint']} at {row['timestamp']} (Status: {row['status_code']})"):
            st.write(f"**Error:** {row['error_message']}")
            if row['ai_diagnosis']:
                st.markdown(f"**🤖 AI Diagnosis:**\n\n{row['ai_diagnosis']}")
            else:
                st.info("No AI diagnosis available.")
else:
    st.success("No recent failures detected.")

# SSL Status
st.header("SSL Certificate Status")
ssl_data = df[['endpoint', 'ssl_expiry_days']].drop_duplicates('endpoint', keep='first') # Approximate latest
# Actually we want the latest SSL expiry for each endpoint
latest_ssl = []
for endpoint in unique_endpoints:
    latest = df[df['endpoint'] == endpoint].sort_values('timestamp', ascending=False).iloc[0]
    if pd.notna(latest['ssl_expiry_days']):
        latest_ssl.append({
            "Endpoint": endpoint,
            "Days to Expiry": int(latest['ssl_expiry_days'])
        })

if latest_ssl:
    ssl_df = pd.DataFrame(latest_ssl)
    st.dataframe(ssl_df, hide_index=True)
else:
    st.info("No SSL data available.")
