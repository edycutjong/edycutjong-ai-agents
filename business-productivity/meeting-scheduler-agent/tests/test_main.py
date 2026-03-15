"""Tests for meeting-scheduler-agent main.py, config.py, agent/llm.py, and agent/core.py."""
import pytest
import os, sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class TestConfig:
    def test_config_defaults(self):
        import config
        assert config.TIMEZONE == "UTC"
        assert config.DEFAULT_MEETING_DURATION == 60


class TestLlm:
    def test_get_llm_no_key(self, capsys):
        import agent.llm as llm_mod
        original = llm_mod.OPENAI_API_KEY
        llm_mod.OPENAI_API_KEY = None
        result = llm_mod.get_llm()
        assert result is None
        llm_mod.OPENAI_API_KEY = original

    @patch("agent.llm.ChatOpenAI")
    def test_get_llm_with_key(self, mock_chat):
        import agent.llm as llm_mod
        original = llm_mod.OPENAI_API_KEY
        llm_mod.OPENAI_API_KEY = "test-key"
        mock_chat.return_value = MagicMock()
        result = llm_mod.get_llm()
        assert result is not None
        mock_chat.assert_called_once()
        llm_mod.OPENAI_API_KEY = original


class TestCore:
    @patch("agent.core.get_llm", return_value=None)
    @patch("agent.core.get_tools", return_value=[])
    def test_create_agent_executor_no_llm(self, mock_tools, mock_llm):
        from agent.core import create_agent_executor
        result = create_agent_executor()
        assert result is None

    def test_run_agent_step_no_executor(self):
        from agent.core import run_agent_step
        result = run_agent_step(None, "hello")
        assert "not initialized" in result

    def test_run_agent_step_exception(self):
        from agent.core import run_agent_step
        mock_executor = MagicMock()
        mock_executor.invoke.side_effect = Exception("API fail")
        result = run_agent_step(mock_executor, "hello")
        assert "Error" in result

    def test_run_agent_step_success(self):
        from agent.core import run_agent_step
        mock_executor = MagicMock()
        mock_msg = MagicMock()
        mock_msg.content = "Hello back!"
        mock_executor.invoke.return_value = {"messages": [mock_msg]}
        result = run_agent_step(mock_executor, "hello")
        assert result == "Hello back!"


class TestMainFunction:
    @patch("main.Prompt")
    @patch("main.Console")
    @patch("main.create_agent_executor", return_value=None)
    def test_main_no_agent(self, mock_create, mock_console_cls, mock_prompt):
        from main import main
        console_inst = MagicMock()
        mock_console_cls.return_value = console_inst
        console_inst.status.return_value.__enter__ = MagicMock()
        console_inst.status.return_value.__exit__ = MagicMock()
        main()
        console_inst.print.assert_called()

    @patch("main.Prompt")
    @patch("main.Console")
    @patch("main.create_agent_executor")
    @patch("main.run_agent_step", return_value="Hi!")
    def test_main_exit_command(self, mock_run, mock_create, mock_console_cls, mock_prompt):
        from main import main
        console_inst = MagicMock()
        mock_console_cls.return_value = console_inst
        console_inst.status.return_value.__enter__ = MagicMock()
        console_inst.status.return_value.__exit__ = MagicMock()
        mock_create.return_value = MagicMock()
        mock_prompt.ask.side_effect = ["exit"]
        main()

    @patch("main.Prompt")
    @patch("main.Console")
    @patch("main.create_agent_executor")
    @patch("main.run_agent_step", return_value="Response")
    def test_main_conversation(self, mock_run, mock_create, mock_console_cls, mock_prompt):
        from main import main
        console_inst = MagicMock()
        mock_console_cls.return_value = console_inst
        console_inst.status.return_value.__enter__ = MagicMock()
        console_inst.status.return_value.__exit__ = MagicMock()
        mock_create.return_value = MagicMock()
        mock_prompt.ask.side_effect = ["hello", "quit"]
        main()

    @patch("main.Prompt")
    @patch("main.Console")
    @patch("main.create_agent_executor")
    @patch("main.run_agent_step", return_value="ignored")
    def test_main_empty_input(self, mock_run, mock_create, mock_console_cls, mock_prompt):
        from main import main
        console_inst = MagicMock()
        mock_console_cls.return_value = console_inst
        console_inst.status.return_value.__enter__ = MagicMock()
        console_inst.status.return_value.__exit__ = MagicMock()
        mock_create.return_value = MagicMock()
        mock_prompt.ask.side_effect = ["", "exit"]
        main()

    @patch("main.Prompt")
    @patch("main.Console")
    @patch("main.create_agent_executor")
    def test_main_keyboard_interrupt(self, mock_create, mock_console_cls, mock_prompt):
        from main import main
        console_inst = MagicMock()
        mock_console_cls.return_value = console_inst
        console_inst.status.return_value.__enter__ = MagicMock()
        console_inst.status.return_value.__exit__ = MagicMock()
        mock_create.return_value = MagicMock()
        mock_prompt.ask.side_effect = KeyboardInterrupt
        main()

    @patch("main.Prompt")
    @patch("main.Console")
    @patch("main.create_agent_executor")
    @patch("main.run_agent_step", side_effect=RuntimeError("boom"))
    def test_main_exception(self, mock_run, mock_create, mock_console_cls, mock_prompt):
        from main import main
        console_inst = MagicMock()
        mock_console_cls.return_value = console_inst
        console_inst.status.return_value.__enter__ = MagicMock()
        console_inst.status.return_value.__exit__ = MagicMock()
        mock_create.return_value = MagicMock()
        mock_prompt.ask.side_effect = ["hello", "exit"]
        main()


class TestMainBlock:
    def test_main_block(self):
        """Test __main__ block using exec guard."""
        script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")
        with open(script) as f:
            source = f.read()
        assert 'if __name__ == "__main__":' in source
        with patch("main.main") as mock_main:
            exec(compile("if __name__ == '__main__': main()", script, "exec"),
                 {"__name__": "__main__", "main": mock_main})
            mock_main.assert_called_once()
