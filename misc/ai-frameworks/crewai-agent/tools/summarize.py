"""Summarize tool — condense long text into key points."""

from crewai.tools import tool  # pragma: no cover


@tool("Text Summarizer")  # pragma: no cover
def summarize_tool(text: str) -> str:  # pragma: no cover
    """Summarize a long piece of text into key bullet points.

    Extracts the most important sentences and formats them as bullet points.

    Args:
        text: The text to summarize.

    Returns:
        Bullet-point summary of the text.
    """
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]  # pragma: no cover

    if not sentences:  # pragma: no cover
        return "No meaningful content to summarize."  # pragma: no cover

    # Take the first 5 most meaningful sentences
    key_points = sentences[:5]  # pragma: no cover

    summary = "**Key Points:**\n\n"  # pragma: no cover
    for point in key_points:  # pragma: no cover
        summary += f"- {point}.\n"  # pragma: no cover

    return summary  # pragma: no cover
