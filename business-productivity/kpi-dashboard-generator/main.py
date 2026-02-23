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
                try:
                    df = DataLoader.load_csv(uploaded_file)
                    st.success(f"Loaded {len(df)} rows.")
                    # Reset data if new file uploaded
                    if st.session_state.data is None or not df.equals(st.session_state.data):
                         st.session_state.data = df
                except Exception as e:
                    st.error(str(e))
        else:
            api_url = st.text_input("API URL")
            if st.button("Fetch Data"):
                try:
                    df = DataLoader.load_api_json(api_url)
                    st.success(f"Loaded {len(df)} rows.")
                    st.session_state.data = df
                except Exception as e:
                    st.error(str(e))

        st.divider()

        # Sidebar - KPI Configuration
        st.header("2. Define KPIs")
        if st.session_state.data is not None:
            columns = st.session_state.data.columns.tolist()
            # Add 'Rows' as a virtual column for counting
            columns_options = ['Rows'] + columns

            with st.form("kpi_form"):
                kpi_name = st.text_input("KPI Name", "Total Sales")
                kpi_col = st.selectbox("Column", columns_options)
                kpi_agg = st.selectbox("Aggregation", ["sum", "avg", "count", "min", "max"])
                kpi_target = st.number_input("Target Value", value=1000.0)
                kpi_logic = st.selectbox("Logic", ["higher_is_better", "lower_is_better"])

                submitted = st.form_submit_button("Add KPI")
                if submitted:
                    new_kpi = KPIDefinition(kpi_name, kpi_col, kpi_agg, kpi_target, logic=kpi_logic)
                    st.session_state.kpi_definitions.append(new_kpi)
                    st.success(f"Added KPI: {kpi_name}")

            # List existing KPIs
            if st.session_state.kpi_definitions:
                st.subheader("Active KPIs")
                for i, kpi in enumerate(st.session_state.kpi_definitions):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.text(f"{kpi.name}")
                        st.caption(f"{kpi.aggregation} of {kpi.column}")
                    with col2:
                        if st.button("🗑️", key=f"del_{i}"):
                            st.session_state.kpi_definitions.pop(i)
                            st.rerun()

    # Main Dashboard
    if st.session_state.data is not None and st.session_state.kpi_definitions:
        st.subheader("Dashboard Overview")

        # KPI Cards Layout
        # We'll use columns, wrapping if too many
        cols = st.columns(4) # 4 per row
        summary_data = []

        for idx, kpi in enumerate(st.session_state.kpi_definitions):
            col_idx = idx % 4
            with cols[col_idx]:
                val = KPIEngine.calculate_metric(st.session_state.data, kpi)
                status = KPIEngine.evaluate_status(val, kpi.target, kpi.logic)

                delta_val = (val - kpi.target) if val is not None else 0

                # Determine color logic
                # Streamlit 'normal' = Green for positive delta, Red for negative
                # Streamlit 'inverse' = Red for positive delta, Green for negative

                delta_color = "normal"
                if kpi.logic == 'lower_is_better':
                    delta_color = "inverse"

                st.metric(
                    label=kpi.name,
                    value=f"{val:,.2f}" if val is not None else "N/A",
                    delta=f"{delta_val:,.2f}",
                    delta_color=delta_color
                )

            summary_data.append(f"- {kpi.name}: {val} (Target: {kpi.target}, Status: {status})")

        st.divider()

        # Visualization Section
        st.subheader("Deep Dive Analysis")
        tab1, tab2 = st.tabs(["Trend Analysis", "Category Analysis"])

        with tab1:
            col_sel1, col_sel2 = st.columns(2)
            with col_sel1:
                date_col = st.selectbox("Select Date Column", st.session_state.data.columns, index=0)
            with col_sel2:
                numeric_cols = [k.column for k in st.session_state.kpi_definitions if k.column != 'Rows']
                if not numeric_cols:
                    # Fallback to all numeric cols
                    numeric_cols = st.session_state.data.select_dtypes(include=['number']).columns.tolist()

                metric_col = st.selectbox("Select Metric to Plot", numeric_cols)

            if date_col and metric_col:
                fig = Visualizer.create_trend_chart(st.session_state.data, date_col, metric_col, title=f"{metric_col} Trend")
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Could not generate trend chart. Ensure the selected date column contains valid dates.")

        with tab2:
            col_sel3, col_sel4 = st.columns(2)
            with col_sel3:
                cat_cols = [c for c in st.session_state.data.columns if st.session_state.data[c].dtype == 'object']
                if not cat_cols:
                     st.info("No categorical columns found.")
                     cat_col = None
                else:
                    cat_col = st.selectbox("Select Category Column", cat_cols)

            with col_sel4:
                metric_col_cat = st.selectbox("Select Metric for Category", numeric_cols, key="cat_metric")

            if cat_col and metric_col_cat:
                 fig = Visualizer.create_bar_chart(st.session_state.data, cat_col, metric_col_cat, title=f"{metric_col_cat} by {cat_col}")
                 if fig:
                    st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # AI Analyst
        st.subheader("🤖 AI Executive Summary")
        if st.button("Generate Summary"):
            analyst = KPIAnalyst()
            if not analyst.api_key:
                 st.warning("OpenAI API Key not found. Please set OPENAI_API_KEY in .env file.")
            else:
                 with st.spinner("Analyzing data..."):
                     summary = analyst.analyze_dashboard("\n".join(summary_data))
                     st.session_state.ai_summary = summary

        if st.session_state.ai_summary:
            st.markdown(st.session_state.ai_summary)

        # Export Report
        st.divider()
        st.subheader("📤 Export")
        if st.button("Download HTML Report"):
            try:
                # Prepare data for report
                kpi_html = ""
                for k in st.session_state.kpi_definitions:
                    val = KPIEngine.calculate_metric(st.session_state.data, k)
                    status = KPIEngine.evaluate_status(val, k.target, k.logic)
                    color = "green" if status == "success" else "orange" if status == "warning" else "red"
                    kpi_html += f'<div class="kpi-card" style="border: 1px solid #ddd; padding: 15px; margin: 10px; border-radius: 8px; display: inline-block; min-width: 200px;">' \
                                f'<h3 style="margin: 0;">{k.name}</h3>' \
                                f'<p style="font-size: 24px; font-weight: bold; margin: 10px 0;">{val:,.2f}</p>' \
                                f'<p style="color: {color}; margin: 0;">Target: {k.target} ({status.upper()})</p></div>'

                ai_summary_html = f"<p>{st.session_state.ai_summary}</p>" if st.session_state.ai_summary else "<p>No analysis generated.</p>"

                report_html = f"""
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

                st.download_button(
                    label="Download HTML",
                    data=report_html,
                    file_name="kpi_report.html",
                    mime="text/html"
                )
            except Exception as e:
                st.error(f"Error generating report: {e}")


    elif st.session_state.data is None:
        st.info("👈 Please upload data to get started.")
        # Optional: Demo Data Button
        if st.button("Load Demo Data"):
            data = {
                'Date': pd.date_range(start='1/1/2023', periods=10, freq='M'),
                'Sales': [1000, 1200, 1100, 1500, 1800, 2000, 2200, 2100, 2500, 3000],
                'Region': ['North', 'South', 'North', 'East', 'West', 'North', 'South', 'West', 'East', 'North'],
                'Costs': [500, 600, 550, 700, 800, 900, 1000, 950, 1100, 1200]
            }
            st.session_state.data = pd.DataFrame(data)
            st.rerun()

    elif not st.session_state.kpi_definitions:
        st.info("👈 Please define at least one KPI in the sidebar.")

if __name__ == "__main__":
    main()
