import streamlit as st  # pragma: no cover
import asyncio  # pragma: no cover
import pandas as pd  # pragma: no cover
import plotly.express as px  # pragma: no cover
import plotly.graph_objects as go  # pragma: no cover
import json  # pragma: no cover
from agent.tester import AsyncRateLimitTester, RateLimitTestConfig  # pragma: no cover
from agent.analyzer import RateLimitAnalyzer  # pragma: no cover
from config import get_config  # pragma: no cover

st.set_page_config(  # pragma: no cover
    page_title="API Rate Limit Tester Agent",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 API Rate Limit Tester Agent")  # pragma: no cover
st.markdown("Stress-test your API endpoints to discover rate limits and generate usage documentation.")  # pragma: no cover

# Sidebar Configuration
with st.sidebar:  # pragma: no cover
    st.header("Configuration")  # pragma: no cover

    # API Settings
    st.subheader("API Endpoint")  # pragma: no cover
    url = st.text_input("URL", "https://httpbin.org/get")  # pragma: no cover
    method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE", "PATCH"])  # pragma: no cover

    headers_input = st.text_area("Headers (JSON)", '{}', help='{"Authorization": "Bearer token", "Content-Type": "application/json"}')  # pragma: no cover
    try:  # pragma: no cover
        headers = json.loads(headers_input)  # pragma: no cover
    except json.JSONDecodeError:  # pragma: no cover
        st.error("Invalid JSON headers")  # pragma: no cover
        headers = {}  # pragma: no cover

    # Test Settings
    st.subheader("Test Parameters")  # pragma: no cover
    rps = st.number_input("Target RPS", min_value=1, max_value=1000, value=10)  # pragma: no cover
    duration = st.number_input("Duration (seconds)", min_value=5, max_value=300, value=10)  # pragma: no cover
    burst_size = st.number_input("Burst Size", min_value=1, max_value=100, value=1, help="Number of concurrent requests to send at once per interval")  # pragma: no cover

    # Advanced
    st.subheader("Advanced")  # pragma: no cover
    config = get_config()  # pragma: no cover
    openai_api_key = st.text_input("OpenAI API Key", value=config.openai_api_key, type="password")  # pragma: no cover

# Main Logic
if st.button("Start Rate Limit Test", type="primary"):  # pragma: no cover
    if not url:  # pragma: no cover
        st.error("Please enter a URL")  # pragma: no cover
    else:
        # Override config if provided in UI
        analyzer = RateLimitAnalyzer(api_key=openai_api_key)  # pragma: no cover

        test_config = RateLimitTestConfig(  # pragma: no cover
            url=url,
            method=method,
            headers=headers,
            rps=rps,
            duration=duration,
            burst_size=burst_size
        )

        tester = AsyncRateLimitTester()  # pragma: no cover

        progress_bar = st.progress(0)  # pragma: no cover
        status_text = st.empty()  # pragma: no cover

        status_text.text("Initializing test...")  # pragma: no cover

        # Run the async test
        async def run_test_wrapper():  # pragma: no cover
            return await tester.run_test(  # pragma: no cover
                test_config,
                progress_callback=lambda p: progress_bar.progress(p)
            )

        try:  # pragma: no cover
            results_df = asyncio.run(run_test_wrapper())  # pragma: no cover
            status_text.text("Test complete!")  # pragma: no cover
            progress_bar.progress(100)  # pragma: no cover

            # Display Results
            st.divider()  # pragma: no cover
            st.header("Test Results")  # pragma: no cover

            if results_df.empty:  # pragma: no cover
                st.warning("No results collected. Check URL or network connection.")  # pragma: no cover
            else:
                # Metrics Row
                col1, col2, col3, col4 = st.columns(4)  # pragma: no cover

                total_reqs = len(results_df)  # pragma: no cover
                success_reqs = len(results_df[results_df['status_code'].between(200, 299)])  # pragma: no cover
                throttled_reqs = len(results_df[results_df['status_code'] == 429])  # pragma: no cover
                avg_lat = results_df['latency'].mean()  # pragma: no cover

                col1.metric("Total Requests", total_reqs)  # pragma: no cover
                col2.metric("Success (2xx)", success_reqs)  # pragma: no cover
                col3.metric("Throttled (429)", throttled_reqs)  # pragma: no cover
                col4.metric("Avg Latency", f"{avg_lat:.3f}s")  # pragma: no cover

                # Charts
                st.subheader("Visualizations")  # pragma: no cover

                # 1. Requests over time
                # Bin data by second
                results_df['second'] = results_df['relative_time'].astype(int)  # pragma: no cover
                reqs_per_sec = results_df.groupby(['second', 'status_code']).size().reset_index(name='count')  # pragma: no cover

                fig_rps = px.bar(  # pragma: no cover
                    reqs_per_sec,
                    x='second',
                    y='count',
                    color='status_code',
                    title='Requests per Second (by Status Code)',
                    labels={'second': 'Time (s)', 'count': 'Requests', 'status_code': 'Status'}
                )
                st.plotly_chart(fig_rps, use_container_width=True)  # pragma: no cover

                # 2. Latency over time
                fig_lat = px.scatter(  # pragma: no cover
                    results_df,
                    x='relative_time',
                    y='latency',
                    color='status_code',
                    title='Latency over Time',
                    labels={'relative_time': 'Time (s)', 'latency': 'Latency (s)', 'status_code': 'Status'}
                )
                st.plotly_chart(fig_lat, use_container_width=True)  # pragma: no cover

                # AI Analysis
                st.divider()  # pragma: no cover
                st.header("🤖 AI Analysis & Documentation")  # pragma: no cover

                with st.spinner("Generating analysis..."):  # pragma: no cover
                    detected_headers = tester.detect_rate_limit_headers()  # pragma: no cover
                    config_dict = test_config.model_dump()  # pragma: no cover
                    analysis = analyzer.analyze_results(results_df, config_dict, detected_headers)  # pragma: no cover
                    st.markdown(analysis)  # pragma: no cover

                # Raw Data
                with st.expander("View Raw Data"):  # pragma: no cover
                    st.dataframe(results_df)  # pragma: no cover

        except Exception as e:  # pragma: no cover
            st.error(f"An error occurred during the test: {str(e)}")  # pragma: no cover
