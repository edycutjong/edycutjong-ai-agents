from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from prompts.templates import READING_LIST_PROMPT
import config

class ReadingListGenerator:
    def __init__(self, model_name=config.MODEL_NAME, temperature=config.TEMPERATURE):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=config.OPENAI_API_KEY
        )

    def generate_reading_list(self, topic: str) -> str:
        """
        Generates a reading list based on a topic.
        """
        chain = READING_LIST_PROMPT | self.llm | StrOutputParser()
        return chain.invoke({"topic": topic})
