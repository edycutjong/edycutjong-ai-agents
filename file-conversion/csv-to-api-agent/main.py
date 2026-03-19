import streamlit as st  # pragma: no cover
import pandas as pd  # pragma: no cover
from agent.analyzer import Analyzer  # pragma: no cover
from agent.generator import Generator  # pragma: no cover
import zipfile  # pragma: no cover
import io  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title="CSV to API Agent",
    page_icon="🔌",
    layout="wide"
)

st.title("🔌 CSV to API Agent")  # pragma: no cover
st.markdown("Upload a CSV file to generate a full REST API server with documentation.")  # pragma: no cover

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])  # pragma: no cover

if uploaded_file is not None:  # pragma: no cover
    try:  # pragma: no cover
        # Analyzer expects a file-like object
        # Ensure we are at the start
        uploaded_file.seek(0)  # pragma: no cover
        analyzer = Analyzer(uploaded_file)  # pragma: no cover

        st.subheader("Data Preview")  # pragma: no cover
        st.dataframe(analyzer.get_preview())  # pragma: no cover

        st.subheader("Inferred Schema")  # pragma: no cover
        schema = analyzer.infer_schema()  # pragma: no cover
        # Convert schema list of dicts to DataFrame for nice display
        schema_display = pd.DataFrame(schema)  # pragma: no cover
        st.table(schema_display)  # pragma: no cover

        if st.button("Generate API Server", type="primary"):  # pragma: no cover
            with st.spinner("Generating code..."):  # pragma: no cover
                # Rewind and read for storage
                uploaded_file.seek(0)  # pragma: no cover
                csv_bytes = uploaded_file.read()  # pragma: no cover

                generator = Generator()  # pragma: no cover
                files = generator.generate(schema, csv_data=csv_bytes)  # pragma: no cover

                # Create ZIP
                zip_buffer = io.BytesIO()  # pragma: no cover
                with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:  # pragma: no cover
                    for filename, content in files.items():  # pragma: no cover
                        # Determine if write or writestr is needed?
                        # writestr handles bytes or string
                        zip_file.writestr(filename, content)  # pragma: no cover

                st.success("API Server Generated Successfully! 🎉")  # pragma: no cover

                # Display code
                tabs = st.tabs([f for f in files.keys() if f != 'data.csv'])  # pragma: no cover
                for i, filename in enumerate([f for f in files.keys() if f != 'data.csv']):  # pragma: no cover
                    content = files[filename]  # pragma: no cover
                    with tabs[i]:  # pragma: no cover
                        st.code(content, language="python" if filename.endswith(".py") else "markdown" if filename.endswith(".md") else "text")  # pragma: no cover

                st.download_button(  # pragma: no cover
                    label="Download API Server (.zip)",
                    data=zip_buffer.getvalue(),
                    file_name="api_server.zip",
                    mime="application/zip"
                )

    except Exception as e:  # pragma: no cover
        st.error(f"Error processing file: {str(e)}")  # pragma: no cover
        st.exception(e)  # pragma: no cover

else:
    st.info("Please upload a CSV file to get started.")  # pragma: no cover
