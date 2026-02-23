import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import ValidationError

from config import config
from .models import LearningPath, Milestone, Resource, Project
from prompts.system import PLANNER_SYSTEM_PROMPT, ADJUSTMENT_SYSTEM_PROMPT

class LearningPathPlanner:
    def __init__(self):
        self.mock_mode = config.MOCK_MODE
        if not self.mock_mode and config.OPENAI_API_KEY:
            self.llm = ChatOpenAI(
                model=config.MODEL_NAME,
                api_key=config.OPENAI_API_KEY,
                temperature=0.7
            )
            self.parser = JsonOutputParser(pydantic_object=LearningPath)
        else:
            self.mock_mode = True

    def generate_path(self, topic: str, user_level: str, additional_info: str = "") -> LearningPath:
        if self.mock_mode:
            return self._mock_generate_path(topic, user_level)

        prompt = ChatPromptTemplate.from_messages([
            ("system", PLANNER_SYSTEM_PROMPT),
            ("user", "Create a learning path for a {topic} role. My current level is {user_level}. Additional info: {additional_info}")
        ])

        chain = prompt | self.llm | self.parser

        try:
            result = chain.invoke({
                "topic": topic,
                "user_level": user_level,
                "additional_info": additional_info
            })
            # Ensure the result is a dict before passing to Pydantic
            if isinstance(result, str):
                result = json.loads(result)
            return LearningPath(**result)
        except Exception as e:
            print(f"Error generating path: {e}")
            return self._mock_generate_path(topic, user_level)

    def adjust_path(self, current_path: LearningPath, feedback: str) -> LearningPath:
        if self.mock_mode:
            # For mock mode, just return the current path with a simulated update
            # We can maybe toggle a milestone if completed, but that's done in tracker.
            # Here we are replanning.
            print("Mock mode: Adjusting path (no-op)")
            return current_path

        prompt = ChatPromptTemplate.from_messages([
            ("system", ADJUSTMENT_SYSTEM_PROMPT),
            ("user", "Here is the feedback: {feedback}")
        ])

        chain = prompt | self.llm | self.parser

        try:
            result = chain.invoke({
                "current_path": current_path.model_dump_json(),
                "user_feedback": feedback
            })
            if isinstance(result, str):
                result = json.loads(result)
            return LearningPath(**result)
        except Exception as e:
            print(f"Error adjusting path: {e}")
            return current_path

    def _mock_generate_path(self, topic: str, user_level: str) -> LearningPath:
        # Return a static dummy path for testing/demo
        return LearningPath(
            topic=topic,
            user_level=user_level,
            total_estimated_time="Mocked 4 weeks",
            milestones=[
                Milestone(
                    id=1,
                    title="Mock Milestone 1: Basics",
                    description="Learn the fundamentals.",
                    skills=["Basic Skill 1", "Basic Skill 2"],
                    resources=[
                        Resource(title="Official Docs", url="https://example.com", type="Documentation", is_paid=False),
                        Resource(title="YouTube Tutorial", url="https://youtube.com", type="Video", is_paid=False)
                    ],
                    projects=[
                        Project(
                            title="Hello World Project",
                            description="Build a simple app.",
                            skills_practiced=["Basic Skill 1"],
                            estimated_duration="2 days"
                        )
                    ],
                    estimated_time="1 week",
                    is_completed=False
                ),
                Milestone(
                    id=2,
                    title="Mock Milestone 2: Advanced",
                    description="Go deeper.",
                    skills=["Advanced Skill 1"],
                    resources=[],
                    estimated_time="2 weeks",
                    is_completed=False
                )
            ]
        )
