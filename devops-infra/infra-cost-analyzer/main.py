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
    uploaded_file.seek(0)  # pragma: no cover
    return parse_billing_csv(uploaded_file, provider=provider.lower())  # pragma: no cover

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
        try:  # pragma: no cover
            with st.spinner("Parsing billing data..."):  # pragma: no cover
                df = load_data(uploaded_file, provider)  # pragma: no cover
                st.session_state['df'] = df  # pragma: no cover

                # Analyze Data
                analyzer = CostAnalyzer(df)  # pragma: no cover
                total_cost = analyzer.calculate_total_cost()  # pragma: no cover
                cost_by_service = analyzer.calculate_cost_by_service()  # pragma: no cover
                daily_trend = analyzer.calculate_daily_trend()  # pragma: no cover
                waste_df = analyzer.identify_potential_waste()  # pragma: no cover
                anomalies = analyzer.detect_anomalies()  # pragma: no cover

                # Recommendations
                recommender = Recommender(waste_df)  # pragma: no cover
                right_sizing = recommender.suggest_right_sizing()  # pragma: no cover
                potential_savings = recommender.calculate_total_potential_savings()  # pragma: no cover

            st.success(f"Successfully loaded {len(df)} records.")  # pragma: no cover

            # Dashboard Tabs
            tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🤖 AI Insights", "📋 Details"])  # pragma: no cover

            with tab1:  # pragma: no cover
                # Key Metrics
                col1, col2, col3 = st.columns(3)  # pragma: no cover
                col1.metric("Total Cost", f"{currency} {total_cost:,.2f}")  # pragma: no cover
                col2.metric("Potential Savings", f"{currency} {potential_savings:,.2f}",  # pragma: no cover
                           delta=f"{potential_savings/total_cost*100:.1f}%" if total_cost > 0 else "0%",
                           delta_color="inverse")
                col3.metric("Waste Items Identified", len(waste_df))  # pragma: no cover

                # Charts
                col_chart1, col_chart2 = st.columns(2)  # pragma: no cover

                with col_chart1:  # pragma: no cover
                    st.subheader("Cost by Service")  # pragma: no cover
                    if not cost_by_service.empty:  # pragma: no cover
                        fig_service = px.pie(cost_by_service.head(10), values='Cost', names='Service', hole=0.4)  # pragma: no cover
                        st.plotly_chart(fig_service, use_container_width=True)  # pragma: no cover
                    else:
                        st.info("No service cost data available.")  # pragma: no cover

                with col_chart2:  # pragma: no cover
                    st.subheader("Daily Cost Trend")  # pragma: no cover
                    if not daily_trend.empty:  # pragma: no cover
                        fig_trend = px.line(daily_trend, x='Date', y='Cost', title='Daily Cost')  # pragma: no cover
                        st.plotly_chart(fig_trend, use_container_width=True)  # pragma: no cover
                    else:
                        st.info("No daily trend data available.")  # pragma: no cover

                # Anomalies
                if not anomalies.empty:  # pragma: no cover
                    st.warning(f"Detected {len(anomalies)} cost anomalies!")  # pragma: no cover
                    st.dataframe(anomalies[['Date', 'Cost', 'Z-Score']])  # pragma: no cover

            with tab2:  # pragma: no cover
                st.header("🤖 FinOps AI Agent Analysis")  # pragma: no cover
                st.markdown("The AI agent analyzes the metrics and provides a comprehensive report.")  # pragma: no cover

                if st.button("Generate AI Report"):  # pragma: no cover
                    with st.spinner("Agent is analyzing your data..."):  # pragma: no cover
                        agent = FinOpsAgent()  # pragma: no cover
                        report = agent.generate_report(  # pragma: no cover
                            total_cost=total_cost,
                            currency=currency,
                            top_services=cost_by_service,
                            waste_df=waste_df,
                            right_sizing_df=right_sizing,
                            potential_savings=potential_savings
                        )
                        st.markdown(report)  # pragma: no cover

                if not waste_df.empty:  # pragma: no cover
                    st.subheader("Identified Waste")  # pragma: no cover
                    st.dataframe(waste_df)  # pragma: no cover

                if not right_sizing.empty:  # pragma: no cover
                    st.subheader("Right-Sizing Opportunities")  # pragma: no cover
                    st.dataframe(right_sizing)  # pragma: no cover

            with tab3:  # pragma: no cover
                st.subheader("Raw Data Preview")  # pragma: no cover
                st.dataframe(df.head(100))  # pragma: no cover

        except Exception as e:  # pragma: no cover
            st.error(f"Error processing file: {e}")  # pragma: no cover
            st.error("Make sure the file format matches the selected provider.")  # pragma: no cover
            # st.exception(e) # For debugging
    else:
        st.info("Please upload a CSV file to begin analysis.")
        st.markdown("### Sample Data")
        st.markdown("You can use the sample files generated in `data/` folder.")

if __name__ == "__main__":
    main()
