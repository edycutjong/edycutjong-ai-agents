from pydantic import BaseModel, Field
from typing import List, Optional

class JobDescription(BaseModel):
    title: str = Field(description="The job title")
    skills: List[str] = Field(description="Key technical skills required")
    experience_level: str = Field(description="Required experience level (e.g., Junior, Senior)")
    responsibilities: str = Field(description="Summary of key responsibilities")

class CodingQuestion(BaseModel):
    problem_statement: str = Field(description="The coding problem statement")
    examples: List[str] = Field(description="Examples of input and output")
    constraints: List[str] = Field(description="Constraints for the solution")

class SystemDesignQuestion(BaseModel):
    prompt: str = Field(description="The system design prompt")
    requirements: List[str] = Field(description="Key functional and non-functional requirements")

class BehavioralQuestion(BaseModel):
    question: str = Field(description="The behavioral interview question")
    focus_area: str = Field(description="The focus area (e.g., Leadership, Failure)")

class Evaluation(BaseModel):
    score: int = Field(description="Score from 1 to 10")
    feedback: str = Field(description="Detailed feedback on the answer")
    improved_answer: str = Field(description="An improved version of the answer")
