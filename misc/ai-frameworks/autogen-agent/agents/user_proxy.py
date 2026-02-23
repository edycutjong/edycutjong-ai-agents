"""UserProxyAgent — executes code and provides feedback."""

from autogen import UserProxyAgent
from config import CODE_EXECUTION_CONFIG, MAX_CONSECUTIVE_AUTO_REPLY, HUMAN_INPUT_MODE


def create_user_proxy(name: str = "user_proxy") -> UserProxyAgent:
    """Create a UserProxyAgent that executes code and relays results.

    Args:
        name: The agent's name in conversations.

    Returns:
        Configured UserProxyAgent instance.
    """
    return UserProxyAgent(
        name=name,
        human_input_mode=HUMAN_INPUT_MODE,
        max_consecutive_auto_reply=MAX_CONSECUTIVE_AUTO_REPLY,
        is_termination_msg=lambda x: x.get("content", "")
        .rstrip()
        .endswith("TERMINATE"),
        code_execution_config=CODE_EXECUTION_CONFIG,
        system_message="""You are a user proxy that executes code on behalf of the user.
When code is provided:
1. Execute it in the sandbox
2. Report the output clearly
3. If there's an error, share the full traceback

Reply TERMINATE when the task is complete and verified.""",
    )
