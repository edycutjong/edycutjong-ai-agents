from langchain_core.prompts import PromptTemplate

ANALYSIS_TEMPLATE = """
You are an expert tech news curator for a high-quality newsletter.
Your task is to analyze the following article and provide structured metadata.

Target Topics: {topics}

Article Title: {title}
Article Content (Snippet):
{content}

---
Instructions:
1. **Relevance**: Determine if this article is relevant to the Target Topics. (Boolean)
2. **Summary**: specific, information-dense summary. Avoid clickbait phrasing. Maximum 3 sentences.
3. **Category**: Assign the single most fitting category from the Target Topics. If it doesn't fit well, use "General Tech".
4. **Score**: Rate the importance and impact of this news on a scale of 1 to 10 (10 being breaking news of the year, 1 being trivial).

Output MUST be a valid JSON object with the following schema:
{{
    "relevant": boolean,
    "summary": "string",
    "category": "string",
    "score": integer
}}
"""

ANALYSIS_PROMPT = PromptTemplate(
    input_variables=["topics", "title", "content"],
    template=ANALYSIS_TEMPLATE
)
