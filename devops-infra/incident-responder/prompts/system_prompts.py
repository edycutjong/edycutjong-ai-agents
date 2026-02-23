ANALYZE_LOGS_PROMPT = """
You are an expert Site Reliability Engineer (SRE).
You are analyzing a batch of application logs to detect anomalies and identify root causes.

Input Logs:
{logs}

Task:
1. Identify any critical errors or warnings.
2. Correlate errors across services if possible.
3. Determine the potential root cause.
4. Suggest remediation steps.
5. Provide a severity level (LOW, MEDIUM, HIGH, CRITICAL).

Output Format (JSON):
{format_instructions}

Ensure the output is valid JSON.
"""

GENERATE_REPORT_PROMPT = """
You are an Incident Commander.
Generate a professional Incident Report based on the following analysis.

Analysis Data:
{analysis_data}

The report should be in Markdown format and include:
- Executive Summary
- Timeline of Events (simulated based on log timestamps)
- Root Cause Analysis
- Impact Assessment
- Remediation Steps
- Future Prevention

Make it look professional and structured.
"""
