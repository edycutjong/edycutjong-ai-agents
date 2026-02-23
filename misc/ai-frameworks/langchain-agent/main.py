"""LangChain Research Agent — Main entry point.

An AI research agent that can search the web, summarize documents,
and answer complex questions using LangChain and OpenAI.

Usage:
    python main.py                          # interactive mode
    python main.py --query "your question"  # single query
    python main.py --file doc.pdf --query "summarize this"
"""

import argparse
import json
import os
from datetime import datetime

from agent import create_agent
from vectorstore import load_and_embed_file, similarity_search
from chains import create_qa_chain
from config import OPENAI_API_KEY, MODEL_NAME


def save_conversation(messages: list[dict], query: str) -> str:
    """Save conversation log to a JSON file.

    Args:
        messages: List of message dicts with role and content.
        query: The original query.

    Returns:
        Path to the saved log file.
    """
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"logs/conversation_{timestamp}.json"

    log = {
        "query": query,
        "model": MODEL_NAME,
        "timestamp": timestamp,
        "messages": messages,
        "message_count": len(messages),
    }

    with open(filename, "w") as f:
        json.dump(log, f, indent=2, default=str)

    return filename


def run_single_query(query: str, filepath: str | None = None) -> None:
    """Run a single query and print the result.

    Args:
        query: The question to answer.
        filepath: Optional file path for document Q&A.
    """
    print(f"\n{'='*60}")
    print(f"🤖 LangChain Research Agent")
    print(f"📝 Query: {query[:100]}{'...' if len(query) > 100 else ''}")
    print(f"🧠 Model: {MODEL_NAME}")
    print(f"{'='*60}\n")

    # Load document if provided
    vectorstore = None
    if filepath:
        print(f"📄 Loading {filepath}...")
        vectorstore = load_and_embed_file(filepath)
        print(f"✅ Document loaded and embedded\n")

    # Create agent
    agent_executor = create_agent()

    # Augment query with document context if available
    augmented = query
    if vectorstore:
        docs = similarity_search(vectorstore, query)
        context = "\n\n".join(doc.page_content for doc in docs)
        augmented = f"Context from loaded document:\n{context}\n\nQuestion: {query}"

    # Run query
    print("🔄 Thinking...\n")
    result = agent_executor.invoke({"input": augmented})
    output = result.get("output", "No response generated.")

    print(f"\n{'─'*60}")
    print(f"📤 Response:\n")
    print(output)
    print(f"\n{'─'*60}")

    # Save log
    messages = [
        {"role": "human", "content": query},
        {"role": "assistant", "content": output},
    ]
    log_file = save_conversation(messages, query)
    print(f"\n📄 Conversation saved to: {log_file}")


def run_interactive(filepath: str | None = None) -> None:
    """Run the agent in interactive chat mode.

    Args:
        filepath: Optional file path for document Q&A.
    """
    print(f"\n{'='*60}")
    print(f"🤖 LangChain Research Agent — Interactive Mode")
    print(f"🧠 Model: {MODEL_NAME}")
    print(f"{'='*60}")
    print(f"\nCommands: /export, /clear, /quit\n")

    # Load document if provided
    vectorstore = None
    if filepath:
        print(f"📄 Loading {filepath}...")
        vectorstore = load_and_embed_file(filepath)
        print(f"✅ Document loaded and embedded\n")

    agent_executor = create_agent()
    history: list[dict] = []

    while True:
        try:
            query = input("\n🧑 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not query:
            continue

        if query == "/quit":
            break
        elif query == "/export":
            log_file = save_conversation(history, "interactive_session")
            print(f"💾 Saved to {log_file}")
            continue
        elif query == "/clear":
            agent_executor.memory.clear()
            history.clear()
            print("🧹 Memory cleared")
            continue

        history.append({"role": "human", "content": query})

        # Augment with document context
        augmented = query
        if vectorstore:
            docs = similarity_search(vectorstore, query)
            context = "\n\n".join(doc.page_content for doc in docs)
            augmented = f"Context:\n{context}\n\nQuestion: {query}"

        try:
            result = agent_executor.invoke({"input": augmented})
            output = result.get("output", "No response generated.")
            history.append({"role": "assistant", "content": output})
            print(f"\n🤖 Agent: {output}")
        except Exception as e:
            print(f"\n❌ Error: {e}")

    print("\nGoodbye! 👋")


def main() -> None:
    """Parse arguments and run the appropriate mode."""
    parser = argparse.ArgumentParser(
        description="LangChain Research Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                  # interactive mode
  python main.py --query "What is LangChain?"     # single query
  python main.py --file doc.pdf --query "summarize this"
  python main.py --file notes.txt                 # interactive with doc
        """,
    )
    parser.add_argument("--query", type=str, help="Single query (non-interactive)")
    parser.add_argument("--file", type=str, help="Load a file for document Q&A")

    args = parser.parse_args()

    # Validate API key
    if not OPENAI_API_KEY:
        print("❌ OPENAI_API_KEY not set.")
        print("   Copy .env.example to .env and add your key.")
        return

    # Validate file if provided
    if args.file and not os.path.exists(args.file):
        print(f"❌ File not found: {args.file}")
        return

    # Run the appropriate mode
    if args.query:
        run_single_query(args.query, args.file)
    else:
        run_interactive(args.file)


if __name__ == "__main__":
    main()
