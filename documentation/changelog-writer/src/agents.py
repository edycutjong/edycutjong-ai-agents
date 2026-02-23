from crewai import Agent
from langchain_openai import ChatOpenAI
import os

class ChangelogAgents:
    def __init__(self):
        # Allow overriding model via env var
        model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
        self.llm = ChatOpenAI(model=model_name, temperature=0)

    def commit_classifier(self):
        return Agent(
            role='Senior Technical Project Manager',
            goal='Classify git commits into clear categories (Features, Fixes, Chores, Documentation, Refactor, Other)',
            backstory='You are an expert at analyzing technical changes and understanding the impact of code commits. You are precise and organized.',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )

    def changelog_writer(self):
        return Agent(
            role='Senior Technical Writer',
            goal='Write a professional, engaging changelog based on categorized commits',
            backstory='You are a skilled technical writer who can translate technical jargon into clear, user-friendly release notes. You understand the importance of highlighting key features and improvements.',
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
