import sys
import os
import unittest
from unittest.mock import MagicMock, patch
import pytest

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.reviewer import TerraformReviewer

TF_CONTENT = """
resource "aws_security_group" "allow_all" {
  name        = "allow_all"
  description = "Allow all inbound traffic"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
"""

class TestReviewer(unittest.TestCase):
    @patch("agent.reviewer.ChatOpenAI")
    def test_run_review(self, MockChatOpenAI):
        # Setup mock
        mock_llm = MagicMock()
        MockChatOpenAI.return_value = mock_llm

        # Mock the chain invocation
        # Since we use `prompt | llm | output_parser`, mocking the chain is complex because of pipe operator.
        # But TerraformReviewer sets `self.chain`.
        # We can intercept `chain.invoke` if we mock `ChatPromptTemplate` or create the chain differently.

        # A simpler way: mock `ChatOpenAI` behavior, but the chain composition happens in __init__.
        # So we mock the class before instantiation.

        # Create instance
        reviewer = TerraformReviewer(api_key="fake-key")

        # Mock the chain on the instance directly to bypass pipe logic mocking
        reviewer.chain = MagicMock()
        reviewer.chain.invoke.return_value = "Mock AI Report"

        # Run review
        result = reviewer.run_review(TF_CONTENT)

        # Assertions
        self.assertIn("security", result)
        self.assertIn("cost", result)
        self.assertIn("rules", result)
        self.assertIn("drift", result)
        self.assertEqual(result["ai_report"], "Mock AI Report")

        # Check security finding is present
        security_findings = result["security"]
        self.assertTrue(any("aws_security_group" in f["resource"] for f in security_findings))

        # Check cost
        self.assertIn("total_monthly_cost", result["cost"])

if __name__ == "__main__":
    unittest.main()
