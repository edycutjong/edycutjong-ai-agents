"""Researcher agent — searches and gathers data on a topic."""

from crewai import Agent


def create_researcher(verbose: bool = False) -> Agent:
    """Create a Researcher agent that gathers information.

    Args:
        verbose: Whether to show agent reasoning.

    Returns:
        Configured Researcher Agent.
    """
    return Agent(
        role="Senior Research Analyst",
        goal="Gather comprehensive, accurate, and up-to-date information on the given topic",
        backstory="""You are an experienced research analyst with a knack for finding 
        the most relevant and credible information. You excel at identifying key trends, 
        statistics, and expert opinions. You always verify facts from multiple sources 
        and present data in a structured format with clear citations.""",
        verbose=verbose,
        allow_delegation=False,
        memory=True,
    )
