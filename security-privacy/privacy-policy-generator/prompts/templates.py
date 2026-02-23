from langchain_core.prompts import PromptTemplate

# GDPR System Prompt
GDPR_SYSTEM_PROMPT = """You are a privacy law expert specializing in GDPR compliance.
Your task is to draft a comprehensive Privacy Policy for a software application that fully adheres to the General Data Protection Regulation (GDPR).
Use clear, transparent language suitable for a general audience but legally robust.
"""

# CCPA System Prompt
CCPA_SYSTEM_PROMPT = """You are a privacy law expert specializing in CCPA (California Consumer Privacy Act) compliance.
Your task is to draft a comprehensive Privacy Policy for a software application that fully adheres to the CCPA.
Ensure you include required disclosures about "Do Not Sell My Personal Information" rights.
"""

# Generic System Prompt
GENERIC_SYSTEM_PROMPT = """You are a privacy law expert.
Your task is to draft a standard Privacy Policy for a software application.
Focus on transparency and clarity regarding data collection and usage.
"""

# User Prompt Template
POLICY_USER_PROMPT = """Generate a {policy_type} compliant Privacy Policy based on the following findings from the codebase scan:

### Data Collection Points (PII Detected)
{pii_list}

### Third-Party Services Integration
{third_parties}

### Additional Context
- Application Name: {app_name}
- Company Name: {company_name}
- Contact Email: {contact_email}

### Requirements
The policy must include the following sections:
1. **Introduction**: Explain what this policy covers.
2. **Information We Collect**: Detail the specific data points found above.
3. **How We Use Your Information**: explain the purpose of collection.
4. **Third-Party Sharing**: Disclose the third-party services found above.
5. **Data Retention**: How long data is stored.
6. **Security Measures**: General statement on security.
7. **User Rights**: specific to {policy_type} (e.g., access, rectification, erasure).
8. **Cookies and Tracking**: if cookies were detected.
9. **Contact Us**: Use the provided contact email.

Format the output in clear Markdown.
"""
