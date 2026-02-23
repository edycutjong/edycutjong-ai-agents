import sys
import os
import unittest
from unittest.mock import MagicMock, patch

# Add the app directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.trends import TrendMonitor
from agent.generator import ContentGenerator
from agent.scheduler import Scheduler
from agent.engagement import EngagementManager

class TestAgentComponents(unittest.TestCase):

    def test_trend_monitor_defaults(self):
        monitor = TrendMonitor()
        trends = monitor.get_trends()
        self.assertTrue(isinstance(trends, list))
        self.assertTrue(len(trends) > 0)
        self.assertIn("topic", trends[0])

    @patch.dict(os.environ, {"OPENAI_API_KEY": ""})
    def test_content_generator_mock(self):
        # Test without API key (Mock mode)
        gen = ContentGenerator(api_key=None)
        draft = gen.generate_draft("Test Topic", "Twitter")
        self.assertIn("[MOCK DRAFT]", draft)
        self.assertIn("Test Topic", draft)

        image_prompt = gen.generate_image_prompt("Test Topic", "Instagram")
        self.assertIn("[MOCK IMAGE PROMPT]", image_prompt)

    def test_scheduler_add_and_retrieve(self):
        # Use a temporary file for testing
        test_file = "test_schedule.json"
        if os.path.exists(test_file):
            os.remove(test_file)

        scheduler = Scheduler(storage_file=test_file)

        # Test adding
        scheduler.add_draft("Topic 1", "Twitter", "Content 1", "Prompt 1")
        queue = scheduler.get_queue("Draft")
        self.assertEqual(len(queue), 1)
        self.assertEqual(queue[0]["topic"], "Topic 1")

        # Test updating
        post_id = queue[0]["id"]
        scheduler.update_status(post_id, "Published")

        published = scheduler.get_queue("Published")
        self.assertEqual(len(published), 1)
        self.assertEqual(published[0]["status"], "Published")

        # Test ID uniqueness after deletion
        scheduler.add_draft("Topic 2", "LinkedIn", "Content 2", "Prompt 2")
        queue = scheduler.get_queue("Draft")
        draft2 = queue[0]
        self.assertEqual(draft2["id"], 2) # Assuming first was ID 1

        scheduler.delete_draft(post_id) # Delete ID 1
        scheduler.add_draft("Topic 3", "Instagram", "Content 3", "Prompt 3")
        queue = scheduler.get_queue("Draft")
        # Should have ID 2 and ID 3
        ids = [d["id"] for d in queue]
        self.assertIn(3, ids)
        self.assertNotIn(1, ids)

        # Cleanup
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_engagement_manager_reply(self):
        # Mock generator
        gen_mock = MagicMock()
        gen_mock.llm = None
        gen_mock.brand_voice = "Friendly"

        engagement = EngagementManager(gen_mock)
        comment = {"user": "User1", "text": "Great post!", "platform": "Twitter", "sentiment": "Positive"}

        reply = engagement.suggest_reply(comment)
        self.assertIn("Thanks", reply)

if __name__ == '__main__':
    unittest.main()
