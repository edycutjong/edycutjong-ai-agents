from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import ValidationError

from .models import TokenSet
try:
    from ..config import Config
    from ..prompts.extraction_prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
except ImportError:
    import sys
    import os
    # Add parent directory to path to allow importing config
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import Config
    from prompts.extraction_prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

class DesignTokenExtractor:
    def __init__(self):
        # Fallback for API key if not in env (e.g., during tests without .env)
        api_key = Config.OPENAI_API_KEY or "mock-key"

        self.llm = ChatOpenAI(
            api_key=api_key,
            model=Config.MODEL_NAME,
            temperature=Config.TEMPERATURE
        )

    def extract(self, content: str) -> TokenSet:
        """
        Extracts design tokens from the given content string.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", USER_PROMPT_TEMPLATE)
        ])

        # Use structured output for direct parsing into TokenSet
        chain = prompt | self.llm.with_structured_output(TokenSet)

        try:
            result = chain.invoke({"content": content})
            return result
        except ValidationError as e:
            # Handle validation errors gracefully
            print(f"Validation Error: {e}")
            return TokenSet(name="error", tokens=[])
        except Exception as e:
            # Handle LLM errors
            print(f"LLM Error: {e}")
            return TokenSet(name="error", tokens=[])
