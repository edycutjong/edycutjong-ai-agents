import os
import sys

# Wrapper to allow running via 'python main.py'
if __name__ == "__main__":
    try:
        from streamlit.web import cli as stcli
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
    except ImportError:
        print("Streamlit is not installed. Please run 'pip install streamlit'.")
        sys.exit(1)

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
extractor = MetricExtractor(api_key=api_key, model=model)
prom_gen = PrometheusGenerator(api_key=api_key, model=model)
graf_gen = GrafanaGenerator(api_key=api_key, model=model)
doc_gen = DocGenerator(api_key=api_key, model=model)

# Main UI
st.title("📊 Log to Metrics Converter")
st.markdown("Transform unstructured logs into structured metrics and dashboards.")

# Input Section
st.subheader("1. Input Logs")
input_method = st.radio("Input Method", ["Paste Text", "Upload File"], horizontal=True)

raw_logs = ""
if input_method == "Paste Text":
    raw_logs = st.text_area("Paste your logs here", height=200, placeholder="2023-10-27 10:00:00 INFO User logged in\n2023-10-27 10:00:01 ERROR Database connection failed")
else:
    uploaded_file = st.file_uploader("Upload log file", type=["log", "txt", "csv"])
    if uploaded_file is not None:
        raw_logs = uploaded_file.getvalue().decode("utf-8")

if st.button("Analyze Logs", type="primary"):
    if not raw_logs:
        st.error("Please provide some logs to analyze.")
    else:
        with st.spinner("Parsing logs..."):
            parsed_logs = parser.parse(raw_logs)

        if not parsed_logs:
            st.error("Failed to parse logs.")
        else:
            st.session_state['parsed_logs'] = parsed_logs
            st.success(f"Successfully parsed {len(parsed_logs)} log lines.")

# Results Section
if 'parsed_logs' in st.session_state:
    parsed_logs = st.session_state['parsed_logs']

    tabs = st.tabs(["📝 Parsed Data", "📈 Metrics", "🔥 Prometheus", "📊 Grafana", "📄 Documentation"])

    with tabs[0]:
        st.subheader("Structured Log Data")
        df = pd.DataFrame(parsed_logs)
        st.dataframe(df, use_container_width=True)
        st.download_button("Download JSON", data=json.dumps(parsed_logs, indent=2), file_name="parsed_logs.json", mime="application/json")

    with tabs[1]:
        st.subheader("Suggested Metrics")
        with st.spinner("Extracting metrics..."):
            if 'metrics' not in st.session_state or st.button("Refresh Metrics"):
                st.session_state['metrics'] = extractor.extract(parsed_logs)

        metrics = st.session_state['metrics']
        st.json(metrics)

    with tabs[2]:
        st.subheader("Prometheus Configuration")
        if 'prom_config' not in st.session_state or st.button("Generate Config"):
             with st.spinner("Generating Prometheus config..."):
                st.session_state['prom_config'] = prom_gen.generate(st.session_state.get('metrics', []))

        prom_config = st.session_state['prom_config']
        st.code(prom_config, language="yaml")
        st.download_button("Download YAML", data=prom_config, file_name="prometheus.yml", mime="text/yaml")

    with tabs[3]:
        st.subheader("Grafana Dashboard")
        if 'grafana_json' not in st.session_state or st.button("Generate Dashboard"):
             with st.spinner("Generating Grafana dashboard..."):
                st.session_state['grafana_json'] = graf_gen.generate(st.session_state.get('metrics', []), service_name)

        grafana_json = st.session_state['grafana_json']
        st.code(grafana_json, language="json")
        st.download_button("Download JSON", data=grafana_json, file_name="dashboard.json", mime="application/json")

    with tabs[4]:
        st.subheader("Metric Documentation")
        if 'docs' not in st.session_state or st.button("Generate Docs"):
             with st.spinner("Writing documentation..."):
                st.session_state['docs'] = doc_gen.generate(st.session_state.get('metrics', []))

        docs = st.session_state['docs']
        st.markdown(docs)
        st.download_button("Download Markdown", data=docs, file_name="metrics.md", mime="text/markdown")
