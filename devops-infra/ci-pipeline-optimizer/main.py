import streamlit as st
import yaml
import json
import os
import sys

# Ensure the project root is in sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)  # pragma: no cover

from agent.ci_agent import CIAgent
from config import Config

st.set_page_config(
    page_title="CI Pipeline Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("🚀 CI Pipeline Optimizer")
    st.markdown("""
    Optimize your GitHub Actions or GitLab CI pipelines with AI.
    Identify bottlenecks, parallelize jobs, and improve caching strategies.
    """)

    # Sidebar for API Key if not in env
    with st.sidebar:
        st.header("Configuration")
        api_key = st.text_input("OpenAI API Key", type="password", value=Config.OPENAI_API_KEY if Config.OPENAI_API_KEY else "")
        if not api_key:
            st.warning("Please provide an OpenAI API Key to proceed.")  # pragma: no cover
            st.stop()  # pragma: no cover

        st.info("This tool analyzes your CI/CD configuration and suggests improvements.")

    agent = CIAgent(api_key=api_key)

    uploaded_file = st.file_uploader("Upload your CI/CD Config (YAML)", type=["yaml", "yml"])

    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")  # pragma: no cover

        col1, col2 = st.columns(2)  # pragma: no cover

        with col1:  # pragma: no cover
            st.subheader("Original Configuration")  # pragma: no cover
            st.code(content, language="yaml")  # pragma: no cover

        if st.button("Analyze & Optimize", type="primary"):  # pragma: no cover
            with st.spinner("Analyzing pipeline..."):  # pragma: no cover
                analysis_result = agent.analyze(content)  # pragma: no cover

            if "error" in analysis_result:  # pragma: no cover
                st.error(analysis_result["error"])  # pragma: no cover
            else:
                st.success("Analysis Complete!")  # pragma: no cover

                # Display Analysis
                with st.expander("📊 Analysis Report", expanded=True):  # pragma: no cover
                    st.markdown("### 🔍 Findings")  # pragma: no cover

                    if "bottlenecks" in analysis_result and analysis_result["bottlenecks"]:  # pragma: no cover
                        st.markdown("**🛑 Bottlenecks:**")  # pragma: no cover
                        for item in analysis_result["bottlenecks"]:  # pragma: no cover
                            st.markdown(f"- {item}")  # pragma: no cover

                    if "parallelization_opportunities" in analysis_result and analysis_result["parallelization_opportunities"]:  # pragma: no cover
                        st.markdown("**⚡ Parallelization Opportunities:**")  # pragma: no cover
                        for item in analysis_result["parallelization_opportunities"]:  # pragma: no cover
                            st.markdown(f"- {item}")  # pragma: no cover

                    if "caching_recommendations" in analysis_result and analysis_result["caching_recommendations"]:  # pragma: no cover
                        st.markdown("**📦 Caching Recommendations:**")  # pragma: no cover
                        for item in analysis_result["caching_recommendations"]:  # pragma: no cover
                            st.markdown(f"- {item}")  # pragma: no cover

                    if "other_improvements" in analysis_result and analysis_result["other_improvements"]:  # pragma: no cover
                        st.markdown("**💡 Other Improvements:**")  # pragma: no cover
                        for item in analysis_result["other_improvements"]:  # pragma: no cover
                            st.markdown(f"- {item}")  # pragma: no cover

                    if "estimated_time_savings" in analysis_result:  # pragma: no cover
                        st.metric("Estimated Time Savings", analysis_result["estimated_time_savings"])  # pragma: no cover

                # optimize
                with st.spinner("Generating optimized configuration..."):  # pragma: no cover
                    optimized_config = agent.optimize(content, analysis_result)  # pragma: no cover

                with col2:  # pragma: no cover
                    st.subheader("✨ Optimized Configuration")  # pragma: no cover
                    st.code(optimized_config, language="yaml")  # pragma: no cover
                    st.download_button(  # pragma: no cover
                        label="Download Optimized YAML",
                        data=optimized_config,
                        file_name="optimized-ci.yml",
                        mime="text/yaml"
                    )

if __name__ == "__main__":
    main()
