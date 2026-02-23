import streamlit as st
import pandas as pd
import os
from agent.core import DataValidator
from agent.llm import LLMAnalyzer
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Data Pipeline Validator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'validation_results' not in st.session_state:
    st.session_state.validation_results = None
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

# Sidebar
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("OpenAI API Key", type="password", help="Required for AI Analysis")
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")

    st.divider()
    st.markdown("### About")
    st.info(
        "This tool validates data integrity between source and destination systems. "
        "It checks for schema mismatches, row counts, data quality issues, and uses AI "
        "to verify transformation logic."
    )

# Main Title
st.title("🔍 Data Pipeline Validator Agent")
st.markdown("Upload your Source and Destination files to validate the ETL pipeline.")

# Tabs
tab_config, tab_results, tab_ai = st.tabs(["Configuration", "Validation Results", "AI Analysis"])

# Configuration Tab
with tab_config:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Source Data")
        source_file = st.file_uploader("Upload Source File", type=["csv", "parquet", "xlsx"], key="source_file")

    with col2:
        st.subheader("Destination Data")
        dest_file = st.file_uploader("Upload Destination File", type=["csv", "parquet", "xlsx"], key="dest_file")

    st.subheader("Transformation Logic (Optional)")
    transform_rule = st.text_area(
        "Describe the transformation rule (for AI Verification)",
        placeholder="e.g., Filter out users under 18 and rename column 'dob' to 'date_of_birth'...",
        key="transform_rule"
    )

    if st.button("Run Validation", type="primary", use_container_width=True):
        if not source_file or not dest_file:
            st.error("Please upload both Source and Destination files.")
        else:
            with st.spinner("Running Validation..."):
                try:
                    validator = DataValidator()

                    # Determine file type from extension
                    s_type = source_file.name.split('.')[-1].lower()
                    d_type = dest_file.name.split('.')[-1].lower()

                    # Load Data
                    # Streamlit file objects are seekable, so can be passed to pandas read_*
                    source_df = validator.load_data(source_file, file_type=s_type)
                    dest_df = validator.load_data(dest_file, file_type=d_type)

                    # Store dataframes in session for visualization (limit size if needed)
                    st.session_state.source_df = source_df
                    st.session_state.dest_df = dest_df

                    # Run Validation
                    results = validator.run_full_validation(source_df, dest_df)
                    st.session_state.validation_results = results
                    st.session_state.analyzed = False # Reset AI analysis

                    st.success("Validation Complete! Switch to 'Validation Results' tab.")

                except Exception as e:
                    st.error(f"Validation Failed: {str(e)}")

# Results Tab
with tab_results:
    if st.session_state.validation_results:
        results = st.session_state.validation_results

        # Metrics
        st.markdown("### 📊 Overview")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Source Rows", results['row_counts']['source_count'])
        m2.metric("Dest Rows", results['row_counts']['dest_count'])
        m3.metric("Row Diff", results['row_counts']['diff'])
        m4.metric("Schema Match", "✅ Yes" if results['schema']['schema_match'] else "❌ No")

        st.divider()

        # Schema Details
        st.markdown("### 🧬 Schema Comparison")
        if results['schema']['schema_match']:
            st.success("Schemas match perfectly.")
        else:
            c1, c2 = st.columns(2)
            with c1:
                st.error("Missing Columns in Dest")
                st.write(results['schema']['missing_columns'])
            with c2:
                st.warning("Type Mismatches")
                st.write(results['schema']['type_mismatches'])

        st.divider()

        # Data Quality
        st.markdown("### 🧹 Data Quality")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Source Quality**")
            st.json(results['source_quality'])
        with c2:
            st.markdown("**Destination Quality**")
            st.json(results['dest_quality'])

        st.divider()

        # Distributions
        st.markdown("### 📈 Distribution Analysis (Numeric Columns)")
        stats = results['distributions']
        if not stats:
            st.info("No common numeric columns found.")
        else:
            # Dropdown to select column
            col_options = list(stats.keys())
            selected_col = st.selectbox("Select Column to Visualize", col_options)

            if selected_col:
                # Plotly Histogram
                source_df = st.session_state.source_df
                dest_df = st.session_state.dest_df

                fig = go.Figure()
                fig.add_trace(go.Histogram(x=source_df[selected_col], name='Source', opacity=0.7))
                fig.add_trace(go.Histogram(x=dest_df[selected_col], name='Destination', opacity=0.7))
                fig.update_layout(barmode='overlay', title=f"Distribution of '{selected_col}'")
                st.plotly_chart(fig, use_container_width=True)

                # Stats table
                st.table(pd.DataFrame([stats[selected_col]]))

    else:
        st.info("Run validation to see results.")

# AI Analysis Tab
with tab_ai:
    if st.session_state.validation_results:
        st.markdown("### 🤖 AI Agent Analysis")

        if not api_key:
            st.warning("Please enter OpenAI API Key in settings sidebar to use AI features.")
        else:
            if st.button("Generate AI Report"):
                with st.spinner("Analyzing Validation Report..."):
                    llm = LLMAnalyzer(api_key=api_key)
                    analysis = llm.analyze_report(st.session_state.validation_results)
                    st.session_state.ai_analysis = analysis
                    st.session_state.analyzed = True

            if st.session_state.get('analyzed'):
                st.markdown("#### Validation Summary")
                st.write(st.session_state.ai_analysis)

            st.divider()

            st.markdown("### 🕵️ Transformation Verification")
            rule = st.session_state.get('transform_rule')
            if not rule:
                st.info("Enter a transformation rule in Configuration tab to verify logic.")
            else:
                if st.button("Verify Transformation Logic"):
                    with st.spinner("Verifying Transformation Logic..."):
                        llm = LLMAnalyzer(api_key=api_key)
                        # Sample 5 rows
                        s_sample = st.session_state.source_df.head(5)
                        d_sample = st.session_state.dest_df.head(5)
                        verification = llm.verify_transformation(s_sample, d_sample, rule)
                        st.session_state.ai_verification = verification

                if st.session_state.get('ai_verification'):
                    st.markdown("#### Verification Result")
                    st.write(st.session_state.ai_verification)

    else:
        st.info("Run validation to see AI analysis.")
