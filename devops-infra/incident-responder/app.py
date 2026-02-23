import streamlit as st
import pandas as pd
import time
import json
import os
from agent.monitor import LogMonitor
from agent.analyzer import LogAnalyzer
from agent.reporter import ReportGenerator
from agent.tools import send_slack_alert, trigger_pagerduty_incident
from config import OPENAI_API_KEY, LLM_MODEL

# Page Config
st.set_page_config(page_title="Incident Responder Agent", layout="wide", page_icon="🚨")

# Initialize Session State
if "logs" not in st.session_state:
    st.session_state.logs = []
if "monitoring" not in st.session_state:
    st.session_state.monitoring = False
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = []
if "monitor" not in st.session_state:
    st.session_state.monitor = LogMonitor()

monitor = st.session_state.monitor
analyzer = LogAnalyzer(api_key=OPENAI_API_KEY, model_name=LLM_MODEL)
reporter = ReportGenerator()

# Sidebar
st.sidebar.title("Configuration")
refresh_rate = st.sidebar.slider("Refresh Rate (s)", 0.5, 5.0, 1.0)
st.sidebar.markdown("---")
st.sidebar.subheader("Alert Settings")
slack_enabled = st.sidebar.checkbox("Enable Slack Alerts", value=True)
pagerduty_enabled = st.sidebar.checkbox("Enable PagerDuty Alerts", value=True)

# Main UI
st.title("🚨 Incident Responder Agent")
st.markdown("Real-time log monitoring and automated incident response powered by AI.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Logs")
    log_placeholder = st.empty()

    start_btn = st.button("Start Monitoring")
    stop_btn = st.button("Stop Monitoring")

    if start_btn:
        st.session_state.monitoring = True
    if stop_btn:
        st.session_state.monitoring = False

with col2:
    st.subheader("Incident Analysis")
    analysis_placeholder = st.empty()

# Monitoring Loop
if st.session_state.monitoring:
    # Generate a log entry
    log_entry = monitor.generate_log_entry()
    st.session_state.logs.append(log_entry)

    # Keep only last 100 logs
    if len(st.session_state.logs) > 100:
        st.session_state.logs.pop(0)

    # Display Logs
    df = pd.DataFrame(st.session_state.logs)
    # Sort by timestamp desc
    df = df.sort_values(by="timestamp", ascending=False)

    # Color code rows based on level
    def color_coding(row):
        val = row.loc['level']
        if val == 'ERROR':
            return ['background-color: #ffcccc'] * len(row)
        elif val == 'WARNING':
            return ['background-color: #ffebcc'] * len(row)
        else:
            return [''] * len(row)

    log_placeholder.dataframe(df.style.apply(color_coding, axis=1), use_container_width=True)

    # Analyze Batch (every 10 logs)
    if len(st.session_state.logs) % 10 == 0 and len(st.session_state.logs) > 0:
        with st.spinner("Analyzing recent logs..."):
            batch = st.session_state.logs[-10:]
            analysis = analyzer.analyze_logs(batch)
            st.session_state.analysis_results.insert(0, analysis)

            # Auto-Response Logic
            severity = analysis.get("severity", "UNKNOWN")
            if severity in ["HIGH", "CRITICAL"]:
                st.toast(f"CRITICAL INCIDENT DETECTED! Severity: {severity}", icon="🔥")

                if slack_enabled:
                    send_slack_alert(f"CRITICAL INCIDENT: {analysis.get('summary')}")
                if pagerduty_enabled:
                    trigger_pagerduty_incident(analysis.get('summary'), severity)

                # Generate Report
                report_content = reporter.generate_markdown(analysis)
                filename = f"incident_report_{int(time.time())}.md"
                reporter.save_markdown(filename, report_content)
                st.toast(f"Report saved: {filename}", icon="📄")

    # Display Analysis History
    with analysis_placeholder.container():
        for i, res in enumerate(st.session_state.analysis_results[:5]):
            with st.expander(f"Analysis: {res.get('severity', 'UNKNOWN')} ({res.get('summary', 'No summary')[:50]}...)"):
                st.json(res)
                report_content = reporter.generate_markdown(res)
                st.download_button(
                    label="Download Report",
                    data=report_content,
                    file_name=f"report_{int(time.time())}_{i}.md",
                    mime="text/markdown",
                    key=f"dl_btn_{i}"
                )

    time.sleep(refresh_rate)
    st.rerun()
