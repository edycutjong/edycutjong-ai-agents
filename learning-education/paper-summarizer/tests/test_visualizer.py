import unittest
from unittest.mock import MagicMock, patch
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable

class TestVisualizer(unittest.TestCase):

    @patch('agent.visualizer.ChatOpenAI')
    def setUp(self, MockChatOpenAI):
        self.mock_llm_instance = MagicMock()
        self.mock_llm_instance.invoke.return_value = AIMessage(content="graph TD\n A-->B")

        class FakeLLM(Runnable):
            def __init__(self, mock_instance):
                self.mock_instance = mock_instance

            def invoke(self, input, config=None, **kwargs):
                return self.mock_instance.invoke(input, config, **kwargs)

        fake_llm = FakeLLM(self.mock_llm_instance)

        MockChatOpenAI.return_value = fake_llm
        from agent.visualizer import Visualizer
        self.visualizer = Visualizer()
        self.mock_llm = self.mock_llm_instance

    def test_generate_visual_summary(self):
        result = self.visualizer.generate_visual_summary("some text")
        self.assertEqual(result, "graph TD\n A-->B")

if __name__ == '__main__':
    unittest.main()
