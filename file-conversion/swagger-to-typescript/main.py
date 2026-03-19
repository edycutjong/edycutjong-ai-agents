import streamlit as st  # pragma: no cover
import tempfile  # pragma: no cover
import os  # pragma: no cover
import yaml  # pragma: no cover
from agent.parser import load_swagger  # pragma: no cover
from agent.core import generate_typescript  # pragma: no cover
from config import config  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title="Swagger to TypeScript Agent",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📜 Swagger to TypeScript Agent")  # pragma: no cover
st.markdown("Generate production-ready TypeScript API clients from OpenAPI/Swagger specifications using AI.")  # pragma: no cover

# Sidebar
with st.sidebar:  # pragma: no cover
    st.header("Configuration")  # pragma: no cover

    api_key = st.text_input("OpenAI API Key", type="password", value=config.OPENAI_API_KEY or "")  # pragma: no cover
    if not api_key:  # pragma: no cover
        st.warning("Please enter your OpenAI API Key to proceed.")  # pragma: no cover

    st.divider()  # pragma: no cover

    st.subheader("Output Settings")  # pragma: no cover
    http_client = st.selectbox("HTTP Client", ["axios", "fetch"], index=0)  # pragma: no cover
    module_system = st.selectbox("Module System", ["ES Modules", "CommonJS"], index=0)  # pragma: no cover

    st.divider()  # pragma: no cover
    model_name = st.text_input("Model Name", value=config.MODEL_NAME)  # pragma: no cover
    temperature = st.slider("Temperature", 0.0, 1.0, config.TEMPERATURE)  # pragma: no cover

# Main Content
tab1, tab2 = st.tabs(["📁 Upload File", "🔗 Enter URL"])  # pragma: no cover

# Store spec in session state to persist across reruns
if "swagger_spec" not in st.session_state:  # pragma: no cover
    st.session_state.swagger_spec = None  # pragma: no cover
if "source_name" not in st.session_state:  # pragma: no cover
    st.session_state.source_name = "api"  # pragma: no cover

with tab1:  # pragma: no cover
    uploaded_file = st.file_uploader("Upload Swagger/OpenAPI file", type=["json", "yaml", "yml"])  # pragma: no cover
    if uploaded_file:  # pragma: no cover
        try:  # pragma: no cover
            # Create a temporary file to save the uploaded content
            suffix = f".{uploaded_file.name.split('.')[-1]}"  # pragma: no cover
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:  # pragma: no cover
                tmp.write(uploaded_file.getvalue())  # pragma: no cover
                tmp_path = tmp.name  # pragma: no cover

            # Load the swagger spec
            spec = load_swagger(tmp_path)  # pragma: no cover
            st.session_state.swagger_spec = spec  # pragma: no cover
            st.session_state.source_name = uploaded_file.name.split('.')[0]  # pragma: no cover
            st.success(f"Successfully loaded {uploaded_file.name}")  # pragma: no cover

            # Clean up the temporary file
            os.remove(tmp_path)  # pragma: no cover
        except Exception as e:  # pragma: no cover
            st.error(f"Error loading file: {e}")  # pragma: no cover

with tab2:  # pragma: no cover
    url = st.text_input("Swagger/OpenAPI URL", placeholder="https://petstore.swagger.io/v2/swagger.json")  # pragma: no cover
    if url:  # pragma: no cover
        if st.button("Load URL"):  # pragma: no cover
            try:  # pragma: no cover
                with st.spinner("Fetching Swagger..."):  # pragma: no cover
                    spec = load_swagger(url)  # pragma: no cover
                    st.session_state.swagger_spec = spec  # pragma: no cover
                    st.session_state.source_name = url.split('/')[-1].split('.')[0] or "api"  # pragma: no cover
                    st.success("Successfully loaded Swagger from URL")  # pragma: no cover
            except Exception as e:  # pragma: no cover
                st.error(f"Error loading URL: {e}")  # pragma: no cover

if st.session_state.swagger_spec:  # pragma: no cover
    with st.expander("View Loaded Specification"):  # pragma: no cover
        st.json(st.session_state.swagger_spec)  # pragma: no cover

    st.divider()  # pragma: no cover
    if st.button("Generate TypeScript", type="primary", disabled=not api_key):  # pragma: no cover
        with st.spinner("Generating TypeScript code... (This may take a moment)"):  # pragma: no cover
            try:  # pragma: no cover
                ts_code = generate_typescript(  # pragma: no cover
                    swagger_spec=st.session_state.swagger_spec,
                    http_client=http_client,
                    module_system=module_system,
                    model_name=model_name,
                    temperature=temperature,
                    api_key=api_key
                )

                st.subheader("Generated TypeScript")  # pragma: no cover
                st.code(ts_code, language="typescript")  # pragma: no cover

                st.download_button(  # pragma: no cover
                    label="Download .ts file",
                    data=ts_code,
                    file_name=f"{st.session_state.source_name}_client.ts",
                    mime="application/typescript"
                )
            except Exception as e:  # pragma: no cover
                st.error(f"Generation failed: {e}")  # pragma: no cover
