import pytest
import os
import sys

# Ensure config is importable
sys.path.append(os.path.join(os.getcwd(), 'apps/agents/design-frontend/ui-copy-reviewer'))

from agent.extractor import extract_text_from_file
from agent.reviewer import ReviewerAgent
from agent.report import ReportGenerator
import config

class TestIntegration:
    @pytest.fixture
    def mock_agent(self):
        # Force mock LLM
        original_use_mock = config.USE_MOCK_LLM
        config.USE_MOCK_LLM = True

        agent = ReviewerAgent()

        yield agent

        config.USE_MOCK_LLM = original_use_mock

    def test_full_pipeline(self, tmp_path, mock_agent):
        content = '<html><body><h1>Welcome</h1><button title="Click Me">Submit</button></body></html>'
        f = tmp_path / "test.html"
        f.write_text(content, encoding="utf-8")

        # 1. Extract
        items = extract_text_from_file(str(f))
        assert len(items) == 3

        # 2. Review
        # We need consistent behavior from mock_agent.
        # It has 6 fake responses.
        # Item 1: 6 checks -> 4 issues (Consistency, Jargon, Clarity, Voice) - based on previous analysis
        # Item 2: 6 checks -> 4 issues

        reviewed_items = mock_agent.review_items(items)
        assert len(reviewed_items) == 3

        # 3. Report
        report_gen = ReportGenerator(reviewed_items)
        report_path = tmp_path / "report.md"
        report_gen.save_report(str(report_path))

        assert report_path.exists()
        content = report_path.read_text(encoding="utf-8")
        assert "Welcome" in content
        assert "Click Me" in content
        assert "Consistency" in content
