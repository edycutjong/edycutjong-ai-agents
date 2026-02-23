"""Summarize tool — condense long text into key points."""

from crewai.tools import tool


@tool("Text Summarizer")
def summarize_tool(text: str) -> str:
    """Summarize a long piece of text into key bullet points.

    Extracts the most important sentences and formats them as bullet points.

    Args:
        text: The text to summarize.

    Returns:
        Bullet-point summary of the text.
    """
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]

    if not sentences:
        return "No meaningful content to summarize."

    # Take the first 5 most meaningful sentences
    key_points = sentences[:5]

    summary = "**Key Points:**\n\n"
    for point in key_points:
        summary += f"- {point}.\n"

    return summary
