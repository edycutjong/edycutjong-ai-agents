from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from config import Config
from prompts.sop_prompts import (
    DIAGRAM_DESCRIPTION_PROMPT,
    MERMAID_CODE_PROMPT
)
import logging

logger = logging.getLogger(__name__)

class DiagramGenerator:
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.output_parser = StrOutputParser()

    def generate_mermaid_code(self, procedure_steps: str) -> str:
        """
        Generates Mermaid.js flowchart code from procedure steps.
        """
        logger.info("Generating Diagram Logic...")
        logic_chain = DIAGRAM_DESCRIPTION_PROMPT | self.llm | self.output_parser
        flowchart_logic = logic_chain.invoke({"procedure_steps": procedure_steps})

        logger.info("Converting to Mermaid Code...")
        code_chain = MERMAID_CODE_PROMPT | self.llm | self.output_parser
        mermaid_code = code_chain.invoke({"flowchart_logic": flowchart_logic})

        # Clean up code block markers if present
        mermaid_code = mermaid_code.replace("```mermaid", "").replace("```", "").strip()

        return f"```mermaid\n{mermaid_code}\n```"
