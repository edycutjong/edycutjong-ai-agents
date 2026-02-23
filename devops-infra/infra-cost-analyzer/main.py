import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

# Ensure the current directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.parser import parse_billing_csv
from agent.analyzer import CostAnalyzer
from agent.recommender import Recommender
from agent.llm_agent import FinOpsAgent
from config import Config

# Cache the data loading function
@st.cache_data
def load_data(uploaded_file, provider):
    # Reset file pointer just in case
    uploaded_file.seek(0)
    return parse_billing_csv(uploaded_file, provider=provider.lower())

def main():
    st.set_page_config(
        page_title="Infrastructure Cost Analyzer",
        page_icon="💸",
        layout="wide"
    )

    st.title("💸 Infrastructure Cost Analyzer")
    st.markdown("Upload your cloud billing CSV to identify waste and get cost-saving recommendations.")

    # Sidebar
    st.sidebar.header("Configuration")

    # Provider Selection
    provider_options = ["Generic", "AWS", "GCP", "Azure"]
    provider = st.sidebar.selectbox(
        "Cloud Provider",
        provider_options,
        index=0
    )

    currency = st.sidebar.text_input("Currency", value=Config.CURRENCY)

    # File Upload
    uploaded_file = st.file_uploader("Upload Billing CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            with st.spinner("Parsing billing data..."):
                df = load_data(uploaded_file, provider)
                st.session_state['df'] = df

                # Analyze Data
                analyzer = CostAnalyzer(df)
                total_cost = analyzer.calculate_total_cost()
                cost_by_service = analyzer.calculate_cost_by_service()
                daily_trend = analyzer.calculate_daily_trend()
                waste_df = analyzer.identify_potential_waste()
                anomalies = analyzer.detect_anomalies()

                # Recommendations
                recommender = Recommender(waste_df)
                right_sizing = recommender.suggest_right_sizing()
                potential_savings = recommender.calculate_total_potential_savings()

            st.success(f"Successfully loaded {len(df)} records.")

            # Dashboard Tabs
            tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🤖 AI Insights", "📋 Details"])

            with tab1:
                # Key Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Cost", f"{currency} {total_cost:,.2f}")
                col2.metric("Potential Savings", f"{currency} {potential_savings:,.2f}",
                           delta=f"{potential_savings/total_cost*100:.1f}%" if total_cost > 0 else "0%",
                           delta_color="inverse")
                col3.metric("Waste Items Identified", len(waste_df))

                # Charts
                col_chart1, col_chart2 = st.columns(2)

                with col_chart1:
                    st.subheader("Cost by Service")
                    if not cost_by_service.empty:
                        fig_service = px.pie(cost_by_service.head(10), values='Cost', names='Service', hole=0.4)
                        st.plotly_chart(fig_service, use_container_width=True)
                    else:
                        st.info("No service cost data available.")

                with col_chart2:
                    st.subheader("Daily Cost Trend")
                    if not daily_trend.empty:
                        fig_trend = px.line(daily_trend, x='Date', y='Cost', title='Daily Cost')
                        st.plotly_chart(fig_trend, use_container_width=True)
                    else:
                        st.info("No daily trend data available.")

                # Anomalies
                if not anomalies.empty:
                    st.warning(f"Detected {len(anomalies)} cost anomalies!")
                    st.dataframe(anomalies[['Date', 'Cost', 'Z-Score']])

            with tab2:
                st.header("🤖 FinOps AI Agent Analysis")
                st.markdown("The AI agent analyzes the metrics and provides a comprehensive report.")

                if st.button("Generate AI Report"):
                    with st.spinner("Agent is analyzing your data..."):
                        agent = FinOpsAgent()
                        report = agent.generate_report(
                            total_cost=total_cost,
                            currency=currency,
                            top_services=cost_by_service,
                            waste_df=waste_df,
                            right_sizing_df=right_sizing,
                            potential_savings=potential_savings
                        )
                        st.markdown(report)

                if not waste_df.empty:
                    st.subheader("Identified Waste")
                    st.dataframe(waste_df)

                if not right_sizing.empty:
                    st.subheader("Right-Sizing Opportunities")
                    st.dataframe(right_sizing)

            with tab3:
                st.subheader("Raw Data Preview")
                st.dataframe(df.head(100))

        except Exception as e:
            st.error(f"Error processing file: {e}")
            st.error("Make sure the file format matches the selected provider.")
            # st.exception(e) # For debugging
    else:
        st.info("Please upload a CSV file to begin analysis.")
        st.markdown("### Sample Data")
        st.markdown("You can use the sample files generated in `data/` folder.")

if __name__ == "__main__":
    main()
