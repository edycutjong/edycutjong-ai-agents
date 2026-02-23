from langchain_core.prompts import PromptTemplate

INTRODUCTION_TEMPLATE = PromptTemplate.from_template("""
You are an expert technical writer creating a tutorial for a software library.
Based on the following analysis of the library, write a compelling introduction.
It should explain what the library does, its key features, and why a developer should use it.

Library Context:
{context}

Target Audience: {difficulty}

Write the Introduction section in Markdown.
""")

PREREQUISITES_TEMPLATE = PromptTemplate.from_template("""
Based on the library analysis, list the prerequisites for using this library.
Include necessary software (Python version, etc.), dependencies, and prior knowledge required.

Library Context:
{context}

Target Audience: {difficulty}

Write the Prerequisites section in Markdown with a checklist.
""")

OUTLINE_TEMPLATE = PromptTemplate.from_template("""
Create a step-by-step outline for a {difficulty} level tutorial for the following library.
The tutorial should guide the user from setup to a working example.
Do not write the full content yet, just the section headers and a brief description of what each step covers.

Library Context:
{context}

Topic/Goal: {topic}

Write the Outline in Markdown.
""")

SECTION_CONTENT_TEMPLATE = PromptTemplate.from_template("""
Write the content for the tutorial section: "{section_title}".
Follow the outline and context provided.
Include clear explanations and code snippets where appropriate.
Ensure the tone is suitable for a {difficulty} audience.

Library Context:
{context}

Section Goal: {section_goal}

Write the content in Markdown.
""")

CODE_EXAMPLE_TEMPLATE = PromptTemplate.from_template("""
Create a complete, runnable code example for the following library demonstrating: {topic}.
The code should be well-commented and follow best practices.
If possible, include expected output as comments or a separate block.

Library Context:
{context}

Write the code example in a Markdown code block.
""")

TROUBLESHOOTING_TEMPLATE = PromptTemplate.from_template("""
Based on the library's potential pitfalls or common usage errors, generate a Troubleshooting section.
Identify 3-5 common issues a user might face and provide solutions.

Library Context:
{context}

Write the Troubleshooting section in Markdown.
""")
