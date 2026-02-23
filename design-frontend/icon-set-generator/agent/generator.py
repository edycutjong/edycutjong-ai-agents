import os
import sys

# Ensure parent directory is in path for config import if run directly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

import logging
from typing import Optional
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

try:
    from config import config
    from prompts.system_prompts import ICON_GENERATION_SYSTEM_PROMPT
except ImportError:
    # Fallback for when running from a different context
    from apps.agents.design_frontend.icon_set_generator.config import config
    from apps.agents.design_frontend.icon_set_generator.prompts.system_prompts import ICON_GENERATION_SYSTEM_PROMPT

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IconGenerator:
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        self.provider = provider.lower()
        self.api_key = api_key
        self.llm = self._initialize_llm()
        self.prompt_template = PromptTemplate(
            template=ICON_GENERATION_SYSTEM_PROMPT,
            input_variables=["description", "style", "color"]
        )

    def _initialize_llm(self):
        try:
            if self.provider == "openai":
                api_key = self.api_key or config.OPENAI_API_KEY
                if not api_key:
                    logger.warning("OpenAI API Key not found.")
                    return None
                return ChatOpenAI(
                    api_key=api_key,
                    model="gpt-4o",
                    temperature=0.2
                )
            elif self.provider == "google":
                api_key = self.api_key or config.GOOGLE_API_KEY
                if not api_key:
                    logger.warning("Google API Key not found.")
                    return None
                return ChatGoogleGenerativeAI(
                    google_api_key=api_key,
                    model="gemini-1.5-pro",
                    temperature=0.2
                )
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM: {e}")
            return None

    def generate_icon(self, description: str, style: str = "Line", color: str = "currentColor") -> str:
        if not self.llm:
            return "Error: LLM provider not configured or failed to initialize."

        try:
            chain = self.prompt_template | self.llm | StrOutputParser()
            svg_content = chain.invoke({
                "description": description,
                "style": style,
                "color": color
            })

            cleaned_svg = self._clean_svg_output(svg_content)
            return cleaned_svg
        except Exception as e:
            logger.error(f"Error generating icon: {e}")
            return f"Error generating icon: {str(e)}"

    def _clean_svg_output(self, content: str) -> str:
        """Removes markdown code blocks and whitespace."""
        content = content.strip()

        # Remove markdown code blocks
        if "```" in content:
            lines = content.splitlines()
            new_lines = []
            in_block = False
            for line in lines:
                if line.strip().startswith("```"):
                    in_block = not in_block
                    continue
                # If we were in a block, we keep the line.
                # But sometimes LLM outputs: ```xml\n<svg>...\n```
                # We essentially just want to extract the SVG part.
                new_lines.append(line)

            # Simple heuristic: if we stripped everything, it might be just text.
            # But usually we just want to find <svg> ... </svg>
            pass

        # Robust extraction
        start_idx = content.find("<svg")
        end_idx = content.rfind("</svg>")

        if start_idx != -1 and end_idx != -1:
            return content[start_idx : end_idx + 6]

        # If no <svg> tag found, return as is (might be error message) or try to salvage
        return content
