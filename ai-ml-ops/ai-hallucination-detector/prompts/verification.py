from langchain.prompts import PromptTemplate

VERIFICATION_TEMPLATE = """
You are an impartial and strict fact-checker. You are provided with a claim and a source text.
Your task is to verify if the claim is supported by the source text.

Claim: {claim}

Source Text:
{source_text}

Determine the verification status of the claim based on the source text.
The status must be one of the following:
- "VERIFIED": The claim is explicitly supported by the source text.
- "CONTRADICTED": The claim is explicitly contradicted by the source text.
- "UNSUPPORTED": The claim is not found in the source text or cannot be verified from the provided context.

Also provide a confidence score (0.0 to 1.0) and a brief explanation citing the part of the source text if applicable.

Return the result in the following JSON format:
{{
    "status": "VERIFIED" | "CONTRADICTED" | "UNSUPPORTED",
    "confidence": <float>,
    "explanation": "<string>"
}}
"""

verification_prompt = PromptTemplate(
    input_variables=["claim", "source_text"],
    template=VERIFICATION_TEMPLATE,
)
