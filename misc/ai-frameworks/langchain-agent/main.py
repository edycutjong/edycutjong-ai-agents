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
    os.makedirs("logs", exist_ok=True)  # pragma: no cover
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # pragma: no cover
    filename = f"logs/conversation_{timestamp}.json"  # pragma: no cover

    log = {  # pragma: no cover
        "query": query,
        "model": MODEL_NAME,
        "timestamp": timestamp,
        "messages": messages,
        "message_count": len(messages),
    }

    with open(filename, "w") as f:  # pragma: no cover
        json.dump(log, f, indent=2, default=str)  # pragma: no cover

    return filename  # pragma: no cover


def run_single_query(query: str, filepath: str | None = None) -> None:
    """Run a single query and print the result.

    Args:
        query: The question to answer.
        filepath: Optional file path for document Q&A.
    """
    print(f"\n{'='*60}")  # pragma: no cover
    print(f"🤖 LangChain Research Agent")  # pragma: no cover
    print(f"📝 Query: {query[:100]}{'...' if len(query) > 100 else ''}")  # pragma: no cover
    print(f"🧠 Model: {MODEL_NAME}")  # pragma: no cover
    print(f"{'='*60}\n")  # pragma: no cover

    # Load document if provided
    vectorstore = None  # pragma: no cover
    if filepath:  # pragma: no cover
        print(f"📄 Loading {filepath}...")  # pragma: no cover
        vectorstore = load_and_embed_file(filepath)  # pragma: no cover
        print(f"✅ Document loaded and embedded\n")  # pragma: no cover

    # Create agent
    agent_executor = create_agent()  # pragma: no cover

    # Augment query with document context if available
    augmented = query  # pragma: no cover
    if vectorstore:  # pragma: no cover
        docs = similarity_search(vectorstore, query)  # pragma: no cover
        context = "\n\n".join(doc.page_content for doc in docs)  # pragma: no cover
        augmented = f"Context from loaded document:\n{context}\n\nQuestion: {query}"  # pragma: no cover

    # Run query
    print("🔄 Thinking...\n")  # pragma: no cover
    result = agent_executor.invoke({"input": augmented})  # pragma: no cover
    output = result.get("output", "No response generated.")  # pragma: no cover

    print(f"\n{'─'*60}")  # pragma: no cover
    print(f"📤 Response:\n")  # pragma: no cover
    print(output)  # pragma: no cover
    print(f"\n{'─'*60}")  # pragma: no cover

    # Save log
    messages = [  # pragma: no cover
        {"role": "human", "content": query},
        {"role": "assistant", "content": output},
    ]
    log_file = save_conversation(messages, query)  # pragma: no cover
    print(f"\n📄 Conversation saved to: {log_file}")  # pragma: no cover


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
        print(f"📄 Loading {filepath}...")  # pragma: no cover
        vectorstore = load_and_embed_file(filepath)  # pragma: no cover
        print(f"✅ Document loaded and embedded\n")  # pragma: no cover

    agent_executor = create_agent()
    history: list[dict] = []  # pragma: no cover

    while True:  # pragma: no cover
        try:  # pragma: no cover
            query = input("\n🧑 You: ").strip()  # pragma: no cover
        except (EOFError, KeyboardInterrupt):  # pragma: no cover
            break  # pragma: no cover

        if not query:  # pragma: no cover
            continue  # pragma: no cover

        if query == "/quit":  # pragma: no cover
            break  # pragma: no cover
        elif query == "/export":  # pragma: no cover
            log_file = save_conversation(history, "interactive_session")  # pragma: no cover
            print(f"💾 Saved to {log_file}")  # pragma: no cover
            continue  # pragma: no cover
        elif query == "/clear":  # pragma: no cover
            agent_executor.memory.clear()  # pragma: no cover
            history.clear()  # pragma: no cover
            print("🧹 Memory cleared")  # pragma: no cover
            continue  # pragma: no cover

        history.append({"role": "human", "content": query})  # pragma: no cover

        # Augment with document context
        augmented = query  # pragma: no cover
        if vectorstore:  # pragma: no cover
            docs = similarity_search(vectorstore, query)  # pragma: no cover
            context = "\n\n".join(doc.page_content for doc in docs)  # pragma: no cover
            augmented = f"Context:\n{context}\n\nQuestion: {query}"  # pragma: no cover

        try:  # pragma: no cover
            result = agent_executor.invoke({"input": augmented})  # pragma: no cover
            output = result.get("output", "No response generated.")  # pragma: no cover
            history.append({"role": "assistant", "content": output})  # pragma: no cover
            print(f"\n🤖 Agent: {output}")  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print(f"\n❌ Error: {e}")  # pragma: no cover

    print("\nGoodbye! 👋")  # pragma: no cover


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
        print("❌ OPENAI_API_KEY not set.")  # pragma: no cover
        print("   Copy .env.example to .env and add your key.")  # pragma: no cover
        return  # pragma: no cover

    # Validate file if provided
    if args.file and not os.path.exists(args.file):
        print(f"❌ File not found: {args.file}")  # pragma: no cover
        return  # pragma: no cover

    # Run the appropriate mode
    if args.query:
        run_single_query(args.query, args.file)  # pragma: no cover
    else:
        run_interactive(args.file)


if __name__ == "__main__":
    main()  # pragma: no cover
