import streamlit as st  # pragma: no cover
import pandas as pd  # pragma: no cover
import os  # pragma: no cover
from agent.core import DataValidator  # pragma: no cover
from agent.llm import LLMAnalyzer  # pragma: no cover
import plotly.express as px  # pragma: no cover
import plotly.graph_objects as go  # pragma: no cover

# Page Configuration
st.set_page_config(  # pragma: no cover
    page_title="Data Pipeline Validator",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'validation_results' not in st.session_state:  # pragma: no cover
    st.session_state.validation_results = None  # pragma: no cover
if 'analyzed' not in st.session_state:  # pragma: no cover
    st.session_state.analyzed = False  # pragma: no cover

# Sidebar
with st.sidebar:  # pragma: no cover
    st.title("Settings")  # pragma: no cover
    api_key = st.text_input("OpenAI API Key", type="password", help="Required for AI Analysis")  # pragma: no cover
    if not api_key:  # pragma: no cover
        api_key = os.getenv("OPENAI_API_KEY")  # pragma: no cover

    st.divider()  # pragma: no cover
    st.markdown("### About")  # pragma: no cover
    st.info(  # pragma: no cover
        "This tool validates data integrity between source and destination systems. "
        "It checks for schema mismatches, row counts, data quality issues, and uses AI "
        "to verify transformation logic."
    )

# Main Title
st.title("🔍 Data Pipeline Validator Agent")  # pragma: no cover
st.markdown("Upload your Source and Destination files to validate the ETL pipeline.")  # pragma: no cover

# Tabs
tab_config, tab_results, tab_ai = st.tabs(["Configuration", "Validation Results", "AI Analysis"])  # pragma: no cover

# Configuration Tab
with tab_config:  # pragma: no cover
    col1, col2 = st.columns(2)  # pragma: no cover

    with col1:  # pragma: no cover
        st.subheader("Source Data")  # pragma: no cover
        source_file = st.file_uploader("Upload Source File", type=["csv", "parquet", "xlsx"], key="source_file")  # pragma: no cover

    with col2:  # pragma: no cover
        st.subheader("Destination Data")  # pragma: no cover
        dest_file = st.file_uploader("Upload Destination File", type=["csv", "parquet", "xlsx"], key="dest_file")  # pragma: no cover

    st.subheader("Transformation Logic (Optional)")  # pragma: no cover
    transform_rule = st.text_area(  # pragma: no cover
        "Describe the transformation rule (for AI Verification)",
        placeholder="e.g., Filter out users under 18 and rename column 'dob' to 'date_of_birth'...",
        key="transform_rule"
    )

    if st.button("Run Validation", type="primary", use_container_width=True):  # pragma: no cover
        if not source_file or not dest_file:  # pragma: no cover
            st.error("Please upload both Source and Destination files.")  # pragma: no cover
        else:
            with st.spinner("Running Validation..."):  # pragma: no cover
                try:  # pragma: no cover
                    validator = DataValidator()  # pragma: no cover

                    # Determine file type from extension
                    s_type = source_file.name.split('.')[-1].lower()  # pragma: no cover
                    d_type = dest_file.name.split('.')[-1].lower()  # pragma: no cover

                    # Load Data
                    # Streamlit file objects are seekable, so can be passed to pandas read_*
                    source_df = validator.load_data(source_file, file_type=s_type)  # pragma: no cover
                    dest_df = validator.load_data(dest_file, file_type=d_type)  # pragma: no cover

                    # Store dataframes in session for visualization (limit size if needed)
                    st.session_state.source_df = source_df  # pragma: no cover
                    st.session_state.dest_df = dest_df  # pragma: no cover

                    # Run Validation
                    results = validator.run_full_validation(source_df, dest_df)  # pragma: no cover
                    st.session_state.validation_results = results  # pragma: no cover
                    st.session_state.analyzed = False # Reset AI analysis  # pragma: no cover

                    st.success("Validation Complete! Switch to 'Validation Results' tab.")  # pragma: no cover

                except Exception as e:  # pragma: no cover
                    st.error(f"Validation Failed: {str(e)}")  # pragma: no cover

# Results Tab
with tab_results:  # pragma: no cover
    if st.session_state.validation_results:  # pragma: no cover
        results = st.session_state.validation_results  # pragma: no cover

        # Metrics
        st.markdown("### 📊 Overview")  # pragma: no cover
        m1, m2, m3, m4 = st.columns(4)  # pragma: no cover
        m1.metric("Source Rows", results['row_counts']['source_count'])  # pragma: no cover
        m2.metric("Dest Rows", results['row_counts']['dest_count'])  # pragma: no cover
        m3.metric("Row Diff", results['row_counts']['diff'])  # pragma: no cover
        m4.metric("Schema Match", "✅ Yes" if results['schema']['schema_match'] else "❌ No")  # pragma: no cover

        st.divider()  # pragma: no cover

        # Schema Details
        st.markdown("### 🧬 Schema Comparison")  # pragma: no cover
        if results['schema']['schema_match']:  # pragma: no cover
            st.success("Schemas match perfectly.")  # pragma: no cover
        else:
            c1, c2 = st.columns(2)  # pragma: no cover
            with c1:  # pragma: no cover
                st.error("Missing Columns in Dest")  # pragma: no cover
                st.write(results['schema']['missing_columns'])  # pragma: no cover
            with c2:  # pragma: no cover
                st.warning("Type Mismatches")  # pragma: no cover
                st.write(results['schema']['type_mismatches'])  # pragma: no cover

        st.divider()  # pragma: no cover

        # Data Quality
        st.markdown("### 🧹 Data Quality")  # pragma: no cover
        c1, c2 = st.columns(2)  # pragma: no cover
        with c1:  # pragma: no cover
            st.markdown("**Source Quality**")  # pragma: no cover
            st.json(results['source_quality'])  # pragma: no cover
        with c2:  # pragma: no cover
            st.markdown("**Destination Quality**")  # pragma: no cover
            st.json(results['dest_quality'])  # pragma: no cover

        st.divider()  # pragma: no cover

        # Distributions
        st.markdown("### 📈 Distribution Analysis (Numeric Columns)")  # pragma: no cover
        stats = results['distributions']  # pragma: no cover
        if not stats:  # pragma: no cover
            st.info("No common numeric columns found.")  # pragma: no cover
        else:
            # Dropdown to select column
            col_options = list(stats.keys())  # pragma: no cover
            selected_col = st.selectbox("Select Column to Visualize", col_options)  # pragma: no cover

            if selected_col:  # pragma: no cover
                # Plotly Histogram
                source_df = st.session_state.source_df  # pragma: no cover
                dest_df = st.session_state.dest_df  # pragma: no cover

                fig = go.Figure()  # pragma: no cover
                fig.add_trace(go.Histogram(x=source_df[selected_col], name='Source', opacity=0.7))  # pragma: no cover
                fig.add_trace(go.Histogram(x=dest_df[selected_col], name='Destination', opacity=0.7))  # pragma: no cover
                fig.update_layout(barmode='overlay', title=f"Distribution of '{selected_col}'")  # pragma: no cover
                st.plotly_chart(fig, use_container_width=True)  # pragma: no cover

                # Stats table
                st.table(pd.DataFrame([stats[selected_col]]))  # pragma: no cover

    else:
        st.info("Run validation to see results.")  # pragma: no cover

# AI Analysis Tab
with tab_ai:  # pragma: no cover
    if st.session_state.validation_results:  # pragma: no cover
        st.markdown("### 🤖 AI Agent Analysis")  # pragma: no cover

        if not api_key:  # pragma: no cover
            st.warning("Please enter OpenAI API Key in settings sidebar to use AI features.")  # pragma: no cover
        else:
            if st.button("Generate AI Report"):  # pragma: no cover
                with st.spinner("Analyzing Validation Report..."):  # pragma: no cover
                    llm = LLMAnalyzer(api_key=api_key)  # pragma: no cover
                    analysis = llm.analyze_report(st.session_state.validation_results)  # pragma: no cover
                    st.session_state.ai_analysis = analysis  # pragma: no cover
                    st.session_state.analyzed = True  # pragma: no cover

            if st.session_state.get('analyzed'):  # pragma: no cover
                st.markdown("#### Validation Summary")  # pragma: no cover
                st.write(st.session_state.ai_analysis)  # pragma: no cover

            st.divider()  # pragma: no cover

            st.markdown("### 🕵️ Transformation Verification")  # pragma: no cover
            rule = st.session_state.get('transform_rule')  # pragma: no cover
            if not rule:  # pragma: no cover
                st.info("Enter a transformation rule in Configuration tab to verify logic.")  # pragma: no cover
            else:
                if st.button("Verify Transformation Logic"):  # pragma: no cover
                    with st.spinner("Verifying Transformation Logic..."):  # pragma: no cover
                        llm = LLMAnalyzer(api_key=api_key)  # pragma: no cover
                        # Sample 5 rows
                        s_sample = st.session_state.source_df.head(5)  # pragma: no cover
                        d_sample = st.session_state.dest_df.head(5)  # pragma: no cover
                        verification = llm.verify_transformation(s_sample, d_sample, rule)  # pragma: no cover
                        st.session_state.ai_verification = verification  # pragma: no cover

                if st.session_state.get('ai_verification'):  # pragma: no cover
                    st.markdown("#### Verification Result")  # pragma: no cover
                    st.write(st.session_state.ai_verification)  # pragma: no cover

    else:
        st.info("Run validation to see AI analysis.")  # pragma: no cover
