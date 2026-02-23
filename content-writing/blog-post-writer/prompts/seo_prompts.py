from langchain_core.prompts import PromptTemplate

SEO_OPTIMIZATION_PROMPT = PromptTemplate(
    input_variables=["topic", "content"],
    template="""
    You are an expert SEO specialist.

    Topic: {topic}

    Content:
    {content}

    Your task is to provide an SEO optimization report and metadata for the above content.

    Please provide:
    1. A list of 5-10 target keywords relevant to the content.
    2. A meta description (max 160 characters).
    3. A title tag (max 60 characters).
    4. Suggestions for improving keyword density or placement within the content.
    5. Suggestions for internal linking opportunities.

    Output Format:
    **Keywords:** [List of keywords]
    **Meta Description:** [Meta description]
    **Title Tag:** [Title tag]
    **Optimization Suggestions:**
    - [Suggestion 1]
    - [Suggestion 2]
    ...
    """
)
