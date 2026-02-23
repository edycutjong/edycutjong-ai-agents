from langchain_core.prompts import PromptTemplate

SEVERITY_PROMPT = PromptTemplate.from_template(
    """
    You are an expert bug triage assistant. Analyze the following issue and assign a severity level (low, medium, high, critical) and relevant labels.

    Issue Title: {title}
    Issue Description: {description}

    Provide your response in the following JSON format:
    {{
        "severity": "severity_level",
        "labels": ["label1", "label2"],
        "reasoning": "Brief explanation of why this severity was chosen."
    }}
    """
)

ROUTING_PROMPT = PromptTemplate.from_template(
    """
    You are an expert technical project manager. Route the following issue to the correct team.
    Available Teams: {teams}

    Issue Title: {title}
    Issue Description: {description}

    Provide your response in the following JSON format:
    {{
        "team": "Team Name",
        "reasoning": "Brief explanation of why this team was chosen."
    }}
    """
)

SENTIMENT_PROMPT = PromptTemplate.from_template(
    """
    Analyze the sentiment of the following bug report. Is the user frustrated, neutral, or happy (e.g. feature request)?

    Issue Title: {title}
    Issue Description: {description}

    Provide your response in the following JSON format:
    {{
        "sentiment": "positive/neutral/negative",
        "score": 0.0 to 1.0 (where 0 is negative and 1 is positive),
        "summary": "Brief summary of the user's tone."
    }}
    """
)

FIX_SUGGESTION_PROMPT = PromptTemplate.from_template(
    """
    You are a senior software engineer. Based on the bug report below, suggest potential files or components that might need to be fixed.

    Issue Title: {title}
    Issue Description: {description}

    Provide your response in the following JSON format:
    {{
        "suggested_files": ["file1.py", "component2.js"],
        "potential_cause": "Hypothesis on what is causing the bug.",
        "fix_strategy": "High-level strategy to fix the issue."
    }}
    """
)
