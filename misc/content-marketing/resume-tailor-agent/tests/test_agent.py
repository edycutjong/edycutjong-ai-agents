import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.core import ResumeTailorAgent
from agent.utils import read_pdf, create_pdf
from config import Config

class TestResumeTailorAgent:

    @pytest.fixture
    def agent(self):
        # Force mock mode for tests
        Config.MOCK_MODE = True
        return ResumeTailorAgent()

    def test_initialization(self, agent):
        assert agent.llm is None

    def test_analyze_job(self, agent):
        job_desc = "Software Engineer at Tech Co."
        result = agent.analyze_job(job_desc)
        assert isinstance(result, str)
        assert "Job Analysis (MOCK)" in result

    def test_tailor_resume(self, agent):
        resume = "My Resume"
        analysis = "Job Analysis"
        result = agent.tailor_resume(resume, analysis)
        assert isinstance(result, str)
        assert "TAILORED RESUME (MOCK)" in result

    def test_generate_cover_letter(self, agent):
        resume = "My Resume"
        job_desc = "Software Engineer"
        result = agent.generate_cover_letter(resume, job_desc)
        assert isinstance(result, str)
        assert "Dear Hiring Manager" in result

    def test_create_pdf(self, tmp_path):
        # Test PDF creation
        output_file = tmp_path / "test_output.pdf"
        text = "This is a test PDF."
        create_pdf(text, str(output_file))
        assert os.path.exists(output_file)
        assert os.path.getsize(output_file) > 0

    @patch('agent.utils.PdfReader')
    def test_read_pdf(self, mock_pdf_reader):
        # Mock PdfReader to return dummy text
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Page text"

        mock_reader_instance = MagicMock()
        mock_reader_instance.pages = [mock_page]

        mock_pdf_reader.return_value = mock_reader_instance

        content = read_pdf("dummy.pdf")
        assert content == "Page text"
