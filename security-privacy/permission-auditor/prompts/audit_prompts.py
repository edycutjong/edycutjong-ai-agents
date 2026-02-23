from langchain_core.prompts import PromptTemplate

PERMISSION_ANALYSIS_PROMPT = """
You are a Security & Privacy Permission Auditor. Your job is to analyze the permissions requested by an application and determine if they are necessary based on the application's description.

**App Description:**
{app_description}

**Platform:** {platform}

**Requested Permissions:**
{permissions}

**Instructions:**
1. Analyze each permission.
2. Determine if the permission is justified by the App Description.
3. Identify permissions that seem excessive or risky.
4. Assign a Risk Level (Low, Medium, High, Critical) to the overall permission set.
5. Provide a specific suggestion for each excessive permission (e.g., "Remove this permission", "Use a less invasive API").

**Output Format:**
Return a JSON object with the following structure:
{{
    "risk_level": "High",
    "summary": "Short summary of findings.",
    "analysis": [
        {{
            "permission": "PERMISSION_NAME",
            "status": "Justified" | "Excessive" | "Unknown",
            "reason": "Why it is justified or excessive.",
            "suggestion": "Recommendation."
        }}
    ]
}}
"""

JUSTIFICATION_DOC_PROMPT = """
You are a technical writer creating a Permission Justification Document for an app store submission (Google Play / Apple App Store).

**App Description:**
{app_description}

**Permissions to Justify:**
{permissions}

**Instructions:**
Write a clear, professional justification for each permission. Explain WHY the app needs it to function. If a permission is critical, emphasize the user benefit.

**Output:**
A Markdown formatted document.
"""
