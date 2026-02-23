import base64
from typing import Optional
import os
import sys

# Add the project root to sys.path to ensure config can be imported
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from config import config
from prompts.system_prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

class AltTextGenerator:
    def __init__(self, provider: str = None, model: str = None):
        self.provider = provider or config.DEFAULT_PROVIDER
        self.model = model or (config.OPENAI_MODEL if self.provider == "openai" else config.GOOGLE_MODEL)

        if self.provider == "openai":
            if not config.OPENAI_API_KEY:
                 # Fallback or raise error, but let's assume valid config if provider is selected
                 pass
            self.llm = ChatOpenAI(
                model=self.model,
                temperature=0.2,
                max_tokens=100,
                api_key=config.OPENAI_API_KEY
            )
        elif self.provider == "google":
            if not config.GEMINI_API_KEY:
                 pass
            self.llm = ChatGoogleGenerativeAI(
                model=self.model,
                temperature=0.2,
                max_output_tokens=100,
                api_key=config.GEMINI_API_KEY
            )
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def generate_alt_text(self, image_data: str, context: str = "") -> str:
        """
        Generates alt text for an image.
        image_data: base64 encoded string of the image.
        context: text context surrounding the image.
        """
        if not image_data:
            return "Error: Image data missing."

        prompt_text = USER_PROMPT_TEMPLATE.format(context=context, src="[Image]")

        if self.provider == "openai":
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=[
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            },
                        },
                    ]
                )
            ]
        elif self.provider == "google":
            # Google Generative AI (Gemini) handles images differently in LangChain
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(
                    content=[
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{image_data}"
                        },
                    ]
                )
            ]

        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            return f"Error generating alt text: {e}"
