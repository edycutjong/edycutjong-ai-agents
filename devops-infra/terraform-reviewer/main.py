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
    merged = {}
    for hcl in hcl_list:
        for key, value in hcl.items():
            if key not in merged:
                merged[key] = []
            if isinstance(value, list):
                merged[key].extend(value)
            elif isinstance(value, dict):
                # Should be list of dicts usually, but handle just in case
                merged[key].append(value)
    return merged

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
        if st.button("🚀 Run Analysis", type="primary"):
            with st.spinner("Parsing and Analyzing Terraform configuration..."):
                # 1. Read and Parse TF Files
                tf_contents = []
                for uploaded_file in uploaded_tf_files:
                    string_data = uploaded_file.getvalue().decode("utf-8")
                    tf_contents.append(string_data)

                # Combine content implies parsing separately and merging
                # But reviewer.py expects a string for parsing.
                # However, concatenating strings is easiest for valid HCL if no conflict.
                # Let's try concatenating all content with newlines.
                combined_tf_content = "\n".join(tf_contents)

                # 2. Read State File
                state_content = None
                if uploaded_state_file:
                    try:
                        state_content = json.load(uploaded_state_file)
                    except Exception as e:
                        st.error(f"Error reading state file: {e}")

                # 3. Initialize Reviewer
                reviewer = TerraformReviewer(api_key=api_key)

                # 4. Run Review
                results = reviewer.run_review(combined_tf_content, state_content)

                if "error" in results:
                    st.error(results["error"])
                else:
                    display_results(results)

    elif not api_key:
        st.warning("Please provide an OpenAI API Key to proceed.")

def display_results(results: Dict[str, Any]):
    # Metrics
    security_count = len(results.get("security", []))
    cost_total = results.get("cost", {}).get("total_monthly_cost", 0.0)
    drift_status = results.get("drift", {}).get("status", "Not Checked")

    m1, m2, m3 = st.columns(3)
    m1.metric("Security Issues", security_count, delta_color="inverse")
    m2.metric("Est. Monthly Cost", f"${cost_total:.2f}")
    m3.metric("Drift Status", drift_status, delta_color="off" if drift_status == "Synced" else "inverse")

    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🤖 AI Report", "🛡️ Security", "💰 Cost Details", "📏 Rules & Best Practices", "🌫️ Drift"])

    with tab1:
        st.markdown(results.get("ai_report", "No report generated."))

    with tab2:
        findings = results.get("security", [])
        if findings:
            for f in findings:
                severity = f.get("severity", "LOW")
                color = "red" if severity == "CRITICAL" else "orange" if severity == "HIGH" else "blue"
                st.markdown(f"**[{severity}]** :{color}[{f['resource']}]")
                st.write(f"_{f['message']}_")
                st.divider()
        else:
            st.success("No security issues found!")

    with tab3:
        cost_data = results.get("cost", {})
        details = cost_data.get("details", {})
        if details:
            st.dataframe(
                [{"Resource": k, "Cost ($)": v} for k, v in details.items()],
                use_container_width=True
            )
        else:
            st.info("No costable resources found.")

    with tab4:
        rules = results.get("rules", [])
        if rules:
            for r in rules:
                st.warning(f"**{r['resource']}**: {r['message']}")
        else:
            st.success("All naming and static rules passed!")

    with tab5:
        drift = results.get("drift", {})
        if drift.get("status") == "No State Provided":
            st.info("Upload a .tfstate file to enable drift detection.")
        elif drift.get("status") == "Synced":
            st.success("Infrastructure is in sync with State.")
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                st.subheader("In Code, Not in State (To Create)")
                for item in drift.get("in_code_not_in_state", []):
                    st.write(f"- {item}")
            with col_b:
                st.subheader("In State, Not in Code (To Delete)")
                for item in drift.get("in_state_not_in_code", []):
                    st.write(f"- {item}")

if __name__ == "__main__":
    main()
