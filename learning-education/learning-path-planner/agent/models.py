from typing import List, Optional
from pydantic import BaseModel, Field

class Resource(BaseModel):
    title: str = Field(..., description="Title of the resource")
    url: str = Field(..., description="URL of the resource")
    type: str = Field(..., description="Type of resource (e.g., Video, Article, Course, Documentation)")
    is_paid: bool = Field(False, description="Whether the resource is paid")
    cost: Optional[str] = Field(None, description="Cost of the resource if paid")

class Project(BaseModel):
    title: str = Field(..., description="Title of the project")
    description: str = Field(..., description="Description of the project")
    skills_practiced: List[str] = Field(..., description="List of skills practiced in this project")
    estimated_duration: str = Field(..., description="Estimated duration to complete the project")

class Milestone(BaseModel):
    id: int = Field(..., description="Order of the milestone")
    title: str = Field(..., description="Title of the milestone (e.g., 'Learn Python Basics')")
    description: str = Field(..., description="Detailed description of what to learn")
    skills: List[str] = Field(..., description="List of skills to be acquired")
    resources: List[Resource] = Field(..., description="List of learning resources")
    projects: List[Project] = Field(default_factory=list, description="Suggested projects for practice")
    estimated_time: str = Field(..., description="Estimated time to complete this milestone")
    is_completed: bool = Field(False, description="Whether the milestone is completed")

class LearningPath(BaseModel):
    topic: str = Field(..., description="The main topic or role of the learning path")
    user_level: str = Field(..., description="User's current skill level")
    milestones: List[Milestone] = Field(..., description="Ordered list of milestones")
    total_estimated_time: str = Field(..., description="Total estimated time for the entire path")
