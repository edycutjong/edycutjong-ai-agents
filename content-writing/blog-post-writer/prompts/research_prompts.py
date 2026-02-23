from langchain_core.prompts import PromptTemplate

RESEARCH_SUMMARY_PROMPT = PromptTemplate(
    input_variables=["topic", "search_results"],
    template="""
    You are an expert researcher. Your goal is to provide a comprehensive summary of the given topic based on the search results provided.

    Topic: {topic}

    Search Results:
    {search_results}

    Please provide a structured summary that includes:
    1. Key concepts and definitions.
    2. Current trends and statistics (if available).
    3. Different perspectives or arguments related to the topic.
    4. Notable examples or case studies.
    5. References to specific sources (URLs) where possible.

    Ensure the summary is detailed enough for a content writer to create a high-quality blog post.
    """
)
