import streamlit as st
import json
import os
import sys

# Ensure project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from agent.core import PermissionAuditorAgent

def main():
    st.set_page_config(page_title="Permission Auditor", page_icon="🛡️", layout="wide")

    st.title("🛡️ Permission Auditor")
    st.markdown("""
    **Analyze app permissions for privacy risks and generate justification documents.**
    Supports: Android Manifest (XML), iOS Info.plist, Chrome Extension Manifest (JSON), Web Package (JSON).
    """)

    # Sidebar for inputs
    with st.sidebar:
        st.header("Upload Manifest")
        uploaded_file = st.file_uploader("Upload App Manifest", type=["xml", "plist", "json"])

        st.header("Context")
        app_description = st.text_area("App Description", height=150, placeholder="Describe what your app does and why it needs permissions (e.g., 'A camera app that takes photos and saves them to gallery').")

        analyze_btn = st.button("Audit Permissions", type="primary")

    if uploaded_file and app_description:
        # Initialize Agent
        try:
            agent = PermissionAuditorAgent()
        except ValueError as e:
            st.error(f"Configuration Error: {str(e)}")
            return

        # Parse Manifest
        file_content = uploaded_file.read()
        permissions, platform = agent.parse_manifest_file(file_content, uploaded_file.name)

        if not permissions:
            st.warning("No permissions found or file type not recognized.")
            return

        # Display Parsed Data
        st.subheader(f"Parsed {platform.capitalize()} Permissions")
        st.write(f"Found {len(permissions)} permissions.")
        with st.expander("View Raw Permissions List"):
            st.json(permissions)

        if analyze_btn:
            with st.spinner("Analyzing permissions with AI..."):
                analysis_result = agent.analyze_permissions(permissions, app_description, platform)

            # Display Results
            st.divider()
            st.header("Analysis Report")

            # Risk Level Badge
            risk = analysis_result.get("risk_level", "Unknown")
            risk_color = "red" if risk in ["High", "Critical"] else "orange" if risk == "Medium" else "green"
            st.markdown(f"### Risk Level: :{risk_color}[{risk}]")

            st.markdown(f"**Summary:** {analysis_result.get('summary', 'No summary available.')}")

            # Detailed Table
            analysis_data = analysis_result.get("analysis", [])
            if analysis_data:
                st.dataframe(analysis_data, use_container_width=True)

            # Justification Generator
            st.divider()
            st.header("Justification Generator")
            if st.button("Generate Justification Document"):
                with st.spinner("Drafting justification..."):
                    doc = agent.generate_justification(permissions, app_description)
                st.markdown("### Generated Document")
                st.markdown(doc)
                st.download_button("Download Markdown", doc, file_name="permission_justification.md")

    elif analyze_btn and not uploaded_file:
        st.warning("Please upload a manifest file.")
    elif analyze_btn and not app_description:
        st.warning("Please provide an app description.")

if __name__ == "__main__":
    main()
