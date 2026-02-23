"""Rich terminal interface for the LangChain agent."""

import argparse
import json
import os
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

from agent import create_agent
from vectorstore import load_and_embed_file, similarity_search
from chains import create_qa_chain
from config import OPENAI_API_KEY

console = Console()


def save_history(messages: list[dict], filename: str | None = None) -> str:
    """Save conversation history as markdown.

    Args:
        messages: List of message dicts.
        filename: Optional output path.

    Returns:
        Path to saved file.
    """
    os.makedirs("exports", exist_ok=True)
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"exports/chat_{timestamp}.md"

    with open(filename, "w") as f:
        f.write("# Conversation Export\n\n")
        f.write(f"_Exported on {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n---\n\n")
        for msg in messages:
            role = "🧑 You" if msg["role"] == "human" else "🤖 Agent"
            f.write(f"### {role}\n\n{msg['content']}\n\n---\n\n")

    return filename


def interactive_mode(agent_executor, vectorstore=None) -> None:
    """Run the agent in interactive chat mode.

    Args:
        agent_executor: Configured AgentExecutor.
        vectorstore: Optional FAISS vector store for document Q&A.
    """
    console.print(
        Panel(
            "[bold cyan]🤖 LangChain Research Agent[/bold cyan]\n\n"
            "Commands:\n"
            "  [dim]/search <query>[/dim]  — Web search\n"
            "  [dim]/export[/dim]          — Save chat history\n"
            "  [dim]/clear[/dim]           — Clear memory\n"
            "  [dim]/quit[/dim]            — Exit",
            border_style="cyan",
        )
    )

    history: list[dict] = []

    while True:
        try:
            query = Prompt.ask("\n[bold green]You[/bold green]")
        except (EOFError, KeyboardInterrupt):
            break

        if not query.strip():
            continue

        if query.strip() == "/quit":
            break
        elif query.strip() == "/export":
            path = save_history(history)
            console.print(f"[green]💾 Saved to {path}[/green]")
            continue
        elif query.strip() == "/clear":
            agent_executor.memory.clear()
            history.clear()
            console.print("[yellow]🧹 Memory cleared[/yellow]")
            continue

        history.append({"role": "human", "content": query})

        # If we have a vector store, augment the query with context
        if vectorstore:
            docs = similarity_search(vectorstore, query)
            context = "\n\n".join(doc.page_content for doc in docs)
            augmented = f"Context from loaded document:\n{context}\n\nQuestion: {query}"
        else:
            augmented = query

        try:
            with console.status("[yellow]Thinking...[/yellow]"):
                result = agent_executor.invoke({"input": augmented})

            output = result.get("output", "No response generated.")
            history.append({"role": "assistant", "content": output})

            console.print()
            console.print(Panel(Markdown(output), title="🤖 Agent", border_style="blue"))

        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")

    console.print("\n[dim]Goodbye! 👋[/dim]")


def single_query(agent_executor, query: str, vectorstore=None) -> None:
    """Run a single query and print the result.

    Args:
        agent_executor: Configured AgentExecutor.
        query: The question to answer.
        vectorstore: Optional FAISS vector store.
    """
    if vectorstore:
        docs = similarity_search(vectorstore, query)
        context = "\n\n".join(doc.page_content for doc in docs)
        query = f"Context:\n{context}\n\nQuestion: {query}"

    with console.status("[yellow]Thinking...[/yellow]"):
        result = agent_executor.invoke({"input": query})

    output = result.get("output", "No response generated.")
    console.print(Panel(Markdown(output), title="🤖 Agent", border_style="blue"))


def main() -> None:
    """Parse arguments and run the agent."""
    parser = argparse.ArgumentParser(
        description="LangChain Research Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--query", type=str, help="Single query (non-interactive)")
    parser.add_argument("--file", type=str, help="Load a file for document Q&A")

    args = parser.parse_args()

    if not OPENAI_API_KEY:
        console.print(Panel("[red]❌ OPENAI_API_KEY not set.[/red]\nCopy .env.example to .env and add your key.", title="Error"))
        return

    # Load document if provided
    vectorstore = None
    if args.file:
        try:
            console.print(f"[yellow]📄 Loading {args.file}...[/yellow]")
            vectorstore = load_and_embed_file(args.file)
            console.print(f"[green]✅ Document loaded and embedded[/green]")
        except FileNotFoundError as e:
            console.print(f"[red]❌ {e}[/red]")
            return

    # Create agent
    agent_executor = create_agent()

    # Run in single or interactive mode
    if args.query:
        single_query(agent_executor, args.query, vectorstore)
    else:
        interactive_mode(agent_executor, vectorstore)


if __name__ == "__main__":
    main()
