"""Writer agent — synthesizes research into structured reports."""

from crewai import Agent


def create_writer(verbose: bool = False) -> Agent:
    """Create a Writer agent that produces polished reports.

    Args:
        verbose: Whether to show agent reasoning.

    Returns:
        Configured Writer Agent.
    """
    return Agent(
        role="Senior Content Writer",
        goal="Transform research findings into a compelling, well-structured markdown report",
        backstory="""You are a seasoned content writer who excels at transforming 
        complex research into clear, engaging prose. You use proper markdown formatting 
        with headers, bullet points, and emphasis. Your writing is concise yet comprehensive, 
        suitable for both technical and non-technical audiences. You always include 
        an executive summary, key findings, and actionable insights.""",
        verbose=verbose,
        allow_delegation=False,
        memory=True,
    )
