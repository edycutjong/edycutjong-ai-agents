from typing import Dict, Any
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import sys

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import get_config

class RateLimitAnalyzer:
    def __init__(self, api_key: str = None):
        config = get_config()
        # Use provided key or fallback to config
        self.api_key = api_key or config.openai_api_key

        # Fallback if no key is provided, the UI should probably handle this check
        if not self.api_key:
             self.llm = None
        else:
            self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-4o", temperature=0.2)

    def analyze_results(self, df: pd.DataFrame, config_data: Dict[str, Any], detected_headers: Dict[str, str]) -> str:
        if self.llm is None:
            return "Error: OpenAI API Key not found. Please configure it in .env file."

        if df.empty:
            return "No data to analyze."

        # Calculate summary statistics
        total_requests = len(df)
        status_counts = df['status_code'].value_counts().to_dict()
        avg_latency = df['latency'].mean()
        max_latency = df['latency'].max()

        # Determine if/when throttling occurred
        throttled_requests = df[df['status_code'] == 429]
        throttled_count = len(throttled_requests)
        first_throttle_time = throttled_requests['relative_time'].min() if not throttled_requests.empty else None

        # Prepare context for LLM
        context = {
            "url": config_data.get("url"),
            "method": config_data.get("method"),
            "target_rps": config_data.get("rps"),
            "burst_size": config_data.get("burst_size"),
            "total_requests": total_requests,
            "status_counts": status_counts,
            "avg_latency": f"{avg_latency:.4f}s",
            "max_latency": f"{max_latency:.4f}s",
            "throttled_count": throttled_count,
            "first_throttle_time": f"{first_throttle_time:.2f}s" if first_throttle_time is not None else "N/A",
            "detected_headers": detected_headers
        }

        template = """
        You are a Senior API Engineer and Rate Limit Expert.
        Analyze the following results from a rate limit stress test on an API.

        Test Configuration:
        - URL: {url}
        - Method: {method}
        - Target RPS: {target_rps}
        - Burst Size: {burst_size}

        Results:
        - Total Requests: {total_requests}
        - Status Code Distribution: {status_counts}
        - Average Latency: {avg_latency}
        - Max Latency: {max_latency}
        - Throttled Requests (429): {throttled_count}
        - Time to First Throttle: {first_throttle_time}

        Detected Rate Limit Headers:
        {detected_headers}

        Please provide a comprehensive Markdown report including:
        1. **Executive Summary**: Brief overview of the test outcome.
        2. **Rate Limit Analysis**:
           - Identify the likely rate limit strategy (e.g., Fixed Window, Sliding Window, Token Bucket, Leaky Bucket).
           - Estimate the effective rate limit (RPS or requests/minute) based on the data.
           - Explain the behavior of the API when the limit is reached (e.g., hard 429, increased latency).
        3. **Header Interpretation**: Explain what the detected headers mean (if any).
        4. **Client-Side Strategy**: Suggest how a client application should handle these limits (e.g., backoff strategy, concurrency limits).

        Be precise and technical. If the data is inconclusive, state that clearly.
        """

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke(context)
        except Exception as e:
            return f"Error during analysis: {str(e)}"
