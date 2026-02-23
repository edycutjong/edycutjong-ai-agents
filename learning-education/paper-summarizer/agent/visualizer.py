from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from prompts.templates import VISUAL_SUMMARY_PROMPT
import config

class Visualizer:
    def __init__(self, model_name=config.MODEL_NAME, temperature=config.TEMPERATURE):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=config.OPENAI_API_KEY
        )

    def generate_visual_summary(self, text: str) -> str:
        """
        Generates a Mermaid.js code snippet representing the paper's concepts.
        """
        chain = VISUAL_SUMMARY_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({"text": text})
