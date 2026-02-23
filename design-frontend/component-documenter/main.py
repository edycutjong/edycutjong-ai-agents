import streamlit as st
import os
import sys

# Ensure proper path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from agent.parser import parse_uploaded_file, get_language_from_extension
from agent.generator import ComponentDocumenter
from config import Config

st.set_page_config(
    page_title="Component Documenter Agent",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
<style>
    .reportview-container {
        background: #0E1117;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #FFFFFF;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
    }
    .stTextArea textarea {
        font-family: 'Fira Code', monospace;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("📝 Component Documenter")
    st.markdown("### Generate premium Storybook-style documentation for your UI components.")

    # Sidebar
    with st.sidebar:
        st.header("Configuration")

        api_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))

        st.info(
            """
            **Supported Frameworks:**
            - React (.jsx, .tsx)
            - Vue (.vue)
            - Svelte (.svelte)
            - Angular (.html templates)
            """
        )

        st.markdown("---")
        st.markdown("Built by **Jules**")

    # Main Content
    uploaded_files = st.file_uploader(
        "Upload Component Files",
        type=['js', 'jsx', 'ts', 'tsx', 'vue', 'svelte', 'html'],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            content, language = parse_uploaded_file(uploaded_file)

            with st.expander(f"File: {uploaded_file.name} ({language})", expanded=True):
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.subheader("Source Code")
                    st.code(content, language=language if language != 'angular-template' else 'html')

                with col2:
                    st.subheader("Documentation")
                    generate_key = f"gen_{uploaded_file.name}"

                    if st.button(f"Generate Docs for {uploaded_file.name}", key=generate_key):
                        if not api_key:
                            st.error("Please provide an OpenAI API Key in the sidebar.")
                        else:
                            with st.spinner("Analyzing component and generating documentation..."):
                                try:
                                    documenter = ComponentDocumenter(api_key=api_key)
                                    docs = documenter.generate_documentation(content, language)
                                    st.session_state[f"docs_{uploaded_file.name}"] = docs
                                except Exception as e:
                                    st.error(f"An error occurred: {str(e)}")

                    # Display generated docs if they exist in session state
                    if f"docs_{uploaded_file.name}" in st.session_state:
                        docs = st.session_state[f"docs_{uploaded_file.name}"]
                        st.markdown(docs)

                        # Download button
                        st.download_button(
                            label="Download MDX",
                            data=docs,
                            file_name=f"{os.path.splitext(uploaded_file.name)[0]}.mdx",
                            mime="text/markdown",
                            key=f"dl_{uploaded_file.name}"
                        )

    else:
        st.info("Please upload one or more component files to get started.")

if __name__ == "__main__":
    main()
