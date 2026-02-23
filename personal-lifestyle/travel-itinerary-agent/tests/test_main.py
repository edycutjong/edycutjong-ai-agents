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
