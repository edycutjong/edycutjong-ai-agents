import streamlit as st
import pandas as pd
from agent.analyzer import Analyzer
from agent.generator import Generator
import zipfile
import io

st.set_page_config(
    page_title="CSV to API Agent",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 CSV to API Agent")
st.markdown("Upload a CSV file to generate a full REST API server with documentation.")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    try:
        # Analyzer expects a file-like object
        # Ensure we are at the start
        uploaded_file.seek(0)
        analyzer = Analyzer(uploaded_file)

        st.subheader("Data Preview")
        st.dataframe(analyzer.get_preview())

        st.subheader("Inferred Schema")
        schema = analyzer.infer_schema()
        # Convert schema list of dicts to DataFrame for nice display
        schema_display = pd.DataFrame(schema)
        st.table(schema_display)

        if st.button("Generate API Server", type="primary"):
            with st.spinner("Generating code..."):
                # Rewind and read for storage
                uploaded_file.seek(0)
                csv_bytes = uploaded_file.read()

                generator = Generator()
                files = generator.generate(schema, csv_data=csv_bytes)

                # Create ZIP
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                    for filename, content in files.items():
                        # Determine if write or writestr is needed?
                        # writestr handles bytes or string
                        zip_file.writestr(filename, content)

                st.success("API Server Generated Successfully! 🎉")

                # Display code
                tabs = st.tabs([f for f in files.keys() if f != 'data.csv'])
                for i, filename in enumerate([f for f in files.keys() if f != 'data.csv']):
                    content = files[filename]
                    with tabs[i]:
                        st.code(content, language="python" if filename.endswith(".py") else "markdown" if filename.endswith(".md") else "text")

                st.download_button(
                    label="Download API Server (.zip)",
                    data=zip_buffer.getvalue(),
                    file_name="api_server.zip",
                    mime="application/zip"
                )

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.exception(e)

else:
    st.info("Please upload a CSV file to get started.")
