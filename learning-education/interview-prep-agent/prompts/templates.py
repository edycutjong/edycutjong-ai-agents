from langchain_core.prompts import PromptTemplate

# Job Description Parsing
PARSER_TEMPLATE = """
You are an expert technical recruiter. Your task is to extract key information from a job description.

Job Description:
{job_description}

Extract the following information:
1. Job Title
2. Key Technical Skills (programming languages, frameworks, tools)
3. Required Experience Level (Junior, Mid, Senior, Lead)
4. Key Responsibilities (summary)

Return the output as a JSON object with the keys: "title", "skills", "experience_level", "responsibilities".
"""

# Question Generation
CODING_QUESTION_TEMPLATE = """
You are a senior software engineer conducting a technical interview.
Based on the following skills and experience level, generate a coding interview question.

Skills: {skills}
Experience Level: {experience_level}
Difficulty: {difficulty} (Easy, Medium, Hard)

The question should be relevant to the skills provided.
Include:
1. Problem Statement
2. Example Input/Output
3. Constraints

Return the output as a JSON object with keys: "problem_statement", "examples", "constraints".
"""

SYSTEM_DESIGN_TEMPLATE = """
You are a principal engineer conducting a system design interview.
Based on the following skills and experience level, generate a system design question.

Skills: {skills}
Experience Level: {experience_level}

The question should be appropriate for the experience level.
Include:
1. Design Prompt (e.g., "Design a URL shortener")
2. Key Requirements (Functional and Non-Functional)

Return the output as a JSON object with keys: "prompt", "requirements".
"""

BEHAVIORAL_TEMPLATE = """
You are a hiring manager conducting a behavioral interview.
Generate a behavioral question based on the STAR method (Situation, Task, Action, Result).

Focus on: {focus_area} (e.g., Conflict Resolution, Leadership, Failure, Success)

Return the output as a JSON object with keys: "question", "focus_area".
"""

# Grading
GRADING_TEMPLATE = """
You are an expert interviewer grading a candidate's response.

Question:
{question}

Candidate's Answer:
{answer}

Evaluate the answer based on:
1. Correctness/Completeness
2. Clarity/Communication
3. Optimization/Efficiency (for coding/system design)

Provide:
1. Score (1-10)
2. Detailed Feedback
3. Improved Answer (what a perfect answer would look like)

Return the output as a JSON object with keys: "score", "feedback", "improved_answer".
"""
