import sys
import os
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

# Ensure the current directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent.researcher import Researcher
from agent.writer import Writer
from agent.seo import SEOOptimizer
from agent.utils import clean_text, save_to_file, format_filename

console = Console()

def main():
    console.print(Panel("[bold blue]Blog Post Writer Agent[/bold blue]", subtitle="Powered by LangChain & OpenAI"))

    # CLI Arguments
    parser = argparse.ArgumentParser(description="Generate SEO-optimized blog posts.")
    parser.add_argument("--topic", type=str, help="The topic of the blog post.")
    parser.add_argument("--output", type=str, help="Output directory.", default="output")
    args = parser.parse_args()

    # Get Topic
    topic = args.topic
    if not topic:
        topic = Prompt.ask("[bold green]Enter the topic for your blog post[/bold green]")

    # Initialize Agents
    researcher = Researcher()
    writer = Writer()
    seo_optimizer = SEOOptimizer()

    # Step 1: Research
    with console.status(f"[bold yellow]Researching '{topic}'...[/bold yellow]", spinner="dots"):
        research_result = researcher.research(topic)
        research_summary = research_result['summary']

    console.print(Panel(Markdown(research_summary), title="Research Summary", border_style="yellow"))

    # Step 2: Outline
    with console.status("[bold cyan]Creating Outline...[/bold cyan]", spinner="dots"):
        outline = writer.create_outline(topic, research_summary)

    console.print(Panel(Markdown(outline), title="Outline", border_style="cyan"))

    # Step 3: Write Post
    with console.status("[bold magenta]Writing Blog Post...[/bold magenta]", spinner="dots"):
        blog_post = writer.write_post(topic, outline, research_summary)

    console.print(Panel(Markdown(blog_post[:500] + "..."), title="Draft Blog Post (Preview)", border_style="magenta"))

    # Step 4: SEO Optimization
    with console.status("[bold green]Optimizing for SEO...[/bold green]", spinner="dots"):
        seo_result = seo_optimizer.optimize(topic, blog_post)
        seo_report = seo_result['seo_report']

    console.print(Panel(Markdown(seo_report), title="SEO Report", border_style="green"))

    # Step 5: Save
    output_dir = args.output
    filename = format_filename(topic)

    # Save Blog Post
    post_path = os.path.join(output_dir, filename)
    saved_post = save_to_file(blog_post, post_path, "md")
    console.print(f"[bold green]✓ Blog post saved to:[/bold green] {saved_post}")

    # Save Report
    report_path = os.path.join(output_dir, f"{filename}-seo-report")
    saved_report = save_to_file(seo_report, report_path, "md")
    console.print(f"[bold green]✓ SEO report saved to:[/bold green] {saved_report}")

    console.print("[bold blue]Done![/bold blue]")

if __name__ == "__main__":
    main()
