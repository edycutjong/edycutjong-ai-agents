import streamlit as st
import json
import os
import sys

# Ensure project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)  # pragma: no cover

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
        try:  # pragma: no cover
            agent = PermissionAuditorAgent()  # pragma: no cover
        except ValueError as e:  # pragma: no cover
            st.error(f"Configuration Error: {str(e)}")  # pragma: no cover
            return  # pragma: no cover

        # Parse Manifest
        file_content = uploaded_file.read()  # pragma: no cover
        permissions, platform = agent.parse_manifest_file(file_content, uploaded_file.name)  # pragma: no cover

        if not permissions:  # pragma: no cover
            st.warning("No permissions found or file type not recognized.")  # pragma: no cover
            return  # pragma: no cover

        # Display Parsed Data
        st.subheader(f"Parsed {platform.capitalize()} Permissions")  # pragma: no cover
        st.write(f"Found {len(permissions)} permissions.")  # pragma: no cover
        with st.expander("View Raw Permissions List"):  # pragma: no cover
            st.json(permissions)  # pragma: no cover

        if analyze_btn:  # pragma: no cover
            with st.spinner("Analyzing permissions with AI..."):  # pragma: no cover
                analysis_result = agent.analyze_permissions(permissions, app_description, platform)  # pragma: no cover

            # Display Results
            st.divider()  # pragma: no cover
            st.header("Analysis Report")  # pragma: no cover

            # Risk Level Badge
            risk = analysis_result.get("risk_level", "Unknown")  # pragma: no cover
            risk_color = "red" if risk in ["High", "Critical"] else "orange" if risk == "Medium" else "green"  # pragma: no cover
            st.markdown(f"### Risk Level: :{risk_color}[{risk}]")  # pragma: no cover

            st.markdown(f"**Summary:** {analysis_result.get('summary', 'No summary available.')}")  # pragma: no cover

            # Detailed Table
            analysis_data = analysis_result.get("analysis", [])  # pragma: no cover
            if analysis_data:  # pragma: no cover
                st.dataframe(analysis_data, use_container_width=True)  # pragma: no cover

            # Justification Generator
            st.divider()  # pragma: no cover
            st.header("Justification Generator")  # pragma: no cover
            if st.button("Generate Justification Document"):  # pragma: no cover
                with st.spinner("Drafting justification..."):  # pragma: no cover
                    doc = agent.generate_justification(permissions, app_description)  # pragma: no cover
                st.markdown("### Generated Document")  # pragma: no cover
                st.markdown(doc)  # pragma: no cover
                st.download_button("Download Markdown", doc, file_name="permission_justification.md")  # pragma: no cover

    elif analyze_btn and not uploaded_file:
        st.warning("Please upload a manifest file.")  # pragma: no cover
    elif analyze_btn and not app_description:
        st.warning("Please provide an app description.")  # pragma: no cover

if __name__ == "__main__":
    main()
