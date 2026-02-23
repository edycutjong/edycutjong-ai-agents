import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent import generate_pr_description

class TestAgent(unittest.TestCase):
    def test_generate_pr_description_fallback(self):
        # Mock HAS_LANGCHAIN to False or ensure no OPENAI_API_KEY
        with patch.dict(os.environ, {}, clear=True):
             desc = generate_pr_description("pkg", [{"severity": "high", "title": "Vuln"}], "1.0.0", "1.0.1")
             self.assertIn("Security Patch: pkg", desc)
             self.assertIn("1.0.0", desc)
             self.assertIn("1.0.1", desc)

if __name__ == "__main__":
    unittest.main()
