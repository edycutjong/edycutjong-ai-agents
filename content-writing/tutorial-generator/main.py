import streamlit as st
import os
import sys

# Add the current directory to sys.path to ensure modules are found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.generator import TutorialGenerator
from agent.utils import read_file_content
try:
    from config import OPENAI_API_KEY, MODEL_NAME
except ImportError:
    # Fallback if config isn't found or env vars not set (handled in UI)
    OPENAI_API_KEY = None
    MODEL_NAME = "gpt-4-turbo-preview"

st.set_page_config(page_title="Tutorial Generator Agent", page_icon="📚", layout="wide")

# Sidebar Configuration
st.sidebar.title("Configuration")

api_key = OPENAI_API_KEY
if not api_key:
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Allow overriding model in sidebar
model_name = st.sidebar.selectbox("Model", ["gpt-4-turbo-preview", "gpt-3.5-turbo"], index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This agent analyzes code libraries or documentation to generate "
    "step-by-step tutorials with runnable examples."
)

# Main Content
st.title("📚 Tutorial Generator Agent")
st.markdown("Generate premium technical tutorials from your library code or documentation.")

col1, col2 = st.columns([2, 1])

with col1:
    input_method = st.radio("Input Method", ["Paste Text", "Upload File"], horizontal=True)

    input_text = ""
    is_code = False

    if input_method == "Paste Text":
        input_type = st.selectbox("Input Type", ["Documentation", "Python Code"])
        is_code = (input_type == "Python Code")
        input_text = st.text_area("Library Content", height=300, placeholder="Paste your documentation or code here...")
    else:
        uploaded_file = st.file_uploader("Upload File", type=["py", "txt", "md"])
        if uploaded_file:
            input_text = read_file_content(uploaded_file)
            if uploaded_file.name.endswith(".py"):
                is_code = True
            st.success(f"Loaded {uploaded_file.name}")

with col2:
    st.subheader("Tutorial Settings")
    difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
    topic = st.text_input("Specific Topic/Goal", placeholder="e.g., Getting Started, Authentication")

    if not topic:
        topic = "Getting Started"

generate_btn = st.button("Generate Tutorial", type="primary", disabled=not input_text)

if generate_btn:
    if not api_key:
        st.error("Please provide an OpenAI API Key.")
    else:
        # Initialize generator
        generator = TutorialGenerator(api_key=api_key, model_name=model_name)

        full_tutorial_md = "# Tutorial: " + topic + "\n\n"

        # Container for results
        results_container = st.container()

        with st.status("Generating Tutorial...", expanded=True) as status:
            try:
                # Iterate through the generator stream
                for section_name, content in generator.generate_full_tutorial_stream(input_text, difficulty, topic, is_code):
                    st.write(f"**Generated {section_name}...**")

                    # Append to full markdown
                    # Analysis is usually internal context, but we can include it as a note or skip
                    if section_name == "Analysis":
                        # Don't add raw analysis to the tutorial output, but maybe show in UI?
                        # Let's show in UI expnader but not add to final MD download unless requested.
                        with results_container:
                            with st.expander("Analysis (Internal Context)", expanded=False):
                                st.text(content)
                        continue

                    section_md = f"\n## {section_name}\n\n{content}\n"
                    full_tutorial_md += section_md

                    # Display in UI
                    with results_container:
                        with st.expander(section_name, expanded=True):
                            st.markdown(content)

                status.update(label="Tutorial Generated Successfully!", state="complete", expanded=False)

                # Download Button
                st.download_button(
                    label="Download Tutorial as Markdown",
                    data=full_tutorial_md,
                    file_name="tutorial.md",
                    mime="text/markdown"
                )

            except Exception as e:
                status.update(label="An error occurred", state="error")
                st.error(f"Error generating tutorial: {str(e)}")
