import unittest
from unittest.mock import patch, MagicMock
import sys
import io
import json
import os
from main import main

class TestMain(unittest.TestCase):

    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.extract_text_from_pdf')
    @patch('main.PaperSummarizer')
    @patch('main.Visualizer')
    @patch('builtins.print')
    def test_main_summarize(self, mock_print, MockVisualizer, MockPaperSummarizer, mock_extract_text, mock_args):
        mock_args.return_value = MagicMock(command="summarize", filepath="paper.pdf", visual=True)
        mock_extract_text.return_value = "Extracted Text"

        mock_summarizer_instance = MagicMock()
        mock_summarizer_instance.summarize_all.return_value = {"summary": "Done"}
        MockPaperSummarizer.return_value = mock_summarizer_instance

        mock_visualizer_instance = MagicMock()
        mock_visualizer_instance.generate_visual_summary.return_value = "graph TD\n A-->B"
        MockVisualizer.return_value = mock_visualizer_instance

        # Mock os.path.exists
        with patch('os.path.exists', return_value=True):
            main()

        mock_extract_text.assert_called_with("paper.pdf")
        mock_summarizer_instance.summarize_all.assert_called_with("Extracted Text")
        mock_visualizer_instance.generate_visual_summary.assert_called_with("Extracted Text")

        # Check if print was called with JSON
        # This is tricky because print is called multiple times.
        # We can assert that print was called with the summary.
        # json.dumps({"summary": "Done"}, indent=2) -> '{\n  "summary": "Done"\n}'
        mock_print.assert_any_call('{\n  "summary": "Done"\n}')
        mock_print.assert_any_call("graph TD\n A-->B")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.BatchProcessor')
    @patch('builtins.print')
    def test_main_batch(self, mock_print, MockBatchProcessor, mock_args):
        mock_args.return_value = MagicMock(command="batch", directory="papers")

        mock_processor_instance = MagicMock()
        mock_processor_instance.process_directory.return_value = {"paper.pdf": {"summary": "S1"}}
        MockBatchProcessor.return_value = mock_processor_instance

        with patch('builtins.open', new_callable=MagicMock) as mock_open:
            main()

        mock_processor_instance.process_directory.assert_called_with("papers")
        mock_print.assert_any_call('{\n  "paper.pdf": {\n    "summary": "S1"\n  }\n}')
        mock_open.assert_called() # Should open file to write

    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.ReadingListGenerator')
    @patch('builtins.print')
    def test_main_reading_list(self, mock_print, MockReadingListGenerator, mock_args):
        mock_args.return_value = MagicMock(command="reading-list", topic="AI")

        mock_generator_instance = MagicMock()
        mock_generator_instance.generate_reading_list.return_value = "List of papers"
        MockReadingListGenerator.return_value = mock_generator_instance

        main()

        mock_generator_instance.generate_reading_list.assert_called_with("AI")
        mock_print.assert_any_call("List of papers")


    @patch('argparse.ArgumentParser.parse_args')
    @patch('builtins.print')
    def test_main_summarize_file_not_found(self, mock_print, mock_args):
        mock_args.return_value = MagicMock(command="summarize", filepath="nonexistent.pdf")
        with patch('os.path.exists', return_value=False):
            main()
        mock_print.assert_any_call("File not found: nonexistent.pdf")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.extract_text_from_pdf')
    @patch('builtins.print')
    def test_main_summarize_extract_failure(self, mock_print, mock_extract_text, mock_args):
        mock_args.return_value = MagicMock(command="summarize", filepath="paper.pdf")
        mock_extract_text.return_value = None
        with patch('os.path.exists', return_value=True):
            main()
        mock_print.assert_any_call("Failed to extract text.")

    @patch('argparse.ArgumentParser.parse_args')
    @patch('main.BatchProcessor')
    @patch('builtins.print')
    def test_main_batch_save_error(self, mock_print, MockBatchProcessor, mock_args):
        mock_args.return_value = MagicMock(command="batch", directory="papers")
        mock_processor_instance = MagicMock()
        mock_processor_instance.process_directory.return_value = {"paper.pdf": {"summary": "S1"}}
        MockBatchProcessor.return_value = mock_processor_instance
        with patch('builtins.open', side_effect=Exception("Permission denied")):
            main()
        mock_print.assert_any_call("Error saving results: Permission denied")

    @patch('sys.argv', ['main.py'])
    @patch('argparse.ArgumentParser.print_help')
    def test_main_no_args_or_invalid(self, mock_print_help):
        main()
        mock_print_help.assert_called_once()

def test_main_block():
    """Test the if __name__ == '__main__' block."""
    with patch('sys.argv', ['main.py', 'reading-list', 'AI']):
        with patch('main.ReadingListGenerator') as MockGen:
            mock_instance = MagicMock()
            mock_instance.generate_reading_list.return_value = "AI papers"
            MockGen.return_value = mock_instance
            with patch('builtins.print'):
                main()
