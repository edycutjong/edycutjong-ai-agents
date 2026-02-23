import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add the app directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.reviewer import Reviewer

class TestReviewer(unittest.TestCase):

    def test_verify_hallucinations(self):
        # Mock ChatOpenAI to avoid init error
        with patch('agent.reviewer.ChatOpenAI'):
            reviewer = Reviewer("fake-key")

        # Test case 1: Simple addition
        # @@ -1,0 +1,1 @@
        # +new line
        patch_text = "@@ -1,0 +1,1 @@\n+new line"
        # Line 1 exists.

        comments = [
            {"line": 1, "filename": "test.py", "body": "Valid"},
            {"line": 2, "filename": "test.py", "body": "Invalid"}
        ]

        verified = reviewer.verify_hallucinations(comments, patch_text)
        self.assertEqual(len(verified), 1)
        self.assertEqual(verified[0]['line'], 1)

    def test_verify_hallucinations_complex(self):
        with patch('agent.reviewer.ChatOpenAI'):
            reviewer = Reviewer("fake-key")

        # Hunk 1: lines 10-11
        # @@ -10,2 +10,2 @@
        #  context1
        # +added1
        # Hunk 2: lines 20
        # @@ -20,1 +20,1 @@
        # +added2

        patch_text = "@@ -10,2 +10,2 @@\n context1\n+added1\n@@ -20,1 +20,1 @@\n+added2"

        # Mapping:
        # @@ -10,2 +10,2 @@ -> new file starts at 10
        #  context1 -> line 10
        # +added1 -> line 11

        # @@ -20,1 +20,1 @@ -> new file starts at 20
        # +added2 -> line 20

        comments = [
            {"line": 10, "filename": "test.py"}, # Valid (context)
            {"line": 11, "filename": "test.py"}, # Valid (added)
            {"line": 12, "filename": "test.py"}, # Invalid (not in diff)
            {"line": 20, "filename": "test.py"}, # Valid (added)
        ]

        verified = reviewer.verify_hallucinations(comments, patch_text)
        lines = [c['line'] for c in verified]
        self.assertIn(10, lines)
        self.assertIn(11, lines)
        self.assertIn(20, lines)
        self.assertNotIn(12, lines)

    def test_verify_hallucinations_with_string_lines(self):
        with patch('agent.reviewer.ChatOpenAI'):
            reviewer = Reviewer("fake-key")

        patch_text = "@@ -1,0 +1,1 @@\n+line 1"
        comments = [{"line": "1", "filename": "test.py"}]

        verified = reviewer.verify_hallucinations(comments, patch_text)
        self.assertEqual(len(verified), 1)
        self.assertEqual(verified[0]['line'], 1) # Should be converted to int

if __name__ == '__main__':
    unittest.main()
