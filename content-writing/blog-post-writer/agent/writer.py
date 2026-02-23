from langchain_openai import ChatOpenAI
from typing import Dict, Any

from config import OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE
from prompts.writer_prompts import OUTLINE_PROMPT, WRITING_PROMPT

class Writer:
    def __init__(self, model_name: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=OPENAI_API_KEY
        )
        self.outline_chain = OUTLINE_PROMPT | self.llm
        self.writing_chain = WRITING_PROMPT | self.llm

    def create_outline(self, topic: str, research_summary: str) -> str:
        """Creates a structured outline based on research."""
        print(f"Creating outline for topic: {topic}...")

        outline_response = self.outline_chain.invoke({
            "topic": topic,
            "research_summary": research_summary
        })

        outline = outline_response.content if hasattr(outline_response, 'content') else str(outline_response)
        return outline

    def write_post(self, topic: str, outline: str, research_summary: str) -> str:
        """Writes the full blog post based on the outline and research."""
        print(f"Writing blog post for topic: {topic}...")

        post_response = self.writing_chain.invoke({
            "topic": topic,
            "outline": outline,
            "research_summary": research_summary
        })

        post = post_response.content if hasattr(post_response, 'content') else str(post_response)
        return post
