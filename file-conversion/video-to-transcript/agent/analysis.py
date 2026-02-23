from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Use relative import for flexibility when running as a module or script
# This assumes that 'prompts' is a sibling package to 'agent' in the python path
try:
    from prompts.transcript_prompts import SUMMARY_TEMPLATE, CHAPTERS_TEMPLATE
except ImportError:
    # If running as a package, try parent relative import (though tricky with hyphens)
    # Or just assume the top-level package is in path
    from apps.agents.file_conversion.video_to_transcript.prompts.transcript_prompts import SUMMARY_TEMPLATE, CHAPTERS_TEMPLATE

class ContentAnalyzer:
    def __init__(self, api_key: str, model_name: str = "gpt-4o-mini"):
        if not api_key:
             raise ValueError("API Key is required for ContentAnalyzer")

        self.llm = ChatOpenAI(api_key=api_key, model=model_name, temperature=0.3)

        self.summary_prompt = PromptTemplate(template=SUMMARY_TEMPLATE, input_variables=["transcript"])
        self.chapters_prompt = PromptTemplate(template=CHAPTERS_TEMPLATE, input_variables=["transcript"])

        self.summary_chain = self.summary_prompt | self.llm | StrOutputParser()
        self.chapters_chain = self.chapters_prompt | self.llm | StrOutputParser()

    def summarize(self, transcript: str) -> str:
        return self.summary_chain.invoke({"transcript": transcript})

    def generate_chapters(self, transcript: str) -> str:
        return self.chapters_chain.invoke({"transcript": transcript})
