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
            item = item.strip()
            if item:
                if not item.startswith('.') and not item.startswith('#'):
                    # Assume class if no prefix provided by LLM, though prompt asked for it
                    selectors.add(f".{item}")
                else:
                    selectors.add(item)

        return selectors

    except Exception as e:
        logger.error(f"Error during smart scan of {filepath}: {e}")
        return set()

if __name__ == "__main__":
    # Test execution (requires API key)
    import sys
    if len(sys.argv) > 1:
        content = ""
        try:
            with open(sys.argv[1], 'r') as f:
                content = f.read()
            print(analyze_component_with_llm(content, sys.argv[1]))
        except Exception as e:
            print(f"Error: {e}")
