import pytest
import os
import sys
from unittest.mock import MagicMock

# Add the project root to sys.path so tests can import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock dependencies globally
sys.modules['langchain_openai'] = MagicMock()
sys.modules['langchain_google_genai'] = MagicMock()
sys.modules['langchain_community'] = MagicMock()
sys.modules['langchain_core'] = MagicMock()
sys.modules['langchain_core.prompts'] = MagicMock()
sys.modules['langchain_core.output_parsers'] = MagicMock()
sys.modules['fpdf'] = MagicMock()
sys.modules['streamlit'] = MagicMock()
sys.modules['dotenv'] = MagicMock()
