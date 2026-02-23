import json
import datetime
import os

class Scheduler:
    def __init__(self, storage_file="schedule.json"):
        self.storage_file = storage_file
        self.queue = self._load_queue()

    def _load_queue(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_queue(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.queue, f, indent=4)

    def add_draft(self, topic, platform, content, image_prompt, date_time=None):
        # Generate a unique ID
        new_id = 1
        if self.queue:
            new_id = max(item["id"] for item in self.queue) + 1

        draft = {
            "id": new_id,
            "topic": topic,
            "platform": platform,
            "content": content,
            "image_prompt": image_prompt,
            "status": "Draft",  # Draft, Scheduled, Published
            "scheduled_time": date_time or datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "created_at": datetime.datetime.now().isoformat()
        }
        self.queue.append(draft)
        self.save_queue()
        return draft

    def update_status(self, draft_id, new_status):
        for draft in self.queue:
            if draft["id"] == draft_id:
                draft["status"] = new_status
                self.save_queue()
                return True
        return False

    def get_queue(self, status=None):
        if status:
            return [d for d in self.queue if d["status"] == status]
        return self.queue

    def delete_draft(self, draft_id):
        self.queue = [d for d in self.queue if d["id"] != draft_id]
        self.save_queue()
