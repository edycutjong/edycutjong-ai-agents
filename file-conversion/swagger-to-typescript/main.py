import streamlit as st
import tempfile
import os
import yaml
from agent.parser import load_swagger
from agent.core import generate_typescript
from config import config

st.set_page_config(
    page_title="Swagger to TypeScript Agent",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📜 Swagger to TypeScript Agent")
st.markdown("Generate production-ready TypeScript API clients from OpenAPI/Swagger specifications using AI.")

# Sidebar
with st.sidebar:
    st.header("Configuration")

    api_key = st.text_input("OpenAI API Key", type="password", value=config.OPENAI_API_KEY or "")
    if not api_key:
        st.warning("Please enter your OpenAI API Key to proceed.")

    st.divider()

    st.subheader("Output Settings")
    http_client = st.selectbox("HTTP Client", ["axios", "fetch"], index=0)
    module_system = st.selectbox("Module System", ["ES Modules", "CommonJS"], index=0)

    st.divider()
    model_name = st.text_input("Model Name", value=config.MODEL_NAME)
    temperature = st.slider("Temperature", 0.0, 1.0, config.TEMPERATURE)

# Main Content
tab1, tab2 = st.tabs(["📁 Upload File", "🔗 Enter URL"])

# Store spec in session state to persist across reruns
if "swagger_spec" not in st.session_state:
    st.session_state.swagger_spec = None
if "source_name" not in st.session_state:
    st.session_state.source_name = "api"

with tab1:
    uploaded_file = st.file_uploader("Upload Swagger/OpenAPI file", type=["json", "yaml", "yml"])
    if uploaded_file:
        try:
            # Create a temporary file to save the uploaded content
            suffix = f".{uploaded_file.name.split('.')[-1]}"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            # Load the swagger spec
            spec = load_swagger(tmp_path)
            st.session_state.swagger_spec = spec
            st.session_state.source_name = uploaded_file.name.split('.')[0]
            st.success(f"Successfully loaded {uploaded_file.name}")

            # Clean up the temporary file
            os.remove(tmp_path)
        except Exception as e:
            st.error(f"Error loading file: {e}")

with tab2:
    url = st.text_input("Swagger/OpenAPI URL", placeholder="https://petstore.swagger.io/v2/swagger.json")
    if url:
        if st.button("Load URL"):
            try:
                with st.spinner("Fetching Swagger..."):
                    spec = load_swagger(url)
                    st.session_state.swagger_spec = spec
                    st.session_state.source_name = url.split('/')[-1].split('.')[0] or "api"
                    st.success("Successfully loaded Swagger from URL")
            except Exception as e:
                st.error(f"Error loading URL: {e}")

if st.session_state.swagger_spec:
    with st.expander("View Loaded Specification"):
        st.json(st.session_state.swagger_spec)

    st.divider()
    if st.button("Generate TypeScript", type="primary", disabled=not api_key):
        with st.spinner("Generating TypeScript code... (This may take a moment)"):
            try:
                ts_code = generate_typescript(
                    swagger_spec=st.session_state.swagger_spec,
                    http_client=http_client,
                    module_system=module_system,
                    model_name=model_name,
                    temperature=temperature,
                    api_key=api_key
                )

                st.subheader("Generated TypeScript")
                st.code(ts_code, language="typescript")

                st.download_button(
                    label="Download .ts file",
                    data=ts_code,
                    file_name=f"{st.session_state.source_name}_client.ts",
                    mime="application/typescript"
                )
            except Exception as e:
                st.error(f"Generation failed: {e}")
