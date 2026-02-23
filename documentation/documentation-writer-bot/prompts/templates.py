from langchain_core.prompts import PromptTemplate

MODULE_DOC_TEMPLATE = """
You are an expert technical writer. Your task is to write comprehensive documentation for the following code file.
The tone should be {tone}.

File Name: {filename}

Code:
{code}

Output Format:
1.  **Overview**: A high-level description of what the module does.
2.  **Classes**: Detailed documentation for each class, including methods, parameters, and return values.
3.  **Functions**: Detailed documentation for each function, including parameters and return values.
4.  **Usage Examples**: Provide 1-2 examples of how to use the code.

Constraints:
- Use Markdown format.
- Be concise but thorough.
- Do not include the original code in the output, only the documentation.
"""

MERMAID_TEMPLATE = """
You are an expert in creating Mermaid diagrams.
Generate a Mermaid class diagram or sequence diagram that best represents the structure and interactions of the following code.

Code:
{code}

Output Format:
Return ONLY the Mermaid code block, starting with ```mermaid and ending with ```.
Do not include any other text.
"""

API_REF_TEMPLATE = """
You are an expert technical writer.
Generate a concise API reference for the following code.

Code:
{code}

Output Format:
- List of exported classes and functions.
- Brief description for each.
- Signature for each.
"""
