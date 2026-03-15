"""Prompts for incident response."""

SYSTEM_PROMPT = """You are an expert SRE and incident response engineer.
Analyze log files, detect patterns, diagnose issues, and suggest remediation.
Provide clear, actionable recommendations."""

DIAGNOSE_PROMPT = """Analyze these log entries and provide:
1. Summary of issues found
2. Root cause analysis
3. Severity assessment
4. Recommended remediation steps

Logs:
```
{log_content}
```"""

REPORT_PROMPT = """Generate a professional post-mortem report from this incident data:

{incident_data}

Include: timeline, root cause, impact, resolution, and action items."""
