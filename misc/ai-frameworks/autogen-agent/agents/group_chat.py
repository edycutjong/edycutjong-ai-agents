"""GroupChat — multi-agent conversation for complex problems."""

from autogen import GroupChat, GroupChatManager
from autogen import AssistantAgent, UserProxyAgent
from config import LLM_CONFIG


def create_group_chat(
    agents: list[AssistantAgent | UserProxyAgent],
    max_round: int = 20,
) -> tuple[GroupChat, GroupChatManager]:
    """Create a GroupChat with a manager for multi-agent collaboration.

    Args:
        agents: List of agents to include in the group chat.
        max_round: Maximum conversation rounds.

    Returns:
        Tuple of (GroupChat, GroupChatManager).
    """
    group_chat = GroupChat(
        agents=agents,
        messages=[],
        max_round=max_round,
        speaker_selection_method="auto",
        allow_repeat_speaker=False,
    )

    manager = GroupChatManager(
        groupchat=group_chat,
        llm_config=LLM_CONFIG,
    )

    return group_chat, manager
