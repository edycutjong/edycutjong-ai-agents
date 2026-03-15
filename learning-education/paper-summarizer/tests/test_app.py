import os
import runpy
from unittest.mock import MagicMock, patch

def run_app_with_mocks(mock_st):
    mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]
    with patch.dict('sys.modules', {'streamlit': mock_st}):
        runpy.run_path('app.py', run_name='__main__')

@patch('app.st')
def test_app_tab1_success(mock_st):
    mock_file = MagicMock()
    mock_file.getvalue.return_value = b"dummy pdf content"
    
    mock_st.file_uploader.return_value = mock_file
    mock_st.button.side_effect = lambda name: name == "Generate Summary"
    
    with patch('agent.pdf_parser.extract_text_from_pdf', return_value="dummy text") as mock_extract, \
         patch('agent.summarizer.PaperSummarizer') as MockSummarizer, \
         patch('agent.visualizer.Visualizer') as MockVisualizer:
        
        mock_summarizer_instance = MagicMock()
        mock_summarizer_instance.summarize_all.return_value = {
            "abstract_methodology": "Abs",
            "plain_language_summary": "Plain",
            "key_findings": "Key",
            "citations": "Cit"
        }
        MockSummarizer.return_value = mock_summarizer_instance
        
        mock_visualizer_instance = MagicMock()
        mock_visualizer_instance.generate_visual_summary.return_value = "visual"
        MockVisualizer.return_value = mock_visualizer_instance
        
        run_app_with_mocks(mock_st)

@patch('app.st')
def test_app_tab1_mermaid(mock_st):
    mock_file = MagicMock()
    mock_file.getvalue.return_value = b"dummy pdf content"
    mock_st.file_uploader.return_value = mock_file
    mock_st.button.side_effect = lambda name: name == "Generate Summary"
    
    with patch('agent.pdf_parser.extract_text_from_pdf', return_value="dummy text") as mock_extract, \
         patch('agent.summarizer.PaperSummarizer') as MockSummarizer, \
         patch('agent.visualizer.Visualizer') as MockVisualizer:
        
        mock_summarizer_instance = MagicMock()
        mock_summarizer_instance.summarize_all.return_value = {
            "abstract_methodology": "Abs",
            "plain_language_summary": "Plain",
            "key_findings": "Key",
            "citations": "Cit"
        }
        MockSummarizer.return_value = mock_summarizer_instance
        
        mock_visualizer_instance = MagicMock()
        mock_visualizer_instance.generate_visual_summary.return_value = "```mermaid\nvisual\n```"
        MockVisualizer.return_value = mock_visualizer_instance
        
        run_app_with_mocks(mock_st)

@patch('app.st')
def test_app_tab2_success(mock_st):
    mock_st.file_uploader.return_value = None
    mock_st.text_input.side_effect = lambda name: "dummy_dir" if name == "Directory Path" else ""
    mock_st.button.side_effect = lambda name: name == "Process Directory"
    
    with patch('os.path.isdir', return_value=True), \
         patch('agent.batch_processor.BatchProcessor') as MockProcessor:
        
        mock_processor_instance = MagicMock()
        mock_processor_instance.process_directory.return_value = {"file1": "summary1"}
        MockProcessor.return_value = mock_processor_instance
        
        run_app_with_mocks(mock_st)

@patch('app.st')
def test_app_tab2_invalid_dir(mock_st):
    mock_st.file_uploader.return_value = None
    mock_st.text_input.side_effect = lambda name: "dummy_dir" if name == "Directory Path" else ""
    mock_st.button.side_effect = lambda name: name == "Process Directory"
    
    with patch('os.path.isdir', return_value=False):
        run_app_with_mocks(mock_st)

@patch('app.st')
def test_app_tab3_success(mock_st):
    mock_st.file_uploader.return_value = None
    mock_st.text_input.side_effect = lambda name: "dummy_topic" if name == "Enter a research topic" else ""
    mock_st.button.side_effect = lambda name: name == "Generate List"
    
    with patch('agent.reading_list.ReadingListGenerator') as MockGenerator:
        mock_generator_instance = MagicMock()
        mock_generator_instance.generate_reading_list.return_value = "reading list"
        MockGenerator.return_value = mock_generator_instance
        
        run_app_with_mocks(mock_st)

@patch('app.st')
def test_app_tab3_no_topic(mock_st):
    mock_st.file_uploader.return_value = None
    mock_st.text_input.side_effect = lambda name: "" if name == "Enter a research topic" else ""
    mock_st.button.side_effect = lambda name: name == "Generate List"
    
    run_app_with_mocks(mock_st)
