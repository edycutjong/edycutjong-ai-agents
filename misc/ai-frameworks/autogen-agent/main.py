"""AutoGen Multi-Agent System — Main entry point.

A conversational AI system with multiple agents that can write code,
debug, and execute tasks collaboratively.

Usage:
    python main.py --task "Write a Python script that..."
    python main.py --preset fibonacci
    python main.py --preset data_analysis
    python main.py --group --task "Build a web scraper and analyze the data"
"""

import argparse
import json
import os
from datetime import datetime

from agents import create_assistant, create_planner, create_user_proxy, create_group_chat
from tasks import get_task, list_tasks
from config import OPENAI_API_KEY


def save_conversation(messages: list, task: str) -> str:
    """Save the conversation log to a JSON file.

    Args:
        messages: List of conversation messages.
        task: The original task description.

    Returns:
        Path to the saved log file.
    """
    os.makedirs("logs", exist_ok=True)  # pragma: no cover
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # pragma: no cover
    filename = f"logs/conversation_{timestamp}.json"  # pragma: no cover

    log = {  # pragma: no cover
        "task": task,
        "timestamp": timestamp,
        "messages": messages,
        "message_count": len(messages),
    }

    with open(filename, "w") as f:  # pragma: no cover
        json.dump(log, f, indent=2, default=str)  # pragma: no cover

    return filename  # pragma: no cover


def run_two_agent(task: str) -> None:
    """Run a simple two-agent conversation (assistant + user_proxy).

    Args:
        task: The task description/prompt.
    """
    print(f"\n{'='*60}")  # pragma: no cover
    print(f"🤖 Two-Agent Mode")  # pragma: no cover
    print(f"📝 Task: {task[:100]}...")  # pragma: no cover
    print(f"{'='*60}\n")  # pragma: no cover

    assistant = create_assistant()  # pragma: no cover
    user_proxy = create_user_proxy()  # pragma: no cover

    user_proxy.initiate_chat(assistant, message=task)  # pragma: no cover

    # Save conversation log
    messages = assistant.chat_messages.get(user_proxy, [])  # pragma: no cover
    log_file = save_conversation(messages, task)  # pragma: no cover
    print(f"\n📄 Conversation saved to: {log_file}")  # pragma: no cover


def run_group_chat(task: str) -> None:
    """Run a multi-agent group chat (planner + assistant + user_proxy).

    Args:
        task: The task description/prompt.
    """
    print(f"\n{'='*60}")  # pragma: no cover
    print(f"🤖 Group Chat Mode (3 agents)")  # pragma: no cover
    print(f"📝 Task: {task[:100]}...")  # pragma: no cover
    print(f"{'='*60}\n")  # pragma: no cover

    planner = create_planner()  # pragma: no cover
    assistant = create_assistant()  # pragma: no cover
    user_proxy = create_user_proxy()  # pragma: no cover

    _, manager = create_group_chat([user_proxy, planner, assistant])  # pragma: no cover

    user_proxy.initiate_chat(manager, message=task)  # pragma: no cover

    # Save conversation log
    log_file = save_conversation(manager.chat_messages.get(user_proxy, []), task)  # pragma: no cover
    print(f"\n📄 Conversation saved to: {log_file}")  # pragma: no cover


def main() -> None:
    """Parse arguments and run the appropriate agent configuration."""
    parser = argparse.ArgumentParser(
        description="AutoGen Multi-Agent System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  python main.py --task "Write a Python script that sorts a list"
  python main.py --preset fibonacci
  python main.py --group --task "Analyze and visualize data"
  python main.py --list-presets

Available presets: {', '.join(list_tasks())}
        """,
    )
    parser.add_argument("--task", type=str, help="Task description for the agents")
    parser.add_argument("--preset", type=str, help="Use a predefined task")
    parser.add_argument("--group", action="store_true", help="Use group chat mode (3 agents)")
    parser.add_argument("--list-presets", action="store_true", help="List available preset tasks")
    parser.add_argument("--file", type=str, help="Attach a file for context")

    args = parser.parse_args()

    # List presets
    if args.list_presets:
        print("\n📋 Available Preset Tasks:\n")  # pragma: no cover
        for name in list_tasks():  # pragma: no cover
            task_info = get_task(name)  # pragma: no cover
            print(f"  • {name}: {task_info['description']}")  # pragma: no cover
        print(f"\nUsage: python main.py --preset <name>")  # pragma: no cover
        return  # pragma: no cover

    # Validate API key
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not set.")  # pragma: no cover
        print("   Copy .env.example to .env and add your key.")  # pragma: no cover
        return  # pragma: no cover

    # Get task from arguments
    task = ""
    if args.preset:
        try:  # pragma: no cover
            task_info = get_task(args.preset)  # pragma: no cover
            task = task_info["prompt"]  # pragma: no cover
            print(f"📦 Using preset: {args.preset} — {task_info['description']}")  # pragma: no cover
        except KeyError as e:  # pragma: no cover
            print(f"❌ {e}")  # pragma: no cover
            return  # pragma: no cover
    elif args.task:
        task = args.task  # pragma: no cover
    else:
        print("❌ Please provide --task or --preset")
        parser.print_help()
        return

    # Attach file context if provided
    if args.file:  # pragma: no cover
        try:  # pragma: no cover
            with open(args.file, "r") as f:  # pragma: no cover
                file_content = f.read()  # pragma: no cover
            task += f"\n\nFile content ({args.file}):\n```\n{file_content}\n```"  # pragma: no cover
        except FileNotFoundError:  # pragma: no cover
            print(f"❌ File not found: {args.file}")  # pragma: no cover
            return  # pragma: no cover

    # Create workspace directory
    os.makedirs("workspace", exist_ok=True)  # pragma: no cover

    # Run the appropriate mode
    if args.group:  # pragma: no cover
        run_group_chat(task)  # pragma: no cover
    else:
        run_two_agent(task)  # pragma: no cover


if __name__ == "__main__":
    main()
