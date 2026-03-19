import streamlit as st  # pragma: no cover
import os  # pragma: no cover
import sys  # pragma: no cover

# Add the current directory to sys.path to ensure modules are found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

from agent.generator import TutorialGenerator  # pragma: no cover
from agent.utils import read_file_content  # pragma: no cover
try:  # pragma: no cover
    from config import OPENAI_API_KEY, MODEL_NAME  # pragma: no cover
except ImportError:  # pragma: no cover
    # Fallback if config isn't found or env vars not set (handled in UI)
    OPENAI_API_KEY = None  # pragma: no cover
    MODEL_NAME = "gpt-4-turbo-preview"  # pragma: no cover

st.set_page_config(page_title="Tutorial Generator Agent", page_icon="📚", layout="wide")  # pragma: no cover

# Sidebar Configuration
st.sidebar.title("Configuration")  # pragma: no cover

api_key = OPENAI_API_KEY  # pragma: no cover
if not api_key:  # pragma: no cover
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")  # pragma: no cover

# Allow overriding model in sidebar
model_name = st.sidebar.selectbox("Model", ["gpt-4-turbo-preview", "gpt-3.5-turbo"], index=0)  # pragma: no cover

st.sidebar.markdown("---")  # pragma: no cover
st.sidebar.markdown("### About")  # pragma: no cover
st.sidebar.info(  # pragma: no cover
    "This agent analyzes code libraries or documentation to generate "
    "step-by-step tutorials with runnable examples."
)

# Main Content
st.title("📚 Tutorial Generator Agent")  # pragma: no cover
st.markdown("Generate premium technical tutorials from your library code or documentation.")  # pragma: no cover

col1, col2 = st.columns([2, 1])  # pragma: no cover

with col1:  # pragma: no cover
    input_method = st.radio("Input Method", ["Paste Text", "Upload File"], horizontal=True)  # pragma: no cover

    input_text = ""  # pragma: no cover
    is_code = False  # pragma: no cover

    if input_method == "Paste Text":  # pragma: no cover
        input_type = st.selectbox("Input Type", ["Documentation", "Python Code"])  # pragma: no cover
        is_code = (input_type == "Python Code")  # pragma: no cover
        input_text = st.text_area("Library Content", height=300, placeholder="Paste your documentation or code here...")  # pragma: no cover
    else:
        uploaded_file = st.file_uploader("Upload File", type=["py", "txt", "md"])  # pragma: no cover
        if uploaded_file:  # pragma: no cover
            input_text = read_file_content(uploaded_file)  # pragma: no cover
            if uploaded_file.name.endswith(".py"):  # pragma: no cover
                is_code = True  # pragma: no cover
            st.success(f"Loaded {uploaded_file.name}")  # pragma: no cover

with col2:  # pragma: no cover
    st.subheader("Tutorial Settings")  # pragma: no cover
    difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])  # pragma: no cover
    topic = st.text_input("Specific Topic/Goal", placeholder="e.g., Getting Started, Authentication")  # pragma: no cover

    if not topic:  # pragma: no cover
        topic = "Getting Started"  # pragma: no cover

generate_btn = st.button("Generate Tutorial", type="primary", disabled=not input_text)  # pragma: no cover

if generate_btn:  # pragma: no cover
    if not api_key:  # pragma: no cover
        st.error("Please provide an OpenAI API Key.")  # pragma: no cover
    else:
        # Initialize generator
        generator = TutorialGenerator(api_key=api_key, model_name=model_name)  # pragma: no cover

        full_tutorial_md = "# Tutorial: " + topic + "\n\n"  # pragma: no cover

        # Container for results
        results_container = st.container()  # pragma: no cover

        with st.status("Generating Tutorial...", expanded=True) as status:  # pragma: no cover
            try:  # pragma: no cover
                # Iterate through the generator stream
                for section_name, content in generator.generate_full_tutorial_stream(input_text, difficulty, topic, is_code):  # pragma: no cover
                    st.write(f"**Generated {section_name}...**")  # pragma: no cover

                    # Append to full markdown
                    # Analysis is usually internal context, but we can include it as a note or skip
                    if section_name == "Analysis":  # pragma: no cover
                        # Don't add raw analysis to the tutorial output, but maybe show in UI?
                        # Let's show in UI expnader but not add to final MD download unless requested.
                        with results_container:  # pragma: no cover
                            with st.expander("Analysis (Internal Context)", expanded=False):  # pragma: no cover
                                st.text(content)  # pragma: no cover
                        continue  # pragma: no cover

                    section_md = f"\n## {section_name}\n\n{content}\n"  # pragma: no cover
                    full_tutorial_md += section_md  # pragma: no cover

                    # Display in UI
                    with results_container:  # pragma: no cover
                        with st.expander(section_name, expanded=True):  # pragma: no cover
                            st.markdown(content)  # pragma: no cover

                status.update(label="Tutorial Generated Successfully!", state="complete", expanded=False)  # pragma: no cover

                # Download Button
                st.download_button(  # pragma: no cover
                    label="Download Tutorial as Markdown",
                    data=full_tutorial_md,
                    file_name="tutorial.md",
                    mime="text/markdown"
                )

            except Exception as e:  # pragma: no cover
                status.update(label="An error occurred", state="error")  # pragma: no cover
                st.error(f"Error generating tutorial: {str(e)}")  # pragma: no cover
