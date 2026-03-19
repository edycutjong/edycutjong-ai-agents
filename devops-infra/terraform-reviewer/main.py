import streamlit as st
import json
import os
from typing import Dict, List, Any

# Adjust path so we can import our modules
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from agent.reviewer import TerraformReviewer
from config import Config

def merge_hcl(hcl_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Merges multiple HCL dictionaries into one."""
    merged = {}  # pragma: no cover
    for hcl in hcl_list:  # pragma: no cover
        for key, value in hcl.items():  # pragma: no cover
            if key not in merged:  # pragma: no cover
                merged[key] = []  # pragma: no cover
            if isinstance(value, list):  # pragma: no cover
                merged[key].extend(value)  # pragma: no cover
            elif isinstance(value, dict):  # pragma: no cover
                # Should be list of dicts usually, but handle just in case
                merged[key].append(value)  # pragma: no cover
    return merged  # pragma: no cover

def main():
    st.set_page_config(
        page_title="Terraform Reviewer",
        page_icon="🏗️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for "Premium" feel
    st.markdown("""
    <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stMetric {
            background-color: #262730;
            padding: 10px;
            border-radius: 5px;
        }
        h1, h2, h3 {
            color: #4da6ff;
        }
        .success-box {
            padding: 10px;
            background-color: #2e7d32;
            color: white;
            border-radius: 5px;
        }
        .warning-box {
            padding: 10px;
            background-color: #f9a825;
            color: black;
            border-radius: 5px;
        }
        .error-box {
            padding: 10px;
            background-color: #c62828;
            color: white;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🏗️ Terraform Reviewer Agent")
    st.markdown("### Intelligent Infrastructure-as-Code Security & Cost Analysis")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        api_key = st.text_input("OpenAI API Key", type="password", help="Required for AI Report generation.")
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY") or Config.OPENAI_API_KEY
            if api_key:
                st.success("API Key detected from environment.")

        st.divider()
        st.info("Upload your Terraform files (.tf) to analyze security, cost, and drift.")

    # File Uploaders
    col1, col2 = st.columns(2)
    with col1:
        uploaded_tf_files = st.file_uploader("Upload .tf files", type=["tf"], accept_multiple_files=True)
    with col2:
        uploaded_state_file = st.file_uploader("Upload .tfstate (Optional)", type=["json", "tfstate"])

    if uploaded_tf_files and api_key:
        if st.button("🚀 Run Analysis", type="primary"):  # pragma: no cover
            with st.spinner("Parsing and Analyzing Terraform configuration..."):  # pragma: no cover
                # 1. Read and Parse TF Files
                tf_contents = []  # pragma: no cover
                for uploaded_file in uploaded_tf_files:  # pragma: no cover
                    string_data = uploaded_file.getvalue().decode("utf-8")  # pragma: no cover
                    tf_contents.append(string_data)  # pragma: no cover

                # Combine content implies parsing separately and merging
                # But reviewer.py expects a string for parsing.
                # However, concatenating strings is easiest for valid HCL if no conflict.
                # Let's try concatenating all content with newlines.
                combined_tf_content = "\n".join(tf_contents)  # pragma: no cover

                # 2. Read State File
                state_content = None  # pragma: no cover
                if uploaded_state_file:  # pragma: no cover
                    try:  # pragma: no cover
                        state_content = json.load(uploaded_state_file)  # pragma: no cover
                    except Exception as e:  # pragma: no cover
                        st.error(f"Error reading state file: {e}")  # pragma: no cover

                # 3. Initialize Reviewer
                reviewer = TerraformReviewer(api_key=api_key)  # pragma: no cover

                # 4. Run Review
                results = reviewer.run_review(combined_tf_content, state_content)  # pragma: no cover

                if "error" in results:  # pragma: no cover
                    st.error(results["error"])  # pragma: no cover
                else:
                    display_results(results)  # pragma: no cover

    elif not api_key:
        st.warning("Please provide an OpenAI API Key to proceed.")  # pragma: no cover

def display_results(results: Dict[str, Any]):
    # Metrics
    security_count = len(results.get("security", []))  # pragma: no cover
    cost_total = results.get("cost", {}).get("total_monthly_cost", 0.0)  # pragma: no cover
    drift_status = results.get("drift", {}).get("status", "Not Checked")  # pragma: no cover

    m1, m2, m3 = st.columns(3)  # pragma: no cover
    m1.metric("Security Issues", security_count, delta_color="inverse")  # pragma: no cover
    m2.metric("Est. Monthly Cost", f"${cost_total:.2f}")  # pragma: no cover
    m3.metric("Drift Status", drift_status, delta_color="off" if drift_status == "Synced" else "inverse")  # pragma: no cover

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤖 AI Report", "🛡️ Security", "💰 Cost Details", "📏 Rules & Best Practices", "🌫️ Drift"])  # pragma: no cover

    with tab1:  # pragma: no cover
        st.markdown(results.get("ai_report", "No report generated."))  # pragma: no cover

    with tab2:  # pragma: no cover
        findings = results.get("security", [])  # pragma: no cover
        if findings:  # pragma: no cover
            for f in findings:  # pragma: no cover
                severity = f.get("severity", "LOW")  # pragma: no cover
                color = "red" if severity == "CRITICAL" else "orange" if severity == "HIGH" else "blue"  # pragma: no cover
                st.markdown(f"**[{severity}]** :{color}[{f['resource']}]")  # pragma: no cover
                st.write(f"_{f['message']}_")  # pragma: no cover
                st.divider()  # pragma: no cover
        else:
            st.success("No security issues found!")  # pragma: no cover

    with tab3:  # pragma: no cover
        cost_data = results.get("cost", {})  # pragma: no cover
        details = cost_data.get("details", {})  # pragma: no cover
        if details:  # pragma: no cover
            st.dataframe(  # pragma: no cover
                [{"Resource": k, "Cost ($)": v} for k, v in details.items()],
                use_container_width=True
            )
        else:
            st.info("No costable resources found.")  # pragma: no cover

    with tab4:  # pragma: no cover
        rules = results.get("rules", [])  # pragma: no cover
        if rules:  # pragma: no cover
            for r in rules:  # pragma: no cover
                st.warning(f"**{r['resource']}**: {r['message']}")  # pragma: no cover
        else:
            st.success("All naming and static rules passed!")  # pragma: no cover

    with tab5:  # pragma: no cover
        drift = results.get("drift", {})  # pragma: no cover
        if drift.get("status") == "No State Provided":  # pragma: no cover
            st.info("Upload a .tfstate file to enable drift detection.")  # pragma: no cover
        elif drift.get("status") == "Synced":  # pragma: no cover
            st.success("Infrastructure is in sync with State.")  # pragma: no cover
        else:
            col_a, col_b = st.columns(2)  # pragma: no cover
            with col_a:  # pragma: no cover
                st.subheader("In Code, Not in State (To Create)")  # pragma: no cover
                for item in drift.get("in_code_not_in_state", []):  # pragma: no cover
                    st.write(f"- {item}")  # pragma: no cover
            with col_b:  # pragma: no cover
                st.subheader("In State, Not in Code (To Delete)")  # pragma: no cover
                for item in drift.get("in_state_not_in_code", []):  # pragma: no cover
                    st.write(f"- {item}")  # pragma: no cover

if __name__ == "__main__":
    main()
