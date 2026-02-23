from langchain_core.prompts import PromptTemplate

OUTLINE_PROMPT = PromptTemplate(
    input_variables=["topic", "research_summary"],
    template="""
    You are an expert content strategist.

    Topic: {topic}

    Research Summary:
    {research_summary}

    Create a comprehensive outline for a blog post on the given topic.
    The outline should include:
    1. A catchy Title.
    2. Introduction (hook, thesis statement).
    3. Main Body Sections (with subsections and key points).
    4. Conclusion (summary, call to action).

    Format the outline clearly.
    """
)

WRITING_PROMPT = PromptTemplate(
    input_variables=["topic", "outline", "research_summary"],
    template="""
    You are a professional blog post writer.

    Topic: {topic}

    Research Summary:
    {research_summary}

    Outline:
    {outline}

    Write a high-quality, SEO-optimized blog post based on the outline and research.

    Guidelines:
    - Use a professional yet engaging tone.
    - Use Markdown formatting (headers, lists, bold text).
    - Ensure the content is original and well-structured.
    - Incorporate key insights from the research.
    - Aim for a comprehensive guide (1000+ words if possible, but prioritize quality).

    Blog Post:
    """
)
