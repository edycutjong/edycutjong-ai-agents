import os
import sys

# Ensure parent directory is in path to import config
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from config import Config
from prompts.templates import (
    PRESS_RELEASE_SYSTEM_PROMPT,
    PRESS_RELEASE_USER_PROMPT,
    QUOTE_GENERATION_PROMPT,
    AUDIENCE_ADAPTATION_PROMPT
)

# Optional: Try importing LangChain. If not installed (e.g. in basic verify env), mock it or fail gracefully.
try:
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
except ImportError:
    print("LangChain dependencies not found. Please install requirements.txt")
    # Define dummy classes for syntax check if needed, but we expect deps to be there.
    pass

class PressReleaseGenerator:
    def __init__(self, model_provider=None, model_name=None):
        self.model_provider = model_provider or Config.DEFAULT_MODEL_PROVIDER
        self.llm = self._initialize_llm(model_name)

    def _initialize_llm(self, model_name):
        if self.model_provider == "openai":
            api_key = Config.OPENAI_API_KEY
            if not api_key:
                print("Warning: OPENAI_API_KEY not found in environment.")
            return ChatOpenAI(
                model=model_name or Config.DEFAULT_OPENAI_MODEL,
                temperature=0.7,
                api_key=api_key
            )
        elif self.model_provider == "google":
            api_key = Config.GOOGLE_API_KEY
            if not api_key:
                print("Warning: GOOGLE_API_KEY not found in environment.")
            return ChatGoogleGenerativeAI(
                model=model_name or Config.DEFAULT_GOOGLE_MODEL,
                temperature=0.7,
                google_api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported model provider: {self.model_provider}")

    def generate_release(self, product_name, details, company_name, company_description, contact_person, media_contact, audience, tone):
        """Generates the full press release."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", PRESS_RELEASE_SYSTEM_PROMPT),
            ("user", PRESS_RELEASE_USER_PROMPT)
        ])

        chain = prompt | self.llm | StrOutputParser()

        return chain.invoke({
            "product_name": product_name,
            "details": details,
            "company_name": company_name,
            "company_description": company_description,
            "contact_person": contact_person,
            "media_contact": media_contact,
            "audience": audience,
            "tone": tone
        })

    def generate_quotes(self, details, contact_person, company_name):
        """Generates quotes for the press release."""
        prompt = ChatPromptTemplate.from_template(QUOTE_GENERATION_PROMPT)
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "details": details,
            "contact_person": contact_person,
            "company_name": company_name
        })

    def adapt_audience(self, lead_paragraph, audience):
        """Adapts the lead paragraph for a specific audience."""
        prompt = ChatPromptTemplate.from_template(AUDIENCE_ADAPTATION_PROMPT)
        chain = prompt | self.llm | StrOutputParser()
        return chain.invoke({
            "lead_paragraph": lead_paragraph,
            "audience": audience
        })
