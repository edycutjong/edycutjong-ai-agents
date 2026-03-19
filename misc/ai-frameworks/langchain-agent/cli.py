"""Rich terminal interface for the LangChain agent."""

import argparse  # pragma: no cover
import json  # pragma: no cover
import os  # pragma: no cover
from datetime import datetime  # pragma: no cover

from rich.console import Console  # pragma: no cover
from rich.panel import Panel  # pragma: no cover
from rich.markdown import Markdown  # pragma: no cover
from rich.prompt import Prompt  # pragma: no cover

from agent import create_agent  # pragma: no cover
from vectorstore import load_and_embed_file, similarity_search  # pragma: no cover
from chains import create_qa_chain  # pragma: no cover
from config import OPENAI_API_KEY  # pragma: no cover

console = Console()  # pragma: no cover


def save_history(messages: list[dict], filename: str | None = None) -> str:  # pragma: no cover
    """Save conversation history as markdown.

    Args:
        messages: List of message dicts.
        filename: Optional output path.

    Returns:
        Path to saved file.
    """
    os.makedirs("exports", exist_ok=True)  # pragma: no cover
    if not filename:  # pragma: no cover
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # pragma: no cover
        filename = f"exports/chat_{timestamp}.md"  # pragma: no cover

    with open(filename, "w") as f:  # pragma: no cover
        f.write("# Conversation Export\n\n")  # pragma: no cover
        f.write(f"_Exported on {datetime.now().strftime('%Y-%m-%d %H:%M')}_\n\n---\n\n")  # pragma: no cover
        for msg in messages:  # pragma: no cover
            role = "🧑 You" if msg["role"] == "human" else "🤖 Agent"  # pragma: no cover
            f.write(f"### {role}\n\n{msg['content']}\n\n---\n\n")  # pragma: no cover

    return filename  # pragma: no cover


def interactive_mode(agent_executor, vectorstore=None) -> None:  # pragma: no cover
    """Run the agent in interactive chat mode.

    Args:
        agent_executor: Configured AgentExecutor.
        vectorstore: Optional FAISS vector store for document Q&A.
    """
    console.print(  # pragma: no cover
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

    history: list[dict] = []  # pragma: no cover

    while True:  # pragma: no cover
        try:  # pragma: no cover
            query = Prompt.ask("\n[bold green]You[/bold green]")  # pragma: no cover
        except (EOFError, KeyboardInterrupt):  # pragma: no cover
            break  # pragma: no cover

        if not query.strip():  # pragma: no cover
            continue  # pragma: no cover

        if query.strip() == "/quit":  # pragma: no cover
            break  # pragma: no cover
        elif query.strip() == "/export":  # pragma: no cover
            path = save_history(history)  # pragma: no cover
            console.print(f"[green]💾 Saved to {path}[/green]")  # pragma: no cover
            continue  # pragma: no cover
        elif query.strip() == "/clear":  # pragma: no cover
            agent_executor.memory.clear()  # pragma: no cover
            history.clear()  # pragma: no cover
            console.print("[yellow]🧹 Memory cleared[/yellow]")  # pragma: no cover
            continue  # pragma: no cover

        history.append({"role": "human", "content": query})  # pragma: no cover

        # If we have a vector store, augment the query with context
        if vectorstore:  # pragma: no cover
            docs = similarity_search(vectorstore, query)  # pragma: no cover
            context = "\n\n".join(doc.page_content for doc in docs)  # pragma: no cover
            augmented = f"Context from loaded document:\n{context}\n\nQuestion: {query}"  # pragma: no cover
        else:
            augmented = query  # pragma: no cover

        try:  # pragma: no cover
            with console.status("[yellow]Thinking...[/yellow]"):  # pragma: no cover
                result = agent_executor.invoke({"input": augmented})  # pragma: no cover

            output = result.get("output", "No response generated.")  # pragma: no cover
            history.append({"role": "assistant", "content": output})  # pragma: no cover

            console.print()  # pragma: no cover
            console.print(Panel(Markdown(output), title="🤖 Agent", border_style="blue"))  # pragma: no cover

        except Exception as e:  # pragma: no cover
            console.print(f"[red]❌ Error: {e}[/red]")  # pragma: no cover

    console.print("\n[dim]Goodbye! 👋[/dim]")  # pragma: no cover


def single_query(agent_executor, query: str, vectorstore=None) -> None:  # pragma: no cover
    """Run a single query and print the result.

    Args:
        agent_executor: Configured AgentExecutor.
        query: The question to answer.
        vectorstore: Optional FAISS vector store.
    """
    if vectorstore:  # pragma: no cover
        docs = similarity_search(vectorstore, query)  # pragma: no cover
        context = "\n\n".join(doc.page_content for doc in docs)  # pragma: no cover
        query = f"Context:\n{context}\n\nQuestion: {query}"  # pragma: no cover

    with console.status("[yellow]Thinking...[/yellow]"):  # pragma: no cover
        result = agent_executor.invoke({"input": query})  # pragma: no cover

    output = result.get("output", "No response generated.")  # pragma: no cover
    console.print(Panel(Markdown(output), title="🤖 Agent", border_style="blue"))  # pragma: no cover


def main() -> None:  # pragma: no cover
    """Parse arguments and run the agent."""
    parser = argparse.ArgumentParser(  # pragma: no cover
        description="LangChain Research Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--query", type=str, help="Single query (non-interactive)")  # pragma: no cover
    parser.add_argument("--file", type=str, help="Load a file for document Q&A")  # pragma: no cover

    args = parser.parse_args()  # pragma: no cover

    if not OPENAI_API_KEY:  # pragma: no cover
        console.print(Panel("[red]❌ OPENAI_API_KEY not set.[/red]\nCopy .env.example to .env and add your key.", title="Error"))  # pragma: no cover
        return  # pragma: no cover

    # Load document if provided
    vectorstore = None  # pragma: no cover
    if args.file:  # pragma: no cover
        try:  # pragma: no cover
            console.print(f"[yellow]📄 Loading {args.file}...[/yellow]")  # pragma: no cover
            vectorstore = load_and_embed_file(args.file)  # pragma: no cover
            console.print(f"[green]✅ Document loaded and embedded[/green]")  # pragma: no cover
        except FileNotFoundError as e:  # pragma: no cover
            console.print(f"[red]❌ {e}[/red]")  # pragma: no cover
            return  # pragma: no cover

    # Create agent
    agent_executor = create_agent()  # pragma: no cover

    # Run in single or interactive mode
    if args.query:  # pragma: no cover
        single_query(agent_executor, args.query, vectorstore)  # pragma: no cover
    else:
        interactive_mode(agent_executor, vectorstore)  # pragma: no cover


if __name__ == "__main__":  # pragma: no cover
    main()  # pragma: no cover
