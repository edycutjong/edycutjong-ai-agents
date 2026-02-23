from langchain_openai import ChatOpenAI
from typing import Dict, Any

from config import OPENAI_API_KEY, DEFAULT_MODEL, DEFAULT_TEMPERATURE
from prompts.seo_prompts import SEO_OPTIMIZATION_PROMPT

class SEOOptimizer:
    def __init__(self, model_name: str = DEFAULT_MODEL, temperature: float = DEFAULT_TEMPERATURE):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=OPENAI_API_KEY
        )
        self.seo_chain = SEO_OPTIMIZATION_PROMPT | self.llm

    def optimize(self, topic: str, content: str) -> Dict[str, Any]:
        """Generates SEO metadata and optimization suggestions."""
        print(f"Generating SEO metadata for topic: {topic}...")

        # Invoke SEO chain
        seo_response = self.seo_chain.invoke({
            "topic": topic,
            "content": content
        })

        seo_result = seo_response.content if hasattr(seo_response, 'content') else str(seo_response)

        return {
            "topic": topic,
            "content": content,
            "seo_report": seo_result
        }
