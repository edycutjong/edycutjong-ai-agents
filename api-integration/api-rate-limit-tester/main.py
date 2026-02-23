import streamlit as st
import asyncio
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from agent.tester import AsyncRateLimitTester, RateLimitTestConfig
from agent.analyzer import RateLimitAnalyzer
from config import get_config

st.set_page_config(
    page_title="API Rate Limit Tester Agent",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 API Rate Limit Tester Agent")
st.markdown("Stress-test your API endpoints to discover rate limits and generate usage documentation.")

# Sidebar Configuration
with st.sidebar:
    st.header("Configuration")

    # API Settings
    st.subheader("API Endpoint")
    url = st.text_input("URL", "https://httpbin.org/get")
    method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE", "PATCH"])

    headers_input = st.text_area("Headers (JSON)", '{}', help='{"Authorization": "Bearer token", "Content-Type": "application/json"}')
    try:
        headers = json.loads(headers_input)
    except json.JSONDecodeError:
        st.error("Invalid JSON headers")
        headers = {}

    # Test Settings
    st.subheader("Test Parameters")
    rps = st.number_input("Target RPS", min_value=1, max_value=1000, value=10)
    duration = st.number_input("Duration (seconds)", min_value=5, max_value=300, value=10)
    burst_size = st.number_input("Burst Size", min_value=1, max_value=100, value=1, help="Number of concurrent requests to send at once per interval")

    # Advanced
    st.subheader("Advanced")
    config = get_config()
    openai_api_key = st.text_input("OpenAI API Key", value=config.openai_api_key, type="password")

# Main Logic
if st.button("Start Rate Limit Test", type="primary"):
    if not url:
        st.error("Please enter a URL")
    else:
        # Override config if provided in UI
        analyzer = RateLimitAnalyzer(api_key=openai_api_key)

        test_config = RateLimitTestConfig(
            url=url,
            method=method,
            headers=headers,
            rps=rps,
            duration=duration,
            burst_size=burst_size
        )

        tester = AsyncRateLimitTester()

        progress_bar = st.progress(0)
        status_text = st.empty()

        status_text.text("Initializing test...")

        # Run the async test
        async def run_test_wrapper():
            return await tester.run_test(
                test_config,
                progress_callback=lambda p: progress_bar.progress(p)
            )

        try:
            results_df = asyncio.run(run_test_wrapper())
            status_text.text("Test complete!")
            progress_bar.progress(100)

            # Display Results
            st.divider()
            st.header("Test Results")

            if results_df.empty:
                st.warning("No results collected. Check URL or network connection.")
            else:
                # Metrics Row
                col1, col2, col3, col4 = st.columns(4)

                total_reqs = len(results_df)
                success_reqs = len(results_df[results_df['status_code'].between(200, 299)])
                throttled_reqs = len(results_df[results_df['status_code'] == 429])
                avg_lat = results_df['latency'].mean()

                col1.metric("Total Requests", total_reqs)
                col2.metric("Success (2xx)", success_reqs)
                col3.metric("Throttled (429)", throttled_reqs)
                col4.metric("Avg Latency", f"{avg_lat:.3f}s")

                # Charts
                st.subheader("Visualizations")

                # 1. Requests over time
                # Bin data by second
                results_df['second'] = results_df['relative_time'].astype(int)
                reqs_per_sec = results_df.groupby(['second', 'status_code']).size().reset_index(name='count')

                fig_rps = px.bar(
                    reqs_per_sec,
                    x='second',
                    y='count',
                    color='status_code',
                    title='Requests per Second (by Status Code)',
                    labels={'second': 'Time (s)', 'count': 'Requests', 'status_code': 'Status'}
                )
                st.plotly_chart(fig_rps, use_container_width=True)

                # 2. Latency over time
                fig_lat = px.scatter(
                    results_df,
                    x='relative_time',
                    y='latency',
                    color='status_code',
                    title='Latency over Time',
                    labels={'relative_time': 'Time (s)', 'latency': 'Latency (s)', 'status_code': 'Status'}
                )
                st.plotly_chart(fig_lat, use_container_width=True)

                # AI Analysis
                st.divider()
                st.header("🤖 AI Analysis & Documentation")

                with st.spinner("Generating analysis..."):
                    detected_headers = tester.detect_rate_limit_headers()
                    config_dict = test_config.model_dump()
                    analysis = analyzer.analyze_results(results_df, config_dict, detected_headers)
                    st.markdown(analysis)

                # Raw Data
                with st.expander("View Raw Data"):
                    st.dataframe(results_df)

        except Exception as e:
            st.error(f"An error occurred during the test: {str(e)}")
