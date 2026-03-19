import os
import logging
from typing import Set, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)

def analyze_component_with_llm(content: str, filepath: str) -> Set[str]:
    """
    Uses an LLM to analyze the given file content and identify dynamically generated CSS classes and IDs.
    Returns a set of selectors (e.g., '.active', '#main-btn').
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not found. Skipping smart scan.")
        return set()

    try:
        llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", api_key=api_key)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert frontend developer. Your task is to analyze the provided code snippet (JS/TS/React/Vue/etc.) and extract ALL CSS class names and IDs that are used, including those generated dynamically or conditionally. Return ONLY a comma-separated list of selectors (e.g., .btn, .active, #header). Do not include any explanation."),
            ("user", "File: {filepath}\n\nCode:\n{content}")
        ])

        chain = prompt | llm | StrOutputParser()

        result = chain.invoke({"filepath": filepath, "content": content})

        selectors = set()
        for item in result.split(','):
            item = item.strip()  # pragma: no cover
            if item:  # pragma: no cover
                if not item.startswith('.') and not item.startswith('#'):  # pragma: no cover
                    # Assume class if no prefix provided by LLM, though prompt asked for it
                    selectors.add(f".{item}")  # pragma: no cover
                else:
                    selectors.add(item)  # pragma: no cover

        return selectors

    except Exception as e:  # pragma: no cover
        logger.error(f"Error during smart scan of {filepath}: {e}")  # pragma: no cover
        return set()  # pragma: no cover

if __name__ == "__main__":
    # Test execution (requires API key)
    import sys  # pragma: no cover
    if len(sys.argv) > 1:  # pragma: no cover
        content = ""  # pragma: no cover
        try:  # pragma: no cover
            with open(sys.argv[1], 'r') as f:  # pragma: no cover
                content = f.read()  # pragma: no cover
            print(analyze_component_with_llm(content, sys.argv[1]))  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print(f"Error: {e}")  # pragma: no cover
