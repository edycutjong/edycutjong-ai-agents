import streamlit as st
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.converter import Converter
from config import config

st.set_page_config(page_title="SQL to NoSQL Migrator", layout="wide")

st.title("SQL to NoSQL Migrator")
st.markdown("Convert your SQL schemas to MongoDB or DynamoDB with AI-powered suggestions.")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    target_db = st.selectbox("Target Database", ["MongoDB", "DynamoDB"])

    if target_db == "MongoDB":
        strategy = st.selectbox("Strategy", ["embed", "reference"])
        st.info("**Embed**: Related data is nested within documents.\n**Reference**: Related data is stored in separate collections with references.")
    else:
        strategy = st.selectbox("Strategy", ["single-table", "multi-table"])
        st.info("**Single Table**: All data in one table with complex keys.\n**Multi Table**: One table per entity.")

    st.header("API Keys")
    openai_key = st.text_input("OpenAI API Key", type="password", value=config.OPENAI_API_KEY if config.OPENAI_API_KEY else "")
    if openai_key:
        config.OPENAI_API_KEY = openai_key

    use_mock = st.checkbox("Use Mock LLM", value=config.USE_MOCK_LLM)
    config.USE_MOCK_LLM = use_mock

# Main Content
input_method = st.radio("Input Method", ["Upload SQL File", "Paste SQL"])

sql_content = ""
if input_method == "Upload SQL File":
    uploaded_file = st.file_uploader("Choose a SQL file", type=["sql"])
    if uploaded_file is not None:
        sql_content = uploaded_file.getvalue().decode("utf-8")
else:
    sql_content = st.text_area("Paste SQL Schema", height=300, value="CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));")

if st.button("Convert", type="primary"):
    if not sql_content.strip():
        st.error("Please provide SQL content.")
    else:
        with st.spinner("Converting..."):
            converter = Converter()
            try:
                result = converter.run(sql_content, target_db, strategy)

                if "error" in result:
                    st.error(result["error"])
                else:
                    st.success("Conversion Successful!")

                    tab1, tab2, tab3, tab4 = st.tabs(["NoSQL Schema", "Migration Script", "Documentation", "Source SQL"])

                    with tab1:
                        st.subheader(f"Generated {target_db} Schema")
                        try:
                            st.json(result["nosql_schema"])
                        except:
                            st.code(result["nosql_schema"], language="json")
                        st.download_button("Download Schema", result["nosql_schema"], file_name=f"schema.json")

                    with tab2:
                        st.subheader("Migration Script")
                        st.code(result["migration_script"], language="python")
                        st.download_button("Download Script", result["migration_script"], file_name="migrate.py")

                    with tab3:
                        st.subheader("Documentation")
                        st.markdown(result["documentation"])
                        st.download_button("Download Docs", result["documentation"], file_name="migration_docs.md")

                    with tab4:
                        st.write(result["sql_schema"])

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.exception(e)
