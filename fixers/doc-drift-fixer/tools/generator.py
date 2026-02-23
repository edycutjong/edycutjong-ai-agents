from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class DocGenerator:
    def __init__(self, api_key: Optional[str] = None):
        if not api_key:
            # Fallback or mock behavior could be implemented here,
            # but usually we want to fail or warn if no key.
            # For this specific app, we might want to allow running without AI
            # if we just want to check links, but the core "fixer" needs AI.
            self.llm = None
        else:
            self.llm = ChatOpenAI(api_key=api_key, model="gpt-4o", temperature=0)

    def generate_update(self, code_diff: str, current_doc: str) -> str:
        """Generate an updated documentation section based on code diff."""
        if not self.llm:
            return "AI features disabled (no API key)."

        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert technical writer.
            The following code changes have occurred:
            {diff}

            Here is the relevant documentation section:
            {doc}

            Please rewrite the documentation to reflect the code changes.
            Maintain the style and tone of the existing documentation.
            Output ONLY the updated documentation content.
            """
        )

        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke({"diff": code_diff, "doc": current_doc})
        except Exception as e:
            return f"Error generating update: {e}"

    def propose_new_doc(self, code_content: str, filename: str) -> str:
        """Generate new documentation for a file."""
        if not self.llm:
             return "AI features disabled (no API key)."

        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert technical writer.
            Create documentation for the following code file ({filename}):
            {code}

            Include:
            - Overview
            - Functions/Classes description
            - Usage examples

            Output in Markdown format.
            """
        )

        chain = prompt | self.llm | StrOutputParser()

        try:
            return chain.invoke({"code": code_content, "filename": filename})
        except Exception as e:
            return f"Error generating new doc: {e}"
