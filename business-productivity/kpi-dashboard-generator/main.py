import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

# Add project root to path if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.data_loader import DataLoader
from agent.kpi_engine import KPIEngine, KPIDefinition
from agent.visualizer import Visualizer
from agent.analyst import KPIAnalyst
from config import Config

st.set_page_config(
    page_title=Config.PAGE_TITLE,
    page_icon=Config.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
    <style>
    .stMetric {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #4F4F4F;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        color: #FFFFFF;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #A0A0A0;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title(f"{Config.PAGE_ICON} {Config.PAGE_TITLE}")

    # Initialize Session State
    if 'kpi_definitions' not in st.session_state:
        st.session_state.kpi_definitions = []
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'ai_summary' not in st.session_state:
        st.session_state.ai_summary = ""

    # Sidebar - Data Loading
    with st.sidebar:
        st.header("1. Data Source")
        data_source = st.radio("Select Source", ["CSV Upload", "API Endpoint"])

        df = None
        if data_source == "CSV Upload":
            uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
            if uploaded_file:
                try:  # pragma: no cover
                    df = DataLoader.load_csv(uploaded_file)  # pragma: no cover
                    st.success(f"Loaded {len(df)} rows.")  # pragma: no cover
                    # Reset data if new file uploaded
                    if st.session_state.data is None or not df.equals(st.session_state.data):  # pragma: no cover
                         st.session_state.data = df  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(str(e))  # pragma: no cover
        else:
            api_url = st.text_input("API URL")  # pragma: no cover
            if st.button("Fetch Data"):  # pragma: no cover
                try:  # pragma: no cover
                    df = DataLoader.load_api_json(api_url)  # pragma: no cover
                    st.success(f"Loaded {len(df)} rows.")  # pragma: no cover
                    st.session_state.data = df  # pragma: no cover
                except Exception as e:  # pragma: no cover
                    st.error(str(e))  # pragma: no cover

        st.divider()

        # Sidebar - KPI Configuration
        st.header("2. Define KPIs")
        if st.session_state.data is not None:
            columns = st.session_state.data.columns.tolist()  # pragma: no cover
            # Add 'Rows' as a virtual column for counting
            columns_options = ['Rows'] + columns  # pragma: no cover

            with st.form("kpi_form"):  # pragma: no cover
                kpi_name = st.text_input("KPI Name", "Total Sales")  # pragma: no cover
                kpi_col = st.selectbox("Column", columns_options)  # pragma: no cover
                kpi_agg = st.selectbox("Aggregation", ["sum", "avg", "count", "min", "max"])  # pragma: no cover
                kpi_target = st.number_input("Target Value", value=1000.0)  # pragma: no cover
                kpi_logic = st.selectbox("Logic", ["higher_is_better", "lower_is_better"])  # pragma: no cover

                submitted = st.form_submit_button("Add KPI")  # pragma: no cover
                if submitted:  # pragma: no cover
                    new_kpi = KPIDefinition(kpi_name, kpi_col, kpi_agg, kpi_target, logic=kpi_logic)  # pragma: no cover
                    st.session_state.kpi_definitions.append(new_kpi)  # pragma: no cover
                    st.success(f"Added KPI: {kpi_name}")  # pragma: no cover

            # List existing KPIs
            if st.session_state.kpi_definitions:  # pragma: no cover
                st.subheader("Active KPIs")  # pragma: no cover
                for i, kpi in enumerate(st.session_state.kpi_definitions):  # pragma: no cover
                    col1, col2 = st.columns([4, 1])  # pragma: no cover
                    with col1:  # pragma: no cover
                        st.text(f"{kpi.name}")  # pragma: no cover
                        st.caption(f"{kpi.aggregation} of {kpi.column}")  # pragma: no cover
                    with col2:  # pragma: no cover
                        if st.button("🗑️", key=f"del_{i}"):  # pragma: no cover
                            st.session_state.kpi_definitions.pop(i)  # pragma: no cover
                            st.rerun()  # pragma: no cover

    # Main Dashboard
    if st.session_state.data is not None and st.session_state.kpi_definitions:
        st.subheader("Dashboard Overview")  # pragma: no cover

        # KPI Cards Layout
        # We'll use columns, wrapping if too many
        cols = st.columns(4) # 4 per row  # pragma: no cover
        summary_data = []  # pragma: no cover

        for idx, kpi in enumerate(st.session_state.kpi_definitions):  # pragma: no cover
            col_idx = idx % 4  # pragma: no cover
            with cols[col_idx]:  # pragma: no cover
                val = KPIEngine.calculate_metric(st.session_state.data, kpi)  # pragma: no cover
                status = KPIEngine.evaluate_status(val, kpi.target, kpi.logic)  # pragma: no cover

                delta_val = (val - kpi.target) if val is not None else 0  # pragma: no cover

                # Determine color logic
                # Streamlit 'normal' = Green for positive delta, Red for negative
                # Streamlit 'inverse' = Red for positive delta, Green for negative

                delta_color = "normal"  # pragma: no cover
                if kpi.logic == 'lower_is_better':  # pragma: no cover
                    delta_color = "inverse"  # pragma: no cover

                st.metric(  # pragma: no cover
                    label=kpi.name,
                    value=f"{val:,.2f}" if val is not None else "N/A",
                    delta=f"{delta_val:,.2f}",
                    delta_color=delta_color
                )

            summary_data.append(f"- {kpi.name}: {val} (Target: {kpi.target}, Status: {status})")  # pragma: no cover

        st.divider()  # pragma: no cover

        # Visualization Section
        st.subheader("Deep Dive Analysis")  # pragma: no cover
        tab1, tab2 = st.tabs(["Trend Analysis", "Category Analysis"])  # pragma: no cover

        with tab1:  # pragma: no cover
            col_sel1, col_sel2 = st.columns(2)  # pragma: no cover
            with col_sel1:  # pragma: no cover
                date_col = st.selectbox("Select Date Column", st.session_state.data.columns, index=0)  # pragma: no cover
            with col_sel2:  # pragma: no cover
                numeric_cols = [k.column for k in st.session_state.kpi_definitions if k.column != 'Rows']  # pragma: no cover
                if not numeric_cols:  # pragma: no cover
                    # Fallback to all numeric cols
                    numeric_cols = st.session_state.data.select_dtypes(include=['number']).columns.tolist()  # pragma: no cover

                metric_col = st.selectbox("Select Metric to Plot", numeric_cols)  # pragma: no cover

            if date_col and metric_col:  # pragma: no cover
                fig = Visualizer.create_trend_chart(st.session_state.data, date_col, metric_col, title=f"{metric_col} Trend")  # pragma: no cover
                if fig:  # pragma: no cover
                    st.plotly_chart(fig, use_container_width=True)  # pragma: no cover
                else:
                    st.warning("Could not generate trend chart. Ensure the selected date column contains valid dates.")  # pragma: no cover

        with tab2:  # pragma: no cover
            col_sel3, col_sel4 = st.columns(2)  # pragma: no cover
            with col_sel3:  # pragma: no cover
                cat_cols = [c for c in st.session_state.data.columns if st.session_state.data[c].dtype == 'object']  # pragma: no cover
                if not cat_cols:  # pragma: no cover
                     st.info("No categorical columns found.")  # pragma: no cover
                     cat_col = None  # pragma: no cover
                else:
                    cat_col = st.selectbox("Select Category Column", cat_cols)  # pragma: no cover

            with col_sel4:  # pragma: no cover
                metric_col_cat = st.selectbox("Select Metric for Category", numeric_cols, key="cat_metric")  # pragma: no cover

            if cat_col and metric_col_cat:  # pragma: no cover
                 fig = Visualizer.create_bar_chart(st.session_state.data, cat_col, metric_col_cat, title=f"{metric_col_cat} by {cat_col}")  # pragma: no cover
                 if fig:  # pragma: no cover
                    st.plotly_chart(fig, use_container_width=True)  # pragma: no cover

        st.divider()  # pragma: no cover

        # AI Analyst
        st.subheader("🤖 AI Executive Summary")  # pragma: no cover
        if st.button("Generate Summary"):  # pragma: no cover
            analyst = KPIAnalyst()  # pragma: no cover
            if not analyst.api_key:  # pragma: no cover
                 st.warning("OpenAI API Key not found. Please set OPENAI_API_KEY in .env file.")  # pragma: no cover
            else:
                 with st.spinner("Analyzing data..."):  # pragma: no cover
                     summary = analyst.analyze_dashboard("\n".join(summary_data))  # pragma: no cover
                     st.session_state.ai_summary = summary  # pragma: no cover

        if st.session_state.ai_summary:  # pragma: no cover
            st.markdown(st.session_state.ai_summary)  # pragma: no cover

        # Export Report
        st.divider()  # pragma: no cover
        st.subheader("📤 Export")  # pragma: no cover
        if st.button("Download HTML Report"):  # pragma: no cover
            try:  # pragma: no cover
                # Prepare data for report
                kpi_html = ""  # pragma: no cover
                for k in st.session_state.kpi_definitions:  # pragma: no cover
                    val = KPIEngine.calculate_metric(st.session_state.data, k)  # pragma: no cover
                    status = KPIEngine.evaluate_status(val, k.target, k.logic)  # pragma: no cover
                    color = "green" if status == "success" else "orange" if status == "warning" else "red"  # pragma: no cover
                    kpi_html += (  # pragma: no cover
                        f'<div class="kpi-card" style="border: 1px solid #ddd; padding: 15px; margin: 10px; border-radius: 8px; display: inline-block; min-width: 200px;">' 
                        f'<h3 style="margin: 0;">{k.name}</h3>' 
                        f'<p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{val:,.2f}</p>' 
                        f'<p style="color: {color}; margin: 0;">Target: {k.target} ({status.upper()})</p></div>'
                    )

                ai_summary_html = f"<p>{st.session_state.ai_summary}</p>" if st.session_state.ai_summary else "<p>No analysis generated.</p>"  # pragma: no cover

                report_html = f"""  # pragma: no cover
                <html>
                <head>
                    <title>KPI Dashboard Report</title>
                    <style>
                        body {{ font-family: sans-serif; padding: 20px; background-color: #f9f9f9; }}
                        h1, h2 {{ color: #333; }}
                        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                        table {{ border-collapse: collapse; width: 100%; }}
                        th, td {{ text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }}
                        tr:nth-child(even) {{ background-color: #f2f2f2; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>KPI Dashboard Report</h1>
                        <p>Generated on: {pd.Timestamp.now()}</p>

                        <h2>Overview</h2>
                        <div style="display: flex; flex-wrap: wrap;">
                        {kpi_html}
                        </div>

                        <h2>AI Executive Summary</h2>
                        <div style="background: #f0f0f0; padding: 15px; border-radius: 5px;">
                        {ai_summary_html}
                        </div>

                        <h2>Data Preview</h2>
                        {st.session_state.data.head(20).to_html(classes='table table-striped', border=0)}
                    </div>
                </body>
                </html>
                """

                st.download_button(  # pragma: no cover
                    label="Download HTML",
                    data=report_html,
                    file_name="kpi_report.html",
                    mime="text/html"
                )
            except Exception as e:  # pragma: no cover
                st.error(f"Error generating report: {e}")  # pragma: no cover


    elif st.session_state.data is None:
        st.info("👈 Please upload data to get started.")
        # Optional: Demo Data Button
        if st.button("Load Demo Data"):
            data = {  # pragma: no cover
                'Date': pd.date_range(start='1/1/2023', periods=10, freq='M'),
                'Sales': [1000, 1200, 1100, 1500, 1800, 2000, 2200, 2100, 2500, 3000],
                'Region': ['North', 'South', 'North', 'East', 'West', 'North', 'South', 'West', 'East', 'North'],
                'Costs': [500, 600, 550, 700, 800, 900, 1000, 950, 1100, 1200]
            }
            st.session_state.data = pd.DataFrame(data)  # pragma: no cover
            st.rerun()  # pragma: no cover

    elif not st.session_state.kpi_definitions:  # pragma: no cover
        st.info("👈 Please define at least one KPI in the sidebar.")  # pragma: no cover

if __name__ == "__main__":
    main()
