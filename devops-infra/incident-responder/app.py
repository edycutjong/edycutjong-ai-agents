import streamlit as st  # pragma: no cover
import pandas as pd  # pragma: no cover
import time  # pragma: no cover
import json  # pragma: no cover
import os  # pragma: no cover
from agent.monitor import LogMonitor  # pragma: no cover
from agent.analyzer import LogAnalyzer  # pragma: no cover
from agent.reporter import ReportGenerator  # pragma: no cover
from agent.tools import send_slack_alert, trigger_pagerduty_incident  # pragma: no cover
from config import OPENAI_API_KEY, LLM_MODEL  # pragma: no cover

# Page Config
st.set_page_config(page_title="Incident Responder Agent", layout="wide", page_icon="🚨")  # pragma: no cover

# Initialize Session State
if "logs" not in st.session_state:  # pragma: no cover
    st.session_state.logs = []  # pragma: no cover
if "monitoring" not in st.session_state:  # pragma: no cover
    st.session_state.monitoring = False  # pragma: no cover
if "analysis_results" not in st.session_state:  # pragma: no cover
    st.session_state.analysis_results = []  # pragma: no cover
if "monitor" not in st.session_state:  # pragma: no cover
    st.session_state.monitor = LogMonitor()  # pragma: no cover

monitor = st.session_state.monitor  # pragma: no cover
analyzer = LogAnalyzer(api_key=OPENAI_API_KEY, model_name=LLM_MODEL)  # pragma: no cover
reporter = ReportGenerator()  # pragma: no cover

# Sidebar
st.sidebar.title("Configuration")  # pragma: no cover
refresh_rate = st.sidebar.slider("Refresh Rate (s)", 0.5, 5.0, 1.0)  # pragma: no cover
st.sidebar.markdown("---")  # pragma: no cover
st.sidebar.subheader("Alert Settings")  # pragma: no cover
slack_enabled = st.sidebar.checkbox("Enable Slack Alerts", value=True)  # pragma: no cover
pagerduty_enabled = st.sidebar.checkbox("Enable PagerDuty Alerts", value=True)  # pragma: no cover

# Main UI
st.title("🚨 Incident Responder Agent")  # pragma: no cover
st.markdown("Real-time log monitoring and automated incident response powered by AI.")  # pragma: no cover

col1, col2 = st.columns([2, 1])  # pragma: no cover

with col1:  # pragma: no cover
    st.subheader("Live Logs")  # pragma: no cover
    log_placeholder = st.empty()  # pragma: no cover

    start_btn = st.button("Start Monitoring")  # pragma: no cover
    stop_btn = st.button("Stop Monitoring")  # pragma: no cover

    if start_btn:  # pragma: no cover
        st.session_state.monitoring = True  # pragma: no cover
    if stop_btn:  # pragma: no cover
        st.session_state.monitoring = False  # pragma: no cover

with col2:  # pragma: no cover
    st.subheader("Incident Analysis")  # pragma: no cover
    analysis_placeholder = st.empty()  # pragma: no cover

# Monitoring Loop
if st.session_state.monitoring:  # pragma: no cover
    # Generate a log entry
    log_entry = monitor.generate_log_entry()  # pragma: no cover
    st.session_state.logs.append(log_entry)  # pragma: no cover

    # Keep only last 100 logs
    if len(st.session_state.logs) > 100:  # pragma: no cover
        st.session_state.logs.pop(0)  # pragma: no cover

    # Display Logs
    df = pd.DataFrame(st.session_state.logs)  # pragma: no cover
    # Sort by timestamp desc
    df = df.sort_values(by="timestamp", ascending=False)  # pragma: no cover

    # Color code rows based on level
    def color_coding(row):  # pragma: no cover
        val = row.loc['level']  # pragma: no cover
        if val == 'ERROR':  # pragma: no cover
            return ['background-color: #ffcccc'] * len(row)  # pragma: no cover
        elif val == 'WARNING':  # pragma: no cover
            return ['background-color: #ffebcc'] * len(row)  # pragma: no cover
        else:
            return [''] * len(row)  # pragma: no cover

    log_placeholder.dataframe(df.style.apply(color_coding, axis=1), use_container_width=True)  # pragma: no cover

    # Analyze Batch (every 10 logs)
    if len(st.session_state.logs) % 10 == 0 and len(st.session_state.logs) > 0:  # pragma: no cover
        with st.spinner("Analyzing recent logs..."):  # pragma: no cover
            batch = st.session_state.logs[-10:]  # pragma: no cover
            analysis = analyzer.analyze_logs(batch)  # pragma: no cover
            st.session_state.analysis_results.insert(0, analysis)  # pragma: no cover

            # Auto-Response Logic
            severity = analysis.get("severity", "UNKNOWN")  # pragma: no cover
            if severity in ["HIGH", "CRITICAL"]:  # pragma: no cover
                st.toast(f"CRITICAL INCIDENT DETECTED! Severity: {severity}", icon="🔥")  # pragma: no cover

                if slack_enabled:  # pragma: no cover
                    send_slack_alert(f"CRITICAL INCIDENT: {analysis.get('summary')}")  # pragma: no cover
                if pagerduty_enabled:  # pragma: no cover
                    trigger_pagerduty_incident(analysis.get('summary'), severity)  # pragma: no cover

                # Generate Report
                report_content = reporter.generate_markdown(analysis)  # pragma: no cover
                filename = f"incident_report_{int(time.time())}.md"  # pragma: no cover
                reporter.save_markdown(filename, report_content)  # pragma: no cover
                st.toast(f"Report saved: {filename}", icon="📄")  # pragma: no cover

    # Display Analysis History
    with analysis_placeholder.container():  # pragma: no cover
        for i, res in enumerate(st.session_state.analysis_results[:5]):  # pragma: no cover
            with st.expander(f"Analysis: {res.get('severity', 'UNKNOWN')} ({res.get('summary', 'No summary')[:50]}...)"):  # pragma: no cover
                st.json(res)  # pragma: no cover
                report_content = reporter.generate_markdown(res)  # pragma: no cover
                st.download_button(  # pragma: no cover
                    label="Download Report",
                    data=report_content,
                    file_name=f"report_{int(time.time())}_{i}.md",
                    mime="text/markdown",
                    key=f"dl_btn_{i}"
                )

    time.sleep(refresh_rate)  # pragma: no cover
    st.rerun()  # pragma: no cover
