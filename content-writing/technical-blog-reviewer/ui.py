import streamlit as st
import os
import sys
import json
import re
from typing import Dict, Any

# Ensure we can import modules from local package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.core import TechnicalBlogReviewer
from config import DEFAULT_MODEL, APP_NAME, APP_DESCRIPTION

st.set_page_config(
    page_title=APP_NAME,
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

def extract_scores(summary: str) -> Dict[str, int]:
    """
    Attempts to extract scores from the summary text using regex.
    """
    scores = {}
    patterns = {
        "Technical Accuracy": r"Technical Accuracy.*?:?\s*(\d+)/?1?0?0?",
        "Code Quality": r"Code Quality.*?:?\s*(\d+)/?1?0?0?",
        "Readability": r"Readability.*?:?\s*(\d+)/?1?0?0?",
        "Overall Score": r"Overall Score.*?:?\s*(\d+)/?1?0?0?"
    }

    for category, pattern in patterns.items():
        match = re.search(pattern, summary, re.IGNORECASE)
        if match:
            try:
                scores[category] = int(match.group(1))
            except ValueError:
                pass
    return scores

def main():
    # Sidebar
    with st.sidebar:
        st.title(f"🤖 {APP_NAME}")
        st.markdown(APP_DESCRIPTION)

        st.divider()

        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
        model = st.selectbox("Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)

        st.divider()
        st.info("Ensure you have a valid OpenAI API Key to proceed.")

    # Main Content
    st.title("📝 Technical Blog Reviewer")
    st.markdown("Automated AI review for technical content.")

    # Input Section
    input_method = st.radio("Input Method", ["Text", "URL", "File Upload"], horizontal=True)

    content = ""
    is_url = False

    if input_method == "Text":
        content = st.text_area("Paste your blog post content here:", height=300)
    elif input_method == "URL":
        content = st.text_input("Enter the blog post URL:")
        is_url = True
    elif input_method == "File Upload":
        uploaded_file = st.file_uploader("Upload a Markdown or Text file", type=["md", "txt"])
        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")

    # Review Button
    if st.button("🚀 Run Review", type="primary", disabled=not content or not api_key):
        if not api_key:
            st.error("Please provide an OpenAI API Key.")
            return

        with st.spinner("Analyzing content... (This may take a minute)"):
            try:
                # Initialize Reviewer
                reviewer = TechnicalBlogReviewer(api_key=api_key, model=model)

                # Run Review
                report = reviewer.review(content, is_url=is_url)

                if "error" in report:
                    st.error(f"Error: {report['error']}")
                else:
                    st.success("Review Complete!")

                    # Store results in session state to persist
                    st.session_state.report = report

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Display Results
    if "report" in st.session_state:
        report = st.session_state.report
        summary = report["summary"]
        scores = extract_scores(summary)

        st.divider()

        # Metrics Dashboard
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Technical Accuracy", f"{scores.get('Technical Accuracy', 'N/A')}")
        with col2:
            st.metric("Code Quality", f"{scores.get('Code Quality', 'N/A')}")
        with col3:
            st.metric("Readability", f"{scores.get('Readability', 'N/A')}")
        with col4:
            st.metric("Overall Score", f"{scores.get('Overall Score', 'N/A')}")

        # Tabs for Detailed Feedback
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "🛠️ Technical Accuracy", "💻 Code Validation", "📖 Readability"])

        with tab1:
            st.markdown(summary)

        with tab2:
            st.markdown(report["technical_accuracy"])

        with tab3:
            st.markdown(report["code_validation"])

        with tab4:
            st.markdown(report["readability"])

        st.divider()

        # Download Button
        report_json = json.dumps(report, indent=2)
        st.download_button(
            label="📥 Download Report (JSON)",
            data=report_json,
            file_name="review_report.json",
            mime="application/json"
        )

if __name__ == "__main__":
    main()
