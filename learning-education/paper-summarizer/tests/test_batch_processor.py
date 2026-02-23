import unittest
from unittest.mock import MagicMock, patch
from agent.batch_processor import BatchProcessor

class TestBatchProcessor(unittest.TestCase):

    @patch('agent.batch_processor.PaperSummarizer')
    @patch('agent.batch_processor.extract_text_from_pdf')
    @patch('os.listdir')
    @patch('os.path.exists')
    def test_process_directory(self, mock_exists, mock_listdir, mock_extract_text, MockPaperSummarizer):
        # Setup mocks
        mock_exists.return_value = True
        mock_listdir.return_value = ["paper1.pdf", "image.png", "paper2.pdf"]

        mock_extract_text.side_effect = ["Text of paper 1", "Text of paper 2"]

        mock_summarizer_instance = MagicMock()
        mock_summarizer_instance.summarize_all.side_effect = [{"summary": "S1"}, {"summary": "S2"}]
        MockPaperSummarizer.return_value = mock_summarizer_instance

        processor = BatchProcessor()
        results = processor.process_directory("/dummy/path")

        self.assertEqual(len(results), 2)
        self.assertIn("paper1.pdf", results)
        self.assertIn("paper2.pdf", results)
        self.assertEqual(results["paper1.pdf"], {"summary": "S1"})
        self.assertEqual(results["paper2.pdf"], {"summary": "S2"})

        mock_extract_text.assert_any_call("/dummy/path/paper1.pdf")
        mock_extract_text.assert_any_call("/dummy/path/paper2.pdf")

    @patch('agent.batch_processor.PaperSummarizer')
    @patch('os.path.exists')
    def test_process_directory_not_exists(self, mock_exists, MockPaperSummarizer):
        mock_exists.return_value = False
        processor = BatchProcessor()
        results = processor.process_directory("/nonexistent")
        self.assertEqual(results, {})

if __name__ == '__main__':
    unittest.main()
