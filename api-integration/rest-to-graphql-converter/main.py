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
            st.warning("Please provide an OpenAI API Key to proceed.")

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
            file_text = uploaded_file.getvalue().decode("utf-8")
            if st.session_state['spec_content'] != file_text and 'file_uploaded' not in st.session_state:
                 st.session_state['spec_content'] = file_text
                 st.session_state['file_uploaded'] = True
                 st.rerun()
            elif 'file_uploaded' in st.session_state and uploaded_file.name != st.session_state.get('last_filename'):
                 st.session_state['spec_content'] = file_text
                 st.session_state['last_filename'] = uploaded_file.name
                 st.rerun()

            st.success(f"Loaded {uploaded_file.name}")

    with col2:
        st.markdown("Or paste content below:")
        text_input = st.text_area("Paste Spec Content", value=st.session_state['spec_content'], height=300)
        if text_input != st.session_state['spec_content']:
            st.session_state['spec_content'] = text_input

    if st.button("Convert to GraphQL", type="primary"):
        spec_content = st.session_state['spec_content']
        if not api_key:
            st.error("OpenAI API Key is required.")
        elif not spec_content:
            st.error("Please provide an API specification.")
        else:
            try:
                with st.spinner("Analyzing REST API and generating GraphQL artifacts..."):
                    # Initialize Converter
                    converter = RestToGraphqlConverter(api_key=api_key)

                    # Convert
                    result = converter.convert(spec_content, language=language)

                    st.session_state['result'] = result
                    st.success("Conversion Complete!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                if config.DEBUG:
                    st.exception(e)

    # Display Results
    if 'result' in st.session_state:
        result = st.session_state['result']

        st.divider()
        st.subheader("Generated Artifacts")

        tab1, tab2, tab3 = st.tabs(["GraphQL Schema", "Resolvers", "Migration Guide"])

        with tab1:
            st.markdown("### Schema (SDL)")
            st.code(result['schema'], language='graphql')
            st.download_button("Download schema.graphql", result['schema'], file_name="schema.graphql")

        with tab2:
            st.markdown(f"### Resolvers ({language})")
            st.code(result['resolvers'], language=language.lower().split('/')[0])
            ext = "py" if "Python" in language else "js" if "Node" in language else "ts"
            st.download_button(f"Download resolvers.{ext}", result['resolvers'], file_name=f"resolvers.{ext}")

        with tab3:
            st.markdown("### Migration Guide")
            st.markdown(result['migration_guide'])
            st.download_button("Download MIGRATION.md", result['migration_guide'], file_name="MIGRATION.md")

if __name__ == "__main__":
    main()
