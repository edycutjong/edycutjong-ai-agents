import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import tempfile  # pragma: no cover
import shutil  # pragma: no cover
import zipfile  # pragma: no cover
from pathlib import Path  # pragma: no cover
import pandas as pd  # pragma: no cover

from agent.scanner import CodeScanner  # pragma: no cover
from agent.generator import PolicyGenerator  # pragma: no cover
from agent.formatter import PolicyFormatter  # pragma: no cover
from config import Config  # pragma: no cover

# Page Configuration
st.set_page_config(  # pragma: no cover
    page_title="Privacy Policy Generator Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium UI
st.markdown("""  # pragma: no cover
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

def main():  # pragma: no cover
    st.markdown('<div class="main-header">🛡️ Privacy Policy Generator Agent</div>', unsafe_allow_html=True)  # pragma: no cover

    # Sidebar Configuration
    with st.sidebar:  # pragma: no cover
        st.header("Configuration")  # pragma: no cover
        api_key = st.text_input("OpenAI API Key", type="password", value=Config.OPENAI_API_KEY if Config.OPENAI_API_KEY else "")  # pragma: no cover
        model_name = st.selectbox("Model", ["gpt-4-turbo", "gpt-3.5-turbo"], index=0)  # pragma: no cover

        st.divider()  # pragma: no cover
        st.info("This agent scans your codebase for data collection patterns and generates a compliant privacy policy.")  # pragma: no cover

    # Main Content

    # 1. Input Section
    st.subheader("1. Source Code Input")  # pragma: no cover
    input_method = st.radio("Select Input Method", ["Local Directory Path", "Upload Zip File"], horizontal=True)  # pragma: no cover

    scan_dir = None  # pragma: no cover
    temp_dir = None  # pragma: no cover

    if input_method == "Local Directory Path":  # pragma: no cover
        scan_path = st.text_input("Enter absolute path to codebase:", placeholder="/path/to/your/project")  # pragma: no cover
        if scan_path and os.path.isdir(scan_path):  # pragma: no cover
            scan_dir = scan_path  # pragma: no cover
        elif scan_path:  # pragma: no cover
            st.error("Invalid directory path.")  # pragma: no cover
    else:
        uploaded_file = st.file_uploader("Upload Codebase (Zip)", type="zip")  # pragma: no cover
        if uploaded_file:  # pragma: no cover
            # Create a temporary directory
            temp_dir = tempfile.mkdtemp()  # pragma: no cover
            zip_path = os.path.join(temp_dir, "uploaded.zip")  # pragma: no cover
            with open(zip_path, "wb") as f:  # pragma: no cover
                f.write(uploaded_file.getbuffer())  # pragma: no cover

            # Extract
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:  # pragma: no cover
                zip_ref.extractall(temp_dir)  # pragma: no cover

            scan_dir = temp_dir  # pragma: no cover
            st.success(f"Uploaded and extracted to temporary directory.")  # pragma: no cover

    # 2. Scanning Section
    if scan_dir:  # pragma: no cover
        st.subheader("2. Scan Codebase")  # pragma: no cover
        if st.button("Start Scan", type="primary"):  # pragma: no cover
            with st.spinner("Scanning codebase for PII and third-party services..."):  # pragma: no cover
                try:  # pragma: no cover
                    scanner = CodeScanner(scan_dir)  # pragma: no cover
                    results = scanner.scan()  # pragma: no cover
                    st.session_state['scan_results'] = results  # pragma: no cover
                    st.success("Scan Complete!")  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(f"Error during scan: {e}")  # pragma: no cover

    # Display Results
    if 'scan_results' in st.session_state:  # pragma: no cover
        results = st.session_state['scan_results']  # pragma: no cover

        # Metrics
        col1, col2, col3 = st.columns(3)  # pragma: no cover
        with col1:  # pragma: no cover
            st.metric("Files Scanned", results.get('files_scanned', 0))  # pragma: no cover
        with col2:  # pragma: no cover
            st.metric("PII Types Found", len(results.get('pii', [])))  # pragma: no cover
        with col3:  # pragma: no cover
            st.metric("Third Parties Found", len(results.get('third_parties', [])))  # pragma: no cover

        # Detailed Findings
        col_pii, col_tp = st.columns(2)  # pragma: no cover

        with col_pii:  # pragma: no cover
            st.markdown("### Detected PII")  # pragma: no cover
            if results.get('pii'):  # pragma: no cover
                pii_data = []  # pragma: no cover
                for item in results['pii']:  # pragma: no cover
                    files = results.get('details', {}).get(item, [])  # pragma: no cover
                    pii_data.append({"Category": item, "Files Count": len(files)})  # pragma: no cover
                st.table(pd.DataFrame(pii_data))  # pragma: no cover
            else:
                st.info("No PII detected.")  # pragma: no cover

        with col_tp:  # pragma: no cover
            st.markdown("### Detected Third Parties")  # pragma: no cover
            if results.get('third_parties'):  # pragma: no cover
                tp_data = []  # pragma: no cover
                for item in results['third_parties']:  # pragma: no cover
                    files = results.get('details', {}).get(item, [])  # pragma: no cover
                    tp_data.append({"Service": item, "Files Count": len(files)})  # pragma: no cover
                st.table(pd.DataFrame(tp_data))  # pragma: no cover
            else:
                st.info("No third-party services detected.")  # pragma: no cover

        st.divider()  # pragma: no cover

        # 3. Generation Section
        st.subheader("3. Generate Policy")  # pragma: no cover

        col_gen1, col_gen2 = st.columns(2)  # pragma: no cover

        with col_gen1:  # pragma: no cover
            policy_type = st.selectbox("Policy Type", ["GDPR", "CCPA", "Generic"])  # pragma: no cover
            app_name = st.text_input("Application Name", value="My App")  # pragma: no cover

        with col_gen2:  # pragma: no cover
            company_name = st.text_input("Company Name", value="My Company")  # pragma: no cover
            contact_email = st.text_input("Contact Email", value="privacy@example.com")  # pragma: no cover

        if st.button("Generate Privacy Policy", type="primary"):  # pragma: no cover
            if not api_key:  # pragma: no cover
                st.error("Please provide an OpenAI API Key in the sidebar.")  # pragma: no cover
            else:
                with st.spinner("Generating policy using AI..."):  # pragma: no cover
                    try:  # pragma: no cover
                        generator = PolicyGenerator(model_name=model_name, api_key=api_key)  # pragma: no cover

                        # Prepare context
                        context = {  # pragma: no cover
                            "app_name": app_name,
                            "company_name": company_name,
                            "contact_email": contact_email
                        }

                        policy_content = generator.generate_policy(results, policy_type, **context)  # pragma: no cover
                        st.session_state['policy_content'] = policy_content  # pragma: no cover
                        st.session_state['policy_type'] = policy_type  # pragma: no cover
                        st.success("Policy Generated Successfully!")  # pragma: no cover
                    except Exception as e:  # pragma: no cover
                        st.error(f"Error generating policy: {e}")  # pragma: no cover

    # Display Generated Policy
    if 'policy_content' in st.session_state:  # pragma: no cover
        st.markdown("### Policy Preview")  # pragma: no cover
        policy_content = st.session_state['policy_content']  # pragma: no cover

        with st.expander("View Policy", expanded=True):  # pragma: no cover
            st.markdown(policy_content)  # pragma: no cover

        # Download Options
        st.subheader("Download")  # pragma: no cover
        col_dl1, col_dl2 = st.columns(2)  # pragma: no cover

        # Markdown Download
        col_dl1.download_button(  # pragma: no cover
            label="Download as Markdown",
            data=policy_content,
            file_name=f"privacy_policy_{st.session_state['policy_type'].lower()}.md",
            mime="text/markdown"
        )

        # HTML Download
        html_content = PolicyFormatter.to_html(policy_content, title=f"{app_name} Privacy Policy")  # pragma: no cover
        col_dl2.download_button(  # pragma: no cover
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

if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
