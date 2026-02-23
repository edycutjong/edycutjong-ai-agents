from langchain_core.prompts import PromptTemplate

PLANNING_PROMPT = """
You are a research planning assistant. Your goal is to break down a complex research topic into a step-by-step plan.
The user wants to research: "{topic}"
Depth: {depth}
Domains to focus on: {domains}

Create a list of specific sub-topics or questions that need to be researched to provide a comprehensive answer.
Return the plan as a numbered list.
"""

SEARCH_QUERY_PROMPT = """
You are a search query generator.
The user wants to research: "{sub_topic}"
Context: "{context}"

Generate {num_queries} specific search queries to find high-quality information on this sub-topic.
Return ONLY the queries, one per line.
"""

SYNTHESIS_PROMPT = """
You are a research synthesizer. You have gathered the following information:
{research_data}

Your task is to synthesize this information into a coherent section of a report about "{topic}".
Focus on: {focus}

Ensure you cite your sources (URLs) where appropriate.
Write in a clear, professional tone.
"""

FACT_CHECK_PROMPT = """
You are a fact-checking assistant. Review the following text for accuracy and consistency:
{text}

Verify the claims against general knowledge and logic. If you find any potential inaccuracies or contradictions, flag them.
If the text seems accurate, return it as is. If changes are needed, provide the corrected version.
"""

FINAL_REPORT_PROMPT = """
You are a professional report writer. Compile the following synthesized sections into a final research report on "{topic}".

Sections:
{sections}

Format the report in Markdown.
Include a table of contents, an executive summary, the main content, and a references section.
Use H1 for the title, H2 for main sections, H3 for subsections.
"""
