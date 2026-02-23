from langchain_core.prompts import PromptTemplate

ABSTRACT_METHODOLOGY_PROMPT = PromptTemplate.from_template(
    """
    You are an expert academic researcher. Read the following text from an academic paper and extract the abstract and the methodology used.

    Text:
    {text}

    Output Format:
    **Abstract:** [Extracted Abstract]

    **Methodology:** [Extracted Methodology]
    """
)

PLAIN_LANGUAGE_SUMMARY_PROMPT = PromptTemplate.from_template(
    """
    You are a science communicator. Read the following text from an academic paper and provide a summary in plain language suitable for a general audience. Avoid jargon where possible, or explain it if necessary.

    Text:
    {text}

    Plain Language Summary:
    """
)

KEY_FINDINGS_PROMPT = PromptTemplate.from_template(
    """
    You are an expert academic researcher. Read the following text from an academic paper and list the key findings and contributions.

    Text:
    {text}

    Key Findings:
    - [Finding 1]
    - [Finding 2]
    ...
    """
)

CITATIONS_PROMPT = PromptTemplate.from_template(
    """
    You are a librarian. Read the following text from an academic paper and extract the list of references or citations mentioned in the text, formatted in a standard citation style (e.g., APA).

    Text:
    {text}

    Citations:
    """
)

VISUAL_SUMMARY_PROMPT = PromptTemplate.from_template(
    """
    You are an expert in data visualization and knowledge representation. Read the following text from an academic paper and generate a Mermaid.js code snippet that represents the core concepts and their relationships (e.g., a mindmap or a flowchart).
    Do not include any markdown formatting like ```mermaid ... ```. Just the code.

    Text:
    {text}

    Mermaid Code:
    """
)

READING_LIST_PROMPT = PromptTemplate.from_template(
    """
    You are an academic advisor. Based on the topic "{topic}", suggest a list of 5 seminal or highly relevant academic papers that a student should read. Include title, author, and a brief reason for inclusion.

    Topic: {topic}

    Reading List:
    """
)
