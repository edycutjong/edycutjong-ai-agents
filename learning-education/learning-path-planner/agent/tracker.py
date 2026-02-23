import json
import os
from typing import Optional
from .models import LearningPath
from config import config

class ProgressTracker:
    def __init__(self, filepath: str = config.DATA_FILE):
        self.filepath = filepath

    def save_path(self, learning_path: LearningPath):
        with open(self.filepath, 'w') as f:
            f.write(learning_path.model_dump_json(indent=2))

    def load_path(self) -> Optional[LearningPath]:
        if not os.path.exists(self.filepath):
            return None
        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
            return LearningPath(**data)
        except Exception as e:
            print(f"Error loading path: {e}")
            return None

    def mark_milestone_complete(self, milestone_id: int) -> Optional[LearningPath]:
        path = self.load_path()
        if not path:
            return None

        for m in path.milestones:
            if m.id == milestone_id:
                m.is_completed = True
                break

        self.save_path(path)
        return path
