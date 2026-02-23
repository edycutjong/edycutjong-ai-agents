import os
import sys
import pytest
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import main

def test_main_cli_args(tmp_path):
    # Test arguments parsing and function calls
    requirements_file = tmp_path / "req.txt"
    requirements_file.write_text("My requirements")

    with patch('sys.argv', ['main.py', str(requirements_file)]), \
         patch('main.ProposalGenerator') as MockGen, \
         patch('main.create_pdf') as mock_pdf, \
         patch('main.create_markdown') as mock_md:

         mock_instance = MockGen.return_value
         mock_instance.generate_proposal.return_value = Mock(project_title="Test")

         main()

         mock_instance.generate_proposal.assert_called_with("My requirements")
         mock_pdf.assert_called()
         mock_md.assert_called()

def test_main_cli_string_args():
    # Test string input
    with patch('sys.argv', ['main.py', "My requirements string"]), \
         patch('main.ProposalGenerator') as MockGen, \
         patch('main.create_pdf') as mock_pdf, \
         patch('main.create_markdown') as mock_md:

         mock_instance = MockGen.return_value
         mock_instance.generate_proposal.return_value = Mock(project_title="Test")

         main()

         mock_instance.generate_proposal.assert_called_with("My requirements string")

def test_main_exception():
    with patch('sys.argv', ['main.py', "req"]), \
         patch('main.ProposalGenerator') as MockGen, \
         patch('sys.exit') as mock_exit:

         mock_instance = MockGen.return_value
         mock_instance.generate_proposal.side_effect = Exception("Error")

         main()

         mock_exit.assert_called_with(1)
