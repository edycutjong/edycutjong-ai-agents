from typing import List, Optional
from pydantic import BaseModel, Field

class ScopeItem(BaseModel):
    title: str = Field(description="Title of the scope item")
    description: str = Field(description="Detailed description of the scope item")

class Milestone(BaseModel):
    name: str = Field(description="Name of the milestone")
    date: str = Field(description="Estimated date or duration (e.g., 'Week 2')")
    description: str = Field(description="Description of what is achieved")

class BudgetItem(BaseModel):
    item: str = Field(description="Name of the budget item or service")
    cost: float = Field(description="Estimated cost")
    description: Optional[str] = Field(None, description="Explanation of the cost")

class Deliverable(BaseModel):
    name: str = Field(description="Name of the deliverable")
    format: str = Field(description="Format of the deliverable (e.g., 'PDF Report', 'Source Code')")
    acceptance_criteria: str = Field(description="Criteria for accepting the deliverable")

class Risk(BaseModel):
    description: str = Field(description="Description of the risk")
    severity: str = Field(description="Severity level: Low, Medium, High")
    mitigation: str = Field(description="Plan to mitigate the risk")

class Proposal(BaseModel):
    project_title: str = Field(description="A catchy and professional title for the project")
    executive_summary: str = Field(description="A high-level summary of the proposal")
    scope_of_work: List[ScopeItem] = Field(description="List of items in the scope of work")
    timeline: List[Milestone] = Field(description="Project timeline with milestones")
    budget: List[BudgetItem] = Field(description="Budget breakdown")
    deliverables: List[Deliverable] = Field(description="List of deliverables")
    risks: List[Risk] = Field(description="Risk assessment and mitigation strategies")
