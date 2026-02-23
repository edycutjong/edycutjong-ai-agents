from langchain_core.prompts import PromptTemplate

# Main documentation generation prompt
COMPONENT_DOC_PROMPT_TEMPLATE = """
You are an expert Frontend Developer and Technical Writer.
Your task is to generate comprehensive, Storybook-style documentation for the following UI component.

Identify the framework (React, Vue, Svelte, Angular) based on the code provided.

The documentation must be in Markdown format and include the following sections:

1.  **Component Name & Description**: A clear title and a brief description of what the component does.
2.  **Props / API Reference**: A table listing all props/inputs, their types, default values, and descriptions. Extract JSDoc/TSDoc comments if available.
3.  **Usage Guidelines**: When to use this component and best practices.
4.  **Examples**:
    *   **Basic Usage**: A simple code example showing how to use the component.
    *   **Variants**: Examples of different states or configurations (e.g., primary vs secondary, sizes).
5.  **Interactive Playground (Mock)**: A section describing how the component behaves interactively.

**Component Code:**
```{language}
{code}
```

**Output Format:**
Return ONLY the Markdown content. Do not include introductory or concluding remarks.
"""

DOC_PROMPT = PromptTemplate(
    input_variables=["language", "code"],
    template=COMPONENT_DOC_PROMPT_TEMPLATE,
)

# You can add more granular prompts here if we decide to split the task later
# e.g., PROP_TABLE_PROMPT, EXAMPLE_GENERATOR_PROMPT
