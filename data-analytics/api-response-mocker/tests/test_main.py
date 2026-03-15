import pytest
from streamlit.testing.v1 import AppTest
from unittest.mock import patch

def test_main_app():
    at = AppTest.from_file("main.py")
    at.run()
    assert not at.exception
