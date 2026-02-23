import streamlit as st
import subprocess
import os
import signal
import json
import time
import pandas as pd
import sys

# Ensure agent module is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from agent.parser import OpenAPIParser
from agent.exporter import PostmanExporter

# Set page config
st.set_page_config(
    page_title="API Response Mocker",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium UI CSS
st.markdown("""
<style>
    /* Dark mode is default in Streamlit, just enhance it */
    .stApp {
        background-color: #0E1117;
    }
    .stSidebar {
        background-color: #262730;
    }
    h1, h2, h3 {
        color: #FAFAFA;
    }
    .stButton > button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #FF6B6B;
        border-color: #FF6B6B;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 API Response Mocker Agent")
st.markdown("""
Upload your OpenAPI/Swagger specification and instantly generate a mock server
with realistic data, latency simulation, and error scenarios.
""")

# Session State for Process Management
if "server_pid" not in st.session_state:
    st.session_state.server_pid = None
if "server_port" not in st.session_state:
    st.session_state.server_port = 8000
if "server_logs" not in st.session_state:
    st.session_state.server_logs = []

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Server Configuration")
    port = st.number_input("Port", min_value=1024, max_value=65535, value=8000)
    latency = st.slider("Latency (ms)", 0, 5000, 0, help="Simulate network delay")
    error_rate = st.slider("Error Rate (%)", 0, 100, 0, help="Randomly return 5xx errors")

# Main Content
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("1. Upload Spec")
    uploaded_file = st.file_uploader("Choose a YAML or JSON file", type=['yaml', 'json', 'yml'])

    start_btn = st.button("🚀 Start Server", disabled=st.session_state.server_pid is not None)
    stop_btn = st.button("🛑 Stop Server", disabled=st.session_state.server_pid is None)

    # Export Section
    if uploaded_file:
        try:
            # Check if we can parse it for export
            uploaded_file.seek(0)
            content = uploaded_file.read().decode("utf-8")
            parser = OpenAPIParser(content)
            exporter = PostmanExporter(parser)
            collection = exporter.export()

            st.download_button(
                "📥 Export Postman Collection",
                data=json.dumps(collection, indent=2),
                file_name="postman_collection.json",
                mime="application/json"
            )
            # Reset pointer for saving
            uploaded_file.seek(0)
        except Exception as e:
            st.warning(f"Could not prepare export: {e}")

    if uploaded_file and start_btn:
        # Save file temporarily
        spec_path = "temp_spec.yaml"
        with open(spec_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        log_file = "server_logs.json"
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
            except:
                pass

        # Prepare Environment
        env = os.environ.copy()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        env["PYTHONPATH"] = current_dir + ":" + env.get("PYTHONPATH", "")

        # Command
        cmd = [
            sys.executable,
            os.path.join(current_dir, "agent/run_server.py"),
            spec_path,
            str(port),
            str(latency),
            str(error_rate / 100.0),
            log_file
        ]

        try:
            # Start Process
            proc = subprocess.Popen(cmd, env=env)
            st.session_state.server_pid = proc.pid
            st.session_state.server_port = port
            st.success(f"Server started on port {port}")
            time.sleep(1) # Give it a moment to start
            st.rerun()
        except Exception as e:
            st.error(f"Failed to start server: {e}")

    if stop_btn:
        if st.session_state.server_pid:
            try:
                os.kill(st.session_state.server_pid, signal.SIGTERM)
                st.session_state.server_pid = None
                st.success("Server stopped.")
                st.rerun()
            except ProcessLookupError:
                st.session_state.server_pid = None
                st.warning("Server process already dead.")
                st.rerun()

with col2:
    st.subheader("2. Live Monitor")

    if st.session_state.server_pid:
        st.info(f"🟢 Server Running at http://localhost:{st.session_state.server_port}")
        st.markdown(f"[View Swagger UI](http://localhost:{st.session_state.server_port}/docs)")

        # Poll Logs
        log_file = "server_logs.json"
        if os.path.exists(log_file):
            try:
                with open(log_file, "r") as f:
                    logs = json.load(f)
                    if logs:
                        df = pd.DataFrame(logs)
                        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
                        df = df.sort_values("timestamp", ascending=False)
                        st.dataframe(
                            df[["timestamp", "method", "path", "status_code", "duration_ms"]],
                            use_container_width=True,
                            hide_index=True
                        )
                    else:
                        st.info("Waiting for requests...")
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        else:
            st.info("No logs generated yet.")

        # Add auto-refresh
        time.sleep(2)
        st.rerun()
    else:
        st.warning("Server is stopped.")
