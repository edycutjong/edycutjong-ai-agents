"""Crew definition — orchestrates agents and tasks for report generation."""

import os
from crewai import Crew, Task, Process
from dotenv import load_dotenv

from agents import create_researcher, create_writer, create_editor

load_dotenv()


def create_research_crew(topic: str, verbose: bool = False) -> Crew:
    """Create a research crew with 3 agents and sequential tasks.

    Args:
        topic: The research topic.
        verbose: Whether to show agent reasoning.

    Returns:
        Configured Crew instance ready to kick off.
    """
    # Create agents
    researcher = create_researcher(verbose=verbose)
    writer = create_writer(verbose=verbose)
    editor = create_editor(verbose=verbose)

    # Define tasks
    research_task = Task(
        description=f"""Research the topic: '{topic}'.
        
        Your deliverables:
        1. Identify 5-7 key aspects or subtopics
        2. Gather relevant statistics and data points
        3. Find expert opinions and notable quotes
        4. Identify current trends and future predictions
        5. Note any controversies or differing viewpoints
        
        Organize your findings in a structured format with clear headings.""",
        expected_output="A comprehensive research document with organized findings, statistics, and citations.",
        agent=researcher,
    )

    writing_task = Task(
        description=f"""Using the research findings, write a comprehensive markdown report on '{topic}'.
        
        Report structure:
        1. **Executive Summary** (2-3 sentences)
        2. **Key Findings** (bullet points)
        3. **Detailed Analysis** (organized by subtopic)
        4. **Trends & Predictions** 
        5. **Actionable Insights**
        6. **Conclusion**
        
        Use proper markdown formatting: headers, bold, bullet points, and > blockquotes for quotes.""",
        expected_output="A well-structured markdown report with all required sections, proper formatting, and clear insights.",
        agent=writer,
        context=[research_task],
    )

    editing_task = Task(
        description="""Review and polish the report. Check for:
        
        1. **Accuracy** — Verify claims are supported by the research
        2. **Clarity** — Simplify complex sentences
        3. **Grammar** — Fix any grammatical errors
        4. **Flow** — Ensure logical progression between sections
        5. **Formatting** — Consistent markdown formatting
        6. **Completeness** — All sections are adequately covered
        
        Output the final, publication-ready markdown report.""",
        expected_output="A polished, publication-ready markdown report with all corrections applied.",
        agent=editor,
        context=[research_task, writing_task],
    )

    # Create and return crew
    return Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=verbose,
    )


def run_crew(topic: str, verbose: bool = False) -> str:
    """Run the research crew and return the final report.

    Args:
        topic: The research topic.
        verbose: Whether to show agent reasoning.

    Returns:
        The final markdown report as a string.
    """
    crew = create_research_crew(topic, verbose=verbose)
    result = crew.kickoff()
    return str(result)
