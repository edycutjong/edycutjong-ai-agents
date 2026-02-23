import unittest
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable

class TestReadingListGenerator(unittest.TestCase):

    @patch('agent.reading_list.ChatOpenAI')
    def setUp(self, MockChatOpenAI):
        self.mock_llm_instance = MagicMock()
        self.mock_llm_instance.invoke.return_value = AIMessage(content="1. Paper A\n2. Paper B")

        class FakeLLM(Runnable):
            def __init__(self, mock_instance):
                self.mock_instance = mock_instance

            def invoke(self, input, config=None, **kwargs):
                return self.mock_instance.invoke(input, config, **kwargs)

        fake_llm = FakeLLM(self.mock_llm_instance)

        MockChatOpenAI.return_value = fake_llm
        from agent.reading_list import ReadingListGenerator
        self.generator = ReadingListGenerator()
        self.mock_llm = self.mock_llm_instance

    def test_generate_reading_list(self):
        result = self.generator.generate_reading_list("Deep Learning")
        self.assertEqual(result, "1. Paper A\n2. Paper B")

if __name__ == '__main__':
    unittest.main()
