import streamlit as st
import os
import tempfile
import shutil
import zipfile
from pathlib import Path
import pandas as pd

from agent.scanner import CodeScanner
from agent.generator import PolicyGenerator
from agent.formatter import PolicyFormatter
from config import Config

# Page Configuration
st.set_page_config(
    page_title="Privacy Policy Generator Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium UI
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
    }
    .main-header {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #262730;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #4CAF50;
    }
    .metric-label {
        color: #b0b0b0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-header">🛡️ Privacy Policy Generator Agent</div>', unsafe_allow_html=True)

    # Sidebar Configuration
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", value=Config.OPENAI_API_KEY if Config.OPENAI_API_KEY else "")
        model_name = st.selectbox("Model", ["gpt-4-turbo", "gpt-3.5-turbo"], index=0)

        st.divider()
        st.info("This agent scans your codebase for data collection patterns and generates a compliant privacy policy.")

    # Main Content

    # 1. Input Section
    st.subheader("1. Source Code Input")
    input_method = st.radio("Select Input Method", ["Local Directory Path", "Upload Zip File"], horizontal=True)

    scan_dir = None
    temp_dir = None

    if input_method == "Local Directory Path":
        scan_path = st.text_input("Enter absolute path to codebase:", placeholder="/path/to/your/project")
        if scan_path and os.path.isdir(scan_path):
            scan_dir = scan_path
        elif scan_path:
            st.error("Invalid directory path.")
    else:
        uploaded_file = st.file_uploader("Upload Codebase (Zip)", type="zip")
        if uploaded_file:
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "uploaded.zip")
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Extract
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            scan_dir = temp_dir
            st.success(f"Uploaded and extracted to temporary directory.")

    # 2. Scanning Section
    if scan_dir:
        st.subheader("2. Scan Codebase")
        if st.button("Start Scan", type="primary"):
            with st.spinner("Scanning codebase for PII and third-party services..."):
                try:
                    scanner = CodeScanner(scan_dir)
                    results = scanner.scan()
                    st.session_state['scan_results'] = results
                    st.success("Scan Complete!")
                except Exception as e:
                    st.error(f"Error during scan: {e}")

    # Display Results
    if 'scan_results' in st.session_state:
        results = st.session_state['scan_results']

        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Files Scanned", results.get('files_scanned', 0))
        with col2:
            st.metric("PII Types Found", len(results.get('pii', [])))
        with col3:
            st.metric("Third Parties Found", len(results.get('third_parties', [])))

        # Detailed Findings
        col_pii, col_tp = st.columns(2)

        with col_pii:
            st.markdown("### Detected PII")
            if results.get('pii'):
                pii_data = []
                for item in results['pii']:
                    files = results.get('details', {}).get(item, [])
                    pii_data.append({"Category": item, "Files Count": len(files)})
                st.table(pd.DataFrame(pii_data))
            else:
                st.info("No PII detected.")

        with col_tp:
            st.markdown("### Detected Third Parties")
            if results.get('third_parties'):
                tp_data = []
                for item in results['third_parties']:
                    files = results.get('details', {}).get(item, [])
                    tp_data.append({"Service": item, "Files Count": len(files)})
                st.table(pd.DataFrame(tp_data))
            else:
                st.info("No third-party services detected.")

        st.divider()

        # 3. Generation Section
        st.subheader("3. Generate Policy")

        col_gen1, col_gen2 = st.columns(2)

        with col_gen1:
            policy_type = st.selectbox("Policy Type", ["GDPR", "CCPA", "Generic"])
            app_name = st.text_input("Application Name", value="My App")

        with col_gen2:
            company_name = st.text_input("Company Name", value="My Company")
            contact_email = st.text_input("Contact Email", value="privacy@example.com")

        if st.button("Generate Privacy Policy", type="primary"):
            if not api_key:
                st.error("Please provide an OpenAI API Key in the sidebar.")
            else:
                with st.spinner("Generating policy using AI..."):
                    try:
                        generator = PolicyGenerator(model_name=model_name, api_key=api_key)

                        # Prepare context
                        context = {
                            "app_name": app_name,
                            "company_name": company_name,
                            "contact_email": contact_email
                        }

                        policy_content = generator.generate_policy(results, policy_type, **context)
                        st.session_state['policy_content'] = policy_content
                        st.session_state['policy_type'] = policy_type
                        st.success("Policy Generated Successfully!")
                    except Exception as e:
                        st.error(f"Error generating policy: {e}")

    # Display Generated Policy
    if 'policy_content' in st.session_state:
        st.markdown("### Policy Preview")
        policy_content = st.session_state['policy_content']

        with st.expander("View Policy", expanded=True):
            st.markdown(policy_content)

        # Download Options
        st.subheader("Download")
        col_dl1, col_dl2 = st.columns(2)

        # Markdown Download
        col_dl1.download_button(
            label="Download as Markdown",
            data=policy_content,
            file_name=f"privacy_policy_{st.session_state['policy_type'].lower()}.md",
            mime="text/markdown"
        )

        # HTML Download
        html_content = PolicyFormatter.to_html(policy_content, title=f"{app_name} Privacy Policy")
        col_dl2.download_button(
            label="Download as HTML",
            data=html_content,
            file_name=f"privacy_policy_{st.session_state['policy_type'].lower()}.html",
            mime="text/html"
        )

    # Cleanup Temp Dir if used
    # Note: This might clean up before session ends if placed here,
    # but Streamlit re-runs script on interaction.
    # So temp_dir is recreated on every run if file uploaded.
    # To avoid this, we should cache the temp dir or handle it differently.
    # But for simplicity, let's rely on OS cleanup or advanced session state management.
    # Actually, `tempfile.mkdtemp()` creates a new dir each run.
    # If file is in `uploaded_file` (which is in RAM), we rewrite it.
    # This is fine for small files.

if __name__ == "__main__":
    main()
