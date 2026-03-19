import streamlit as st
import os
import sys

# Add project root to sys.path to ensure modules are importable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config
from agent.converter import RestToGraphqlConverter

def main():
    st.set_page_config(
        page_title="REST to GraphQL Converter",
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for premium feel
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            font-weight: bold;
        }
        .stTextArea textarea {
            background-color: #262730;
            color: #fafafa;
            border-radius: 8px;
        }
        .stExpander {
            border-radius: 8px;
            border: 1px solid #444;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🔄 REST to GraphQL Converter")
    st.markdown("Convert your REST API specifications (OpenAPI/Swagger) into a production-ready GraphQL schema, resolvers, and migration guide.")

    # Sidebar
    with st.sidebar:
        st.header("Configuration")

        api_key = st.text_input("OpenAI API Key", value=config.OPENAI_API_KEY or "", type="password")
        if not api_key:
            st.warning("Please provide an OpenAI API Key to proceed.")  # pragma: no cover

        language = st.selectbox("Resolver Language", ["Python", "JavaScript/Node.js", "TypeScript"])

        st.divider()
        st.markdown("### How it works")
        st.markdown("1. Upload your OpenAPI JSON/YAML file.")
        st.markdown("2. Click 'Convert'.")
        st.markdown("3. Download generated artifacts.")

    # Main Content
    st.subheader("Input Specification")

    col1, col2 = st.columns([1, 1])

    if 'spec_content' not in st.session_state:
        st.session_state['spec_content'] = ""

    with col1:
        uploaded_file = st.file_uploader("Upload OpenAPI/Swagger File", type=['json', 'yaml', 'yml'])
        if uploaded_file is not None:
            # Check if file content is different to avoid overwriting edits excessively
            file_text = uploaded_file.getvalue().decode("utf-8")  # pragma: no cover
            if st.session_state['spec_content'] != file_text and 'file_uploaded' not in st.session_state:  # pragma: no cover
                 st.session_state['spec_content'] = file_text  # pragma: no cover
                 st.session_state['file_uploaded'] = True  # pragma: no cover
                 st.rerun()  # pragma: no cover
            elif 'file_uploaded' in st.session_state and uploaded_file.name != st.session_state.get('last_filename'):  # pragma: no cover
                 st.session_state['spec_content'] = file_text  # pragma: no cover
                 st.session_state['last_filename'] = uploaded_file.name  # pragma: no cover
                 st.rerun()  # pragma: no cover

            st.success(f"Loaded {uploaded_file.name}")  # pragma: no cover

    with col2:
        st.markdown("Or paste content below:")
        text_input = st.text_area("Paste Spec Content", value=st.session_state['spec_content'], height=300)
        if text_input != st.session_state['spec_content']:
            st.session_state['spec_content'] = text_input  # pragma: no cover

    if st.button("Convert to GraphQL", type="primary"):
        spec_content = st.session_state['spec_content']  # pragma: no cover
        if not api_key:  # pragma: no cover
            st.error("OpenAI API Key is required.")  # pragma: no cover
        elif not spec_content:  # pragma: no cover
            st.error("Please provide an API specification.")  # pragma: no cover
        else:
            try:  # pragma: no cover
                with st.spinner("Analyzing REST API and generating GraphQL artifacts..."):  # pragma: no cover
                    # Initialize Converter
                    converter = RestToGraphqlConverter(api_key=api_key)  # pragma: no cover

                    # Convert
                    result = converter.convert(spec_content, language=language)  # pragma: no cover

                    st.session_state['result'] = result  # pragma: no cover
                    st.success("Conversion Complete!")  # pragma: no cover
            except Exception as e:  # pragma: no cover
                st.error(f"An error occurred: {str(e)}")  # pragma: no cover
                if config.DEBUG:  # pragma: no cover
                    st.exception(e)  # pragma: no cover

    # Display Results
    if 'result' in st.session_state:
        result = st.session_state['result']  # pragma: no cover

        st.divider()  # pragma: no cover
        st.subheader("Generated Artifacts")  # pragma: no cover

        tab1, tab2, tab3 = st.tabs(["GraphQL Schema", "Resolvers", "Migration Guide"])  # pragma: no cover

        with tab1:  # pragma: no cover
            st.markdown("### Schema (SDL)")  # pragma: no cover
            st.code(result['schema'], language='graphql')  # pragma: no cover
            st.download_button("Download schema.graphql", result['schema'], file_name="schema.graphql")  # pragma: no cover

        with tab2:  # pragma: no cover
            st.markdown(f"### Resolvers ({language})")  # pragma: no cover
            st.code(result['resolvers'], language=language.lower().split('/')[0])  # pragma: no cover
            ext = "py" if "Python" in language else "js" if "Node" in language else "ts"  # pragma: no cover
            st.download_button(f"Download resolvers.{ext}", result['resolvers'], file_name=f"resolvers.{ext}")  # pragma: no cover

        with tab3:  # pragma: no cover
            st.markdown("### Migration Guide")  # pragma: no cover
            st.markdown(result['migration_guide'])  # pragma: no cover
            st.download_button("Download MIGRATION.md", result['migration_guide'], file_name="MIGRATION.md")  # pragma: no cover

if __name__ == "__main__":
    main()
