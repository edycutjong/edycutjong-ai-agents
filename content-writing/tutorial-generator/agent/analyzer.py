import ast
from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def analyze_code_structure(code: str) -> Dict[str, Any]:
    """
    Analyzes Python code to extract classes, functions, and their docstrings.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"error": f"Syntax Error: {e}"}

    structure = {"classes": {}, "functions": {}}

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = {}
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods[item.name] = {
                        "docstring": ast.get_docstring(item),
                        "args": [arg.arg for arg in item.args.args],
                        "lineno": item.lineno
                    }
            structure["classes"][node.name] = {
                "docstring": ast.get_docstring(node),
                "methods": methods,
                "lineno": node.lineno
            }
        elif isinstance(node, ast.FunctionDef):
            structure["functions"][node.name] = {
                "docstring": ast.get_docstring(node),
                "args": [arg.arg for arg in node.args.args],
                "lineno": node.lineno
            }

    return structure

def analyze_text_content(text: str, llm) -> str:
    """
    Analyzes text documentation to extract key concepts.
    Truncates text to ~15k chars to fit in reasonable context windows if needed,
    though typically models handle more.
    """
    # Simple truncation to avoid blowing up context if user pastes a book
    safe_text = text[:15000]

    prompt = PromptTemplate.from_template(
        "Analyze the following documentation and summarize the key components, "
        "purpose, and main features of the library. Return a concise summary:\n\n{text}"
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"text": safe_text})
