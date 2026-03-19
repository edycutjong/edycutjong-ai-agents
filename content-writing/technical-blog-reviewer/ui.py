import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover
import json  # pragma: no cover
import re  # pragma: no cover
from typing import Dict, Any  # pragma: no cover

# Ensure we can import modules from local package
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

from agent.core import TechnicalBlogReviewer  # pragma: no cover
from config import DEFAULT_MODEL, APP_NAME, APP_DESCRIPTION  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title=APP_NAME,
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

def extract_scores(summary: str) -> Dict[str, int]:  # pragma: no cover
    """
    Attempts to extract scores from the summary text using regex.
    """
    scores = {}  # pragma: no cover
    patterns = {  # pragma: no cover
        "Technical Accuracy": r"Technical Accuracy.*?:?\s*(\d+)/?1?0?0?",
        "Code Quality": r"Code Quality.*?:?\s*(\d+)/?1?0?0?",
        "Readability": r"Readability.*?:?\s*(\d+)/?1?0?0?",
        "Overall Score": r"Overall Score.*?:?\s*(\d+)/?1?0?0?"
    }

    for category, pattern in patterns.items():  # pragma: no cover
        match = re.search(pattern, summary, re.IGNORECASE)  # pragma: no cover
        if match:  # pragma: no cover
            try:  # pragma: no cover
                scores[category] = int(match.group(1))  # pragma: no cover
            except ValueError:  # pragma: no cover
                pass  # pragma: no cover
    return scores  # pragma: no cover

def main():  # pragma: no cover
    # Sidebar
    with st.sidebar:  # pragma: no cover
        st.title(f"🤖 {APP_NAME}")  # pragma: no cover
        st.markdown(APP_DESCRIPTION)  # pragma: no cover

        st.divider()  # pragma: no cover

        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))  # pragma: no cover
        model = st.selectbox("Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], index=0)  # pragma: no cover

        st.divider()  # pragma: no cover
        st.info("Ensure you have a valid OpenAI API Key to proceed.")  # pragma: no cover

    # Main Content
    st.title("📝 Technical Blog Reviewer")  # pragma: no cover
    st.markdown("Automated AI review for technical content.")  # pragma: no cover

    # Input Section
    input_method = st.radio("Input Method", ["Text", "URL", "File Upload"], horizontal=True)  # pragma: no cover

    content = ""  # pragma: no cover
    is_url = False  # pragma: no cover

    if input_method == "Text":  # pragma: no cover
        content = st.text_area("Paste your blog post content here:", height=300)  # pragma: no cover
    elif input_method == "URL":  # pragma: no cover
        content = st.text_input("Enter the blog post URL:")  # pragma: no cover
        is_url = True  # pragma: no cover
    elif input_method == "File Upload":  # pragma: no cover
        uploaded_file = st.file_uploader("Upload a Markdown or Text file", type=["md", "txt"])  # pragma: no cover
        if uploaded_file:  # pragma: no cover
            content = uploaded_file.read().decode("utf-8")  # pragma: no cover

    # Review Button
    if st.button("🚀 Run Review", type="primary", disabled=not content or not api_key):  # pragma: no cover
        if not api_key:  # pragma: no cover
            st.error("Please provide an OpenAI API Key.")  # pragma: no cover
            return  # pragma: no cover

        with st.spinner("Analyzing content... (This may take a minute)"):  # pragma: no cover
            try:  # pragma: no cover
                # Initialize Reviewer
                reviewer = TechnicalBlogReviewer(api_key=api_key, model=model)  # pragma: no cover

                # Run Review
                report = reviewer.review(content, is_url=is_url)  # pragma: no cover

                if "error" in report:  # pragma: no cover
                    st.error(f"Error: {report['error']}")  # pragma: no cover
                else:
                    st.success("Review Complete!")  # pragma: no cover

                    # Store results in session state to persist
                    st.session_state.report = report  # pragma: no cover

            except Exception as e:  # pragma: no cover
                st.error(f"An error occurred: {str(e)}")  # pragma: no cover

    # Display Results
    if "report" in st.session_state:  # pragma: no cover
        report = st.session_state.report  # pragma: no cover
        summary = report["summary"]  # pragma: no cover
        scores = extract_scores(summary)  # pragma: no cover

        st.divider()  # pragma: no cover

        # Metrics Dashboard
        col1, col2, col3, col4 = st.columns(4)  # pragma: no cover
        with col1:  # pragma: no cover
            st.metric("Technical Accuracy", f"{scores.get('Technical Accuracy', 'N/A')}")  # pragma: no cover
        with col2:  # pragma: no cover
            st.metric("Code Quality", f"{scores.get('Code Quality', 'N/A')}")  # pragma: no cover
        with col3:  # pragma: no cover
            st.metric("Readability", f"{scores.get('Readability', 'N/A')}")  # pragma: no cover
        with col4:  # pragma: no cover
            st.metric("Overall Score", f"{scores.get('Overall Score', 'N/A')}")  # pragma: no cover

        # Tabs for Detailed Feedback
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Summary", "🛠️ Technical Accuracy", "💻 Code Validation", "📖 Readability"])  # pragma: no cover

        with tab1:  # pragma: no cover
            st.markdown(summary)  # pragma: no cover

        with tab2:  # pragma: no cover
            st.markdown(report["technical_accuracy"])  # pragma: no cover

        with tab3:  # pragma: no cover
            st.markdown(report["code_validation"])  # pragma: no cover

        with tab4:  # pragma: no cover
            st.markdown(report["readability"])  # pragma: no cover

        st.divider()  # pragma: no cover

        # Download Button
        report_json = json.dumps(report, indent=2)  # pragma: no cover
        st.download_button(  # pragma: no cover
            label="📥 Download Report (JSON)",
            data=report_json,
            file_name="review_report.json",
            mime="application/json"
        )

if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
