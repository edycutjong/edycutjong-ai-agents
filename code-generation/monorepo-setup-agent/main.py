import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.status import Status
from rich.text import Text

from agent.state import MonorepoConfig, PackageConfig
from agent.monorepo_agent import MonorepoAgent
from config import settings

app = typer.Typer()
console = Console()

@app.command()
def setup():
    """
    Interactive wizard to setup a new monorepo.
    """
    console.print(Panel.fit(
        "[bold blue]Monorepo Setup Agent[/bold blue]\n"
        "[dim]Powered by LangChain & OpenAI[/dim]",
        title="Welcome"
    ))

    # Collect project configuration
    project_name = Prompt.ask("Project Name", default="my-monorepo")

    package_manager = Prompt.ask(
        "Package Manager",
        choices=["pnpm", "npm", "yarn", "bun"],
        default=settings.DEFAULT_PACKAGE_MANAGER
    )

    monorepo_tool = Prompt.ask(
        "Monorepo Tool",
        choices=["turbo", "nx"],
        default=settings.DEFAULT_MONOREPO_TOOL
    )

    # Optional packages configuration
    packages = []
    if Confirm.ask("Do you want to add initial packages?", default=True):
        while True:
            pkg_name = Prompt.ask("Package Name (e.g., @repo/ui)", default="@repo/ui")
            packages.append(PackageConfig(name=pkg_name))
            if not Confirm.ask("Add another package?", default=False):
                break

    ci_provider = Prompt.ask(
        "CI Provider",
        choices=["github-actions", "gitlab-ci", "none"],
        default="github-actions"
    )

    config = MonorepoConfig(
        project_name=project_name,
        package_manager=package_manager,
        monorepo_tool=monorepo_tool,
        packages=packages,
        ci_provider=ci_provider if ci_provider != "none" else None
    )

    console.print(Panel(str(config.model_dump_json(indent=2)), title="Configuration Preview", border_style="green"))

    if not Confirm.ask("Proceed with generation?", default=True):
        console.print("[yellow]Aborted.[/yellow]")
        raise typer.Exit()

    # Execute Agent
    agent = MonorepoAgent(config)

    with console.status("[bold green]Generating Monorepo Structure...[/bold green]") as status:
        try:
            status.update("[bold green]Creating directories...[/bold green]")
            agent._create_structure()

            status.update("[bold green]Generating root files (LLM)...[/bold green]")
            agent._generate_root_files()

            status.update("[bold green]Generating shared configs...[/bold green]")
            agent._generate_shared_configs()

            if config.ci_provider:
                status.update(f"[bold green]Generating CI config for {config.ci_provider}...[/bold green]")
                agent._generate_ci_files()

            status.update("[bold green]Generating apps...[/bold green]")
            agent._generate_apps()

            if config.packages:
                status.update("[bold green]Generating additional packages...[/bold green]")
                agent._generate_packages()

            console.print("[bold green]✔ Monorepo setup complete![/bold green]")

            console.print(Panel(
                f"[bold]Next Steps:[/bold]\n"
                f"1. cd {project_name}\n"
                f"2. {package_manager} install\n"
                f"3. {package_manager} run dev",
                title="Done",
                border_style="blue"
            ))

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
