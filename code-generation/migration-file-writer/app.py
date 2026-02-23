import streamlit as st
import os
import sys

# Add parent directory to path to allow imports from config and agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.migration_agent import MigrationAgent
from config import Config

st.set_page_config(
    page_title="Migration File Writer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤖 Migration File Writer Agent")
st.markdown("Generate database migration files using AI.")

# Sidebar Configuration
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("OpenAI API Key", type="password", value=Config.OPENAI_API_KEY or "")
orm_type = st.sidebar.selectbox("Target ORM", ["Prisma", "Alembic", "Knex"])

st.sidebar.markdown("---")
st.sidebar.markdown("### Instructions")
st.sidebar.info(
    "1. Paste your **Old Schema**.\n"
    "2. Paste your **New Schema**.\n"
    "3. Select your **ORM**.\n"
    "4. Click **Generate Migration**."
)

# Main Content
col1, col2 = st.columns(2)

with col1:
    st.subheader("Old Schema")
    old_schema = st.text_area("Paste old schema here...", height=300)

with col2:
    st.subheader("New Schema")
    new_schema = st.text_area("Paste new schema here...", height=300)

if st.button("Generate Migration", type="primary"):
    if not old_schema or not new_schema:
        st.error("Please provide both old and new schemas.")
    elif not api_key:
        st.error("Please provide an OpenAI API Key.")
    else:
        with st.spinner("Analyzing schemas and generating migration..."):
            try:
                agent = MigrationAgent(api_key=api_key)

                # Generate Migration
                migration_code = agent.generate_migration(old_schema, new_schema, orm_type)

                # Generate Rollback
                rollback_code = agent.generate_rollback(migration_code, orm_type)

                # Analyze Safety
                safety_analysis = agent.analyze_safety(migration_code, old_schema, new_schema)

                st.success("Migration generated successfully!")

                tab1, tab2, tab3 = st.tabs(["Migration Code", "Rollback Code", "Safety Analysis"])

                with tab1:
                    st.code(migration_code, language="sql" if orm_type == "Prisma" else "python" if orm_type == "Alembic" else "javascript")

                with tab2:
                    st.code(rollback_code, language="sql" if orm_type == "Prisma" else "python" if orm_type == "Alembic" else "javascript")

                with tab3:
                    st.markdown(safety_analysis)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Google Jules")
