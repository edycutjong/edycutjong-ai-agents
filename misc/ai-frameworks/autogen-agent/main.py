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
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/conversation_{timestamp}.json"

    log = {
        "task": task,
        "timestamp": timestamp,
        "messages": messages,
        "message_count": len(messages),
    }

    with open(filename, "w") as f:
        json.dump(log, f, indent=2, default=str)

    return filename


def run_two_agent(task: str) -> None:
    """Run a simple two-agent conversation (assistant + user_proxy).

    Args:
        task: The task description/prompt.
    """
    print(f"\n{'='*60}")
    print(f"🤖 Two-Agent Mode")
    print(f"📝 Task: {task[:100]}...")
    print(f"{'='*60}\n")

    assistant = create_assistant()
    user_proxy = create_user_proxy()

    user_proxy.initiate_chat(assistant, message=task)

    # Save conversation log
    messages = assistant.chat_messages.get(user_proxy, [])
    log_file = save_conversation(messages, task)
    print(f"\n📄 Conversation saved to: {log_file}")


def run_group_chat(task: str) -> None:
    """Run a multi-agent group chat (planner + assistant + user_proxy).

    Args:
        task: The task description/prompt.
    """
    print(f"\n{'='*60}")
    print(f"🤖 Group Chat Mode (3 agents)")
    print(f"📝 Task: {task[:100]}...")
    print(f"{'='*60}\n")

    planner = create_planner()
    assistant = create_assistant()
    user_proxy = create_user_proxy()

    _, manager = create_group_chat([user_proxy, planner, assistant])

    user_proxy.initiate_chat(manager, message=task)

    # Save conversation log
    log_file = save_conversation(manager.chat_messages.get(user_proxy, []), task)
    print(f"\n📄 Conversation saved to: {log_file}")


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
        print("\n📋 Available Preset Tasks:\n")
        for name in list_tasks():
            task_info = get_task(name)
            print(f"  • {name}: {task_info['description']}")
        print(f"\nUsage: python main.py --preset <name>")
        return

    # Validate API key
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not set.")
        print("   Copy .env.example to .env and add your key.")
        return

    # Get task from arguments
    task = ""
    if args.preset:
        try:
            task_info = get_task(args.preset)
            task = task_info["prompt"]
            print(f"📦 Using preset: {args.preset} — {task_info['description']}")
        except KeyError as e:
            print(f"❌ {e}")
            return
    elif args.task:
        task = args.task
    else:
        print("❌ Please provide --task or --preset")
        parser.print_help()
        return

    # Attach file context if provided
    if args.file:
        try:
            with open(args.file, "r") as f:
                file_content = f.read()
            task += f"\n\nFile content ({args.file}):\n```\n{file_content}\n```"
        except FileNotFoundError:
            print(f"❌ File not found: {args.file}")
            return

    # Create workspace directory
    os.makedirs("workspace", exist_ok=True)

    # Run the appropriate mode
    if args.group:
        run_group_chat(task)
    else:
        run_two_agent(task)


if __name__ == "__main__":
    main()
