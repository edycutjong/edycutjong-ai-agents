import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table
from rich.layout import Layout
from rich import print as rprint

from agent.parser import JobParser
from agent.generator import QuestionGenerator
from agent.grader import ResponseGrader
from agent.tracker import ProgressTracker
from config import OPENAI_API_KEY

console = Console()

class InterviewApp:
    def __init__(self):
        self.parser = JobParser(api_key=OPENAI_API_KEY)
        self.generator = QuestionGenerator(api_key=OPENAI_API_KEY)
        self.grader = ResponseGrader(api_key=OPENAI_API_KEY)
        self.tracker = ProgressTracker()

        self.context = None  # JobDescription object

    def start(self):
        console.clear()
        console.print(Panel.fit("[bold blue]AI Interview Prep Agent[/bold blue]\n[italic]Master your technical interviews[/italic]", border_style="blue"))

        if not OPENAI_API_KEY:
            console.print("[bold red]Error:[/bold red] OPENAI_API_KEY not found in .env file.")
            sys.exit(1)

        while True:
            self.show_menu()
            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"], default="4")

            if choice == "1":
                self.set_job_context()
            elif choice == "2":
                self.practice_session()
            elif choice == "3":
                self.view_progress()
            elif choice == "4":
                console.print("[bold green]Good luck with your interviews![/bold green]")
                break

    def show_menu(self):
        table = Table(title="Main Menu", show_header=False, box=None)
        table.add_row("[bold cyan]1.[/bold cyan] Set Job Context (Job Description)")
        table.add_row("[bold cyan]2.[/bold cyan] Start Practice Session")
        table.add_row("[bold cyan]3.[/bold cyan] View Progress")
        table.add_row("[bold cyan]4.[/bold cyan] Exit")
        console.print(table)

        if self.context:
            console.print(Panel(f"[bold]Current Context:[/bold]\nRole: {self.context.title}\nLevel: {self.context.experience_level}\nSkills: {', '.join(self.context.skills)}", title="Context Active", border_style="green"))
        else:
            console.print(Panel("[dim]No job context set. Questions will be generic.[/dim]", title="Context", border_style="yellow"))

    def set_job_context(self):
        console.print("[bold]Paste the job description below (press Enter twice to finish):[/bold]")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        job_text = "\n".join(lines)

        if not job_text.strip():
            console.print("[yellow]Empty job description provided.[/yellow]")
            return

        with console.status("[bold green]Analyzing job description...[/bold green]"):
            self.context = self.parser.parse(job_text)

        if self.context:
            console.print(f"[bold green]Context Set![/bold green] Role: {self.context.title}")
        else:
            console.print("[bold red]Failed to parse job description.[/bold red]")

    def practice_session(self):
        console.print("\n[bold]Select Question Type:[/bold]")
        console.print("1. Coding Challenge")
        console.print("2. System Design")
        console.print("3. Behavioral")

        q_type_choice = Prompt.ask("Choice", choices=["1", "2", "3"], default="1")

        question = None
        q_type_str = ""

        skills = self.context.skills if self.context else ["Python", "General Programming"]
        level = self.context.experience_level if self.context else "Mid-Level"

        with console.status("[bold green]Generating question...[/bold green]"):
            if q_type_choice == "1":
                q_type_str = "Coding"
                question = self.generator.generate_coding_question(skills, level)
            elif q_type_choice == "2":
                q_type_str = "System Design"
                question = self.generator.generate_system_design_question(skills, level)
            elif q_type_choice == "3":
                q_type_str = "Behavioral"
                focus = "Leadership" # Could be randomized or selected
                question = self.generator.generate_behavioral_question(focus)

        if not question:
            console.print("[bold red]Failed to generate question.[/bold red]")
            return

        self.display_question(question, q_type_str)

        console.print("\n[bold]Your Answer (press Enter twice to submit):[/bold]")
        lines = []
        while True:
            line = input()
            if not line:
                break
            lines.append(line)
        answer = "\n".join(lines)

        if not answer.strip():
            console.print("[yellow]No answer provided. Skipping grading.[/yellow]")
            return

        with console.status("[bold green]Grading answer...[/bold green]"):
            # Prepare question text for grader
            q_text = ""
            if q_type_choice == "1":
                q_text = f"Problem: {question.problem_statement}\nConstraints: {question.constraints}"
            elif q_type_choice == "2":
                q_text = f"Prompt: {question.prompt}\nRequirements: {question.requirements}"
            elif q_type_choice == "3":
                q_text = question.question

            evaluation = self.grader.grade_response(q_text, answer, q_type_str)

        if evaluation:
            self.display_evaluation(evaluation)
            self.tracker.save_session(q_type_str, q_text, answer, evaluation.score, evaluation.feedback)
        else:
            console.print("[bold red]Failed to grade response.[/bold red]")

    def display_question(self, question, q_type):
        console.clear()
        console.print(f"[bold underline]{q_type} Question[/bold underline]")

        if q_type == "Coding":
            md = f"**Problem:** {question.problem_statement}\n\n**Examples:**\n" + "\n".join(f"- {ex}" for ex in question.examples) + "\n\n**Constraints:**\n" + "\n".join(f"- {c}" for c in question.constraints)
            console.print(Markdown(md))
        elif q_type == "System Design":
            md = f"**Design:** {question.prompt}\n\n**Requirements:**\n" + "\n".join(f"- {r}" for r in question.requirements)
            console.print(Markdown(md))
        elif q_type == "Behavioral":
            console.print(Panel(question.question, title=f"Focus: {question.focus_area}"))

    def display_evaluation(self, evaluation):
        console.print("\n")
        score_color = "green" if evaluation.score >= 7 else "yellow" if evaluation.score >= 5 else "red"
        console.print(Panel(f"[bold {score_color}]Score: {evaluation.score}/10[/bold {score_color}]", title="Evaluation"))

        console.print("[bold]Feedback:[/bold]")
        console.print(Markdown(evaluation.feedback))

        console.print("\n[bold]Improved Answer:[/bold]")
        console.print(Markdown(evaluation.improved_answer))

        Prompt.ask("\nPress Enter to continue")

    def view_progress(self):
        console.clear()
        stats = self.tracker.get_stats()

        table = Table(title="Progress Stats")
        table.add_column("Category", style="cyan")
        table.add_column("Average Score", style="magenta")

        for category, score in stats.items():
            table.add_row(category, f"{score:.1f}")

        console.print(table)

        console.print("\n[bold]Recent Sessions:[/bold]")
        recent_table = Table(show_header=True, header_style="bold magenta")
        recent_table.add_column("Date")
        recent_table.add_column("Type")
        recent_table.add_column("Score")

        # Show last 5
        for session in list(reversed(self.tracker.sessions))[:5]:
            recent_table.add_row(session.timestamp[:10], session.question_type, str(session.score))

        console.print(recent_table)
        Prompt.ask("\nPress Enter to return to menu")

if __name__ == "__main__":
    app = InterviewApp()
    app.start()
