from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Import templates
from prompts.templates import (
    GDPR_SYSTEM_PROMPT,
    CCPA_SYSTEM_PROMPT,
    GENERIC_SYSTEM_PROMPT,
    POLICY_USER_PROMPT
)

class PolicyGenerator:
    """
    Generates privacy policies using an LLM based on scan results.
    """
    def __init__(self, model_name: str = "gpt-4-turbo", api_key: Optional[str] = None):
        self.llm = ChatOpenAI(model=model_name, api_key=api_key)

    def generate_policy(self, scan_results: Dict[str, Any], policy_type: str = "gdpr", **kwargs) -> str:
        """
        Generates a privacy policy based on the scan results and policy type.
        """
        pii_list = ", ".join(scan_results.get("pii", []))
        third_parties = ", ".join(scan_results.get("third_parties", []))

        # Select System Prompt based on type
        if policy_type.lower() == "gdpr":
            system_template = GDPR_SYSTEM_PROMPT
        elif policy_type.lower() == "ccpa":
            system_template = CCPA_SYSTEM_PROMPT
        else:
            system_template = GENERIC_SYSTEM_PROMPT

        # User Prompt
        # Fill in placeholders in POLICY_USER_PROMPT if needed before creating prompt template?
        # No, LangChain prompt template handles placeholders.

        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("user", POLICY_USER_PROMPT)
        ])

        chain = prompt | self.llm | StrOutputParser()

        # Default Context
        context = {
            "policy_type": policy_type.upper(),
            "pii_list": pii_list if pii_list else "None detected (Please verify)",
            "third_parties": third_parties if third_parties else "None detected",
            "app_name": kwargs.get("app_name", "Your Application"),
            "company_name": kwargs.get("company_name", "Your Company"),
            "contact_email": kwargs.get("contact_email", "privacy@example.com")
        }

        return chain.invoke(context)
