from typing import Dict, Any, Optional
import yaml
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

try:
    from ..config import config
    from ..prompts.system_prompts import TS_GENERATION_PROMPT
except ImportError:
    # Fallback for running directly or tests
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import config
    from prompts.system_prompts import TS_GENERATION_PROMPT

def generate_typescript(
    swagger_spec: Dict[str, Any],
    http_client: str = "axios",
    module_system: str = "ES Modules",
    model_name: str = "gpt-4o",
    temperature: float = 0.0,
    api_key: Optional[str] = None
) -> str:
    """
    Generates TypeScript code from a Swagger/OpenAPI spec using an LLM.

    Args:
        swagger_spec (Dict[str, Any]): The parsed Swagger spec.
        http_client (str): The HTTP client to use (axios, fetch).
        module_system (str): The module system (ES Modules, CommonJS).
        model_name (str): The LLM model name.
        temperature (float): The LLM temperature.
        api_key (Optional[str]): The OpenAI API key.

    Returns:
        str: The generated TypeScript code.
    """
    if not api_key:
        api_key = config.OPENAI_API_KEY

    if not api_key:
        raise ValueError("OpenAI API Key is required to run the agent.")

    llm = ChatOpenAI(
        model=model_name,
        temperature=temperature,
        openai_api_key=api_key
    )

    prompt = PromptTemplate.from_template(TS_GENERATION_PROMPT)

    # Convert spec to string (YAML is usually more compact for LLMs than JSON)
    spec_str = yaml.dump(swagger_spec, sort_keys=False)

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    result = chain.invoke({
        "swagger_spec": spec_str,
        "http_client": http_client,
        "module_system": module_system
    })

    # Extract code block if present
    if "```typescript" in result:
        result = result.split("```typescript")[1].split("```")[0].strip()
    elif "```ts" in result:
        result = result.split("```ts")[1].split("```")[0].strip()
    elif "```" in result:
        # Fallback for just code block
        result = result.split("```")[1].split("```")[0].strip()

    return result
