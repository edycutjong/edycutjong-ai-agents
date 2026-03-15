import pytest
from unittest.mock import MagicMock, patch
from main import main, export_to_markdown, export_to_pdf

def test_export_to_markdown(mocker):
    mock_file = mocker.patch("builtins.open", mocker.mock_open())
    mock_console = mocker.patch("main.console")

    export_to_markdown("Test content")

    mock_file.assert_called_with("itinerary.md", "w", encoding="utf-8")
    mock_file().write.assert_called_with("Test content")
    mock_console.print.assert_called()

def test_export_to_pdf(mocker):
    mock_fpdf = mocker.patch("main.FPDF")
    mock_pdf_instance = mock_fpdf.return_value
    mock_console = mocker.patch("main.console")

    export_to_pdf("Test content\nLine 2")

    mock_pdf_instance.add_page.assert_called_once()
    mock_pdf_instance.set_font.assert_called_with("Helvetica", size=12)
    assert mock_pdf_instance.multi_cell.call_count == 2
    mock_pdf_instance.output.assert_called_with("itinerary.pdf")
    mock_console.print.assert_called()

@patch("main.Prompt.ask")
@patch("main.TravelAgent")
def test_main_flow(MockTravelAgent, MockPrompt, mocker):
    # Setup mocks
    mock_agent_instance = MockTravelAgent.return_value
    mock_agent_instance.llm = True
    mock_agent_instance.generate_itinerary.return_value = "Mock Itinerary"

    MockPrompt.side_effect = ["Paris", "May 1-5", "n"] # dest, dates, save=no

    mocker.patch("main.console.print")
    mocker.patch("main.console.status", MagicMock())

    main()

    mock_agent_instance.generate_itinerary.assert_called_with("Paris", "May 1-5")

@patch("main.Prompt.ask")
@patch("main.TravelAgent")
def test_main_flow_save(MockTravelAgent, MockPrompt, mocker):
    mock_agent_instance = MockTravelAgent.return_value
    mock_agent_instance.llm = True
    mock_agent_instance.generate_itinerary.return_value = "Mock Itinerary"

    MockPrompt.side_effect = ["Paris", "May 1-5", "y"] # dest, dates, save=yes

    mock_md = mocker.patch("main.export_to_markdown")
    mock_pdf = mocker.patch("main.export_to_pdf")
    mocker.patch("main.console.print")
    mocker.patch("main.console.status", MagicMock())

    main()

    mock_md.assert_called_with("Mock Itinerary")
    mock_pdf.assert_called_with("Mock Itinerary")


def test_export_to_markdown_error(mocker):
    """Cover main.py lines 16-17: markdown export error."""
    mocker.patch("builtins.open", side_effect=PermissionError("denied"))
    mock_console = mocker.patch("main.console")
    export_to_markdown("Test content")
    # Should print error message
    args = mock_console.print.call_args[0][0]
    assert "Error saving Markdown" in args


def test_export_to_pdf_error(mocker):
    """Cover main.py lines 36-37: PDF export error."""
    mock_fpdf = mocker.patch("main.FPDF")
    mock_fpdf.return_value.output.side_effect = PermissionError("denied")
    mock_console = mocker.patch("main.console")
    export_to_pdf("Test content")
    args = mock_console.print.call_args[0][0]
    assert "Error saving PDF" in args


@patch("main.Prompt.ask")
@patch("main.TravelAgent")
def test_main_no_llm(MockTravelAgent, MockPrompt, mocker):
    """Cover main.py lines 51-52: no LLM available."""
    mock_agent_instance = MockTravelAgent.return_value
    mock_agent_instance.llm = None  # No API key
    MockPrompt.side_effect = ["Paris", "May 1-5"]
    mocker.patch("main.console.print")
    mocker.patch("main.console.status", MagicMock())
    main()
    # Should print error about missing API key
