from langchain.prompts import PromptTemplate

CLAIM_EXTRACTION_TEMPLATE = """
You are an expert fact-checker. Your task is to extract factual claims from the following text.
Each claim should be a single, atomic statement that can be verified against a source document.
Ignore opinions, subjective statements, or general pleasantries.

Text to analyze:
{text}

Return the claims as a numbered list.
"""

claim_extraction_prompt = PromptTemplate(
    input_variables=["text"],
    template=CLAIM_EXTRACTION_TEMPLATE,
)
