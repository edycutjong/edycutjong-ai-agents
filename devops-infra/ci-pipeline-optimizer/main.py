import streamlit as st
import yaml
import json
import os
import sys

# Ensure the project root is in sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

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
            st.warning("Please provide an OpenAI API Key to proceed.")
            st.stop()

        st.info("This tool analyzes your CI/CD configuration and suggests improvements.")

    agent = CIAgent(api_key=api_key)

    uploaded_file = st.file_uploader("Upload your CI/CD Config (YAML)", type=["yaml", "yml"])

    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Configuration")
            st.code(content, language="yaml")

        if st.button("Analyze & Optimize", type="primary"):
            with st.spinner("Analyzing pipeline..."):
                analysis_result = agent.analyze(content)

            if "error" in analysis_result:
                st.error(analysis_result["error"])
            else:
                st.success("Analysis Complete!")

                # Display Analysis
                with st.expander("📊 Analysis Report", expanded=True):
                    st.markdown("### 🔍 Findings")

                    if "bottlenecks" in analysis_result and analysis_result["bottlenecks"]:
                        st.markdown("**🛑 Bottlenecks:**")
                        for item in analysis_result["bottlenecks"]:
                            st.markdown(f"- {item}")

                    if "parallelization_opportunities" in analysis_result and analysis_result["parallelization_opportunities"]:
                        st.markdown("**⚡ Parallelization Opportunities:**")
                        for item in analysis_result["parallelization_opportunities"]:
                            st.markdown(f"- {item}")

                    if "caching_recommendations" in analysis_result and analysis_result["caching_recommendations"]:
                        st.markdown("**📦 Caching Recommendations:**")
                        for item in analysis_result["caching_recommendations"]:
                            st.markdown(f"- {item}")

                    if "other_improvements" in analysis_result and analysis_result["other_improvements"]:
                        st.markdown("**💡 Other Improvements:**")
                        for item in analysis_result["other_improvements"]:
                            st.markdown(f"- {item}")

                    if "estimated_time_savings" in analysis_result:
                        st.metric("Estimated Time Savings", analysis_result["estimated_time_savings"])

                # optimize
                with st.spinner("Generating optimized configuration..."):
                    optimized_config = agent.optimize(content, analysis_result)

                with col2:
                    st.subheader("✨ Optimized Configuration")
                    st.code(optimized_config, language="yaml")
                    st.download_button(
                        label="Download Optimized YAML",
                        data=optimized_config,
                        file_name="optimized-ci.yml",
                        mime="text/yaml"
                    )

if __name__ == "__main__":
    main()
