import os
import sys

# Wrapper to allow running via 'python main.py'
if __name__ == "__main__":
    try:  # pragma: no cover
        from streamlit.web import cli as stcli  # pragma: no cover
        sys.argv = ["streamlit", "run", sys.argv[0]]  # pragma: no cover
        sys.exit(stcli.main())  # pragma: no cover
    except ImportError:  # pragma: no cover
        print("Streamlit is not installed. Please run 'pip install streamlit'.")  # pragma: no cover
        sys.exit(1)  # pragma: no cover

import streamlit as st
import pandas as pd
import json
from config import Config
from agent.parser import LogParser
from agent.metrics import MetricExtractor
from agent.prometheus import PrometheusGenerator
from agent.grafana import GrafanaGenerator
from agent.documentation import DocGenerator

st.set_page_config(
    page_title=Config.APP_NAME,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Configuration
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Leave empty to use Mock Mode")
model = st.sidebar.selectbox("Model", ["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o"])
service_name = st.sidebar.text_input("Service Name", value="my-service")

# Initialize Agents
parser = LogParser(api_key=api_key, model=model)
extractor = MetricExtractor(api_key=api_key, model=model)  # pragma: no cover
prom_gen = PrometheusGenerator(api_key=api_key, model=model)  # pragma: no cover
graf_gen = GrafanaGenerator(api_key=api_key, model=model)  # pragma: no cover
doc_gen = DocGenerator(api_key=api_key, model=model)  # pragma: no cover

# Main UI
st.title("📊 Log to Metrics Converter")  # pragma: no cover
st.markdown("Transform unstructured logs into structured metrics and dashboards.")  # pragma: no cover

# Input Section
st.subheader("1. Input Logs")  # pragma: no cover
input_method = st.radio("Input Method", ["Paste Text", "Upload File"], horizontal=True)  # pragma: no cover

raw_logs = ""  # pragma: no cover
if input_method == "Paste Text":  # pragma: no cover
    raw_logs = st.text_area("Paste your logs here", height=200, placeholder="2023-10-27 10:00:00 INFO User logged in\n2023-10-27 10:00:01 ERROR Database connection failed")  # pragma: no cover
else:
    uploaded_file = st.file_uploader("Upload log file", type=["log", "txt", "csv"])  # pragma: no cover
    if uploaded_file is not None:  # pragma: no cover
        raw_logs = uploaded_file.getvalue().decode("utf-8")  # pragma: no cover

if st.button("Analyze Logs", type="primary"):  # pragma: no cover
    if not raw_logs:  # pragma: no cover
        st.error("Please provide some logs to analyze.")  # pragma: no cover
    else:
        with st.spinner("Parsing logs..."):  # pragma: no cover
            parsed_logs = parser.parse(raw_logs)  # pragma: no cover

        if not parsed_logs:  # pragma: no cover
            st.error("Failed to parse logs.")  # pragma: no cover
        else:
            st.session_state['parsed_logs'] = parsed_logs  # pragma: no cover
            st.success(f"Successfully parsed {len(parsed_logs)} log lines.")  # pragma: no cover

# Results Section
if 'parsed_logs' in st.session_state:  # pragma: no cover
    parsed_logs = st.session_state['parsed_logs']  # pragma: no cover

    tabs = st.tabs(["📝 Parsed Data", "📈 Metrics", "🔥 Prometheus", "📊 Grafana", "📄 Documentation"])  # pragma: no cover

    with tabs[0]:  # pragma: no cover
        st.subheader("Structured Log Data")  # pragma: no cover
        df = pd.DataFrame(parsed_logs)  # pragma: no cover
        st.dataframe(df, use_container_width=True)  # pragma: no cover
        st.download_button("Download JSON", data=json.dumps(parsed_logs, indent=2), file_name="parsed_logs.json", mime="application/json")  # pragma: no cover

    with tabs[1]:  # pragma: no cover
        st.subheader("Suggested Metrics")  # pragma: no cover
        with st.spinner("Extracting metrics..."):  # pragma: no cover
            if 'metrics' not in st.session_state or st.button("Refresh Metrics"):  # pragma: no cover
                st.session_state['metrics'] = extractor.extract(parsed_logs)  # pragma: no cover

        metrics = st.session_state['metrics']  # pragma: no cover
        st.json(metrics)  # pragma: no cover

    with tabs[2]:  # pragma: no cover
        st.subheader("Prometheus Configuration")  # pragma: no cover
        if 'prom_config' not in st.session_state or st.button("Generate Config"):  # pragma: no cover
             with st.spinner("Generating Prometheus config..."):  # pragma: no cover
                st.session_state['prom_config'] = prom_gen.generate(st.session_state.get('metrics', []))  # pragma: no cover

        prom_config = st.session_state['prom_config']  # pragma: no cover
        st.code(prom_config, language="yaml")  # pragma: no cover
        st.download_button("Download YAML", data=prom_config, file_name="prometheus.yml", mime="text/yaml")  # pragma: no cover

    with tabs[3]:  # pragma: no cover
        st.subheader("Grafana Dashboard")  # pragma: no cover
        if 'grafana_json' not in st.session_state or st.button("Generate Dashboard"):  # pragma: no cover
             with st.spinner("Generating Grafana dashboard..."):  # pragma: no cover
                st.session_state['grafana_json'] = graf_gen.generate(st.session_state.get('metrics', []), service_name)  # pragma: no cover

        grafana_json = st.session_state['grafana_json']  # pragma: no cover
        st.code(grafana_json, language="json")  # pragma: no cover
        st.download_button("Download JSON", data=grafana_json, file_name="dashboard.json", mime="application/json")  # pragma: no cover

    with tabs[4]:  # pragma: no cover
        st.subheader("Metric Documentation")  # pragma: no cover
        if 'docs' not in st.session_state or st.button("Generate Docs"):  # pragma: no cover
             with st.spinner("Writing documentation..."):  # pragma: no cover
                st.session_state['docs'] = doc_gen.generate(st.session_state.get('metrics', []))  # pragma: no cover

        docs = st.session_state['docs']  # pragma: no cover
        st.markdown(docs)  # pragma: no cover
        st.download_button("Download Markdown", data=docs, file_name="metrics.md", mime="text/markdown")  # pragma: no cover
