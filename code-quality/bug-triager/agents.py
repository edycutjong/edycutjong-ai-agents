from crewai import Agent
from tools import search_similar_issues
from agent_config import Config

class BugTriagerAgents:
    def triage_agent(self):
        return Agent(
            role='Bug Triage Specialist',
            goal='Analyze new GitHub issues to determine appropriate labels and assignees.',
            backstory="""You are an expert bug triager for a large open source project.
            Your job is to read new issues, understand the core problem, and categorize them correctly.
            You should identify if it's a bug, enhancement, question, etc.
            You should also suggest a suitable maintainer to handle it based on the issue content.
            Use your knowledge to infer the best labels.""",
            verbose=True,
            allow_delegation=False,
            # llm=Config.OPENAI_MODEL_NAME # Assuming standard OpenAI integration is handled by environment variables or passed here if needed.
            # CrewAI automatically picks up OPENAI_API_KEY and OPENAI_MODEL_NAME usually.
            # Explicitly setting it if configured in Config:
             llm=Config.OPENAI_MODEL_NAME if Config.OPENAI_MODEL_NAME else "gpt-4"
        )

    def duplicate_checker_agent(self):
        return Agent(
            role='Duplicate Issue Detective',
            goal='Find existing issues that match the new issue.',
            backstory="""You are meticulous at finding duplicate issues.
            You use search tools to find if a similar issue has already been reported.
            If a duplicate is found, you provide the issue number and link.
            You are thorough and check for both open and closed issues.""",
            verbose=True,
            allow_delegation=False,
            tools=[search_similar_issues], # Use instance method or class method decorated with @tool
            llm=Config.OPENAI_MODEL_NAME if Config.OPENAI_MODEL_NAME else "gpt-4"
        )

    def response_agent(self):
        return Agent(
            role='Community Manager',
            goal='Draft a helpful and polite response to the issue author.',
            backstory="""You are the voice of the project.
            You welcome new contributors and provide initial guidance.
            If the issue is a bug, you thank them and mention it will be looked into.
            If it's a question, you try to point them in the right direction or wait for a maintainer.
            If it's a duplicate, you politely inform them and link the original issue.
            Your tone is always encouraging and professional.""",
            verbose=True,
            allow_delegation=False,
            llm=Config.OPENAI_MODEL_NAME if Config.OPENAI_MODEL_NAME else "gpt-4"
        )
