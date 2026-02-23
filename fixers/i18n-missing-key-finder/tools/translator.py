from typing import Dict, List
import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class Translator:
    """
    Translates missing keys using OpenAI.
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key: str = None):
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
             # For testing/mocking purposes, we might not have a key.
             # In production, this would fail if we try to use it.
             pass
        self.llm = ChatOpenAI(model=model_name, api_key=api_key) if api_key else None

    def translate_keys(self, keys: List[str], target_lang: str, source_lang: str = "en") -> Dict[str, str]:
        """
        Translates a list of keys to the target language.
        Infers the text from the key name (e.g. 'auth.login' -> 'Login').
        """
        if not self.llm:
            raise ValueError("OpenAI API key is missing.")

        if not keys:
            return {}

        prompt = ChatPromptTemplate.from_template(
            """You are a helpful translation assistant.
            Translate the inferred meaning of the following translation keys from {source_lang} (implied) to {target_lang}.
            The keys are in dot notation or snake_case. Convert them to human-readable text.

            Example:
            Keys: ["auth.login_button", "common.welcome"]
            Output: {{"auth.login_button": "Log In", "common.welcome": "Welcome"}}

            Keys to translate:
            {keys}

            Return ONLY a valid JSON object mapping keys to translations.
            """
        )

        chain = prompt | self.llm | JsonOutputParser()

        try:
            # Chunking might be needed for many keys, but for now we do all at once (simple version)
            result = chain.invoke({
                "source_lang": source_lang,
                "target_lang": target_lang,
                "keys": json.dumps(keys)
            })
            return result
        except Exception as e:
            print(f"Translation failed: {e}")
            return {}
