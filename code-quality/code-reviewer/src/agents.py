from crewai import Agent
from langchain_openai import ChatOpenAI
from agent_config import Config

class CodeReviewerAgents:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=Config.MODEL_NAME,
            temperature=0.7,
            api_key=Config.OPENAI_API_KEY
        )

    def code_reviewer_agent(self):
        return Agent(
            role='Senior Code Reviewer',
            goal='Ensure code quality, readability, and correct logic implementation.',
            backstory='You are an expert software engineer with years of experience in reviewing code. You focus on logic, potential bugs, and maintainability.',
            llm=self.llm,
            verbose=True
        )

    def report_generator_agent(self):
        return Agent(
            role='Review Summary Generator',
            goal='Synthesize multiple technical reviews into a cohesive, structured report.',
            backstory='You are an expert technical writer. You take findings from code reviewers, style checkers, and security analysts and compile them into a clear, actionable report.',
            llm=self.llm,
            verbose=True
        )

    def style_checker_agent(self):
        return Agent(
            role='Style Guide Enforcer',
            goal='Ensure code adheres to standard style guides (e.g., PEP8 for Python, ESLint rules for JS).',
            backstory='You are meticulous about code style and formatting. You ensure consistency across the codebase.',
            llm=self.llm,
            verbose=True
        )

    def security_analyst_agent(self):
        return Agent(
            role='Security Analyst',
            goal='Identify potential security vulnerabilities in the code.',
            backstory='You are a security expert. You look for injection flaws, sensitive data exposure, and other security risks.',
            llm=self.llm,
            verbose=True
        )
