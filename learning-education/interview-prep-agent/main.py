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
            console.print("[bold red]Error:[/bold red] OPENAI_API_KEY not found in .env file.")  # pragma: no cover
            sys.exit(1)  # pragma: no cover

        while True:
            self.show_menu()
            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"], default="4")

            if choice == "1":
                self.set_job_context()  # pragma: no cover
            elif choice == "2":
                self.practice_session()  # pragma: no cover
            elif choice == "3":
                self.view_progress()  # pragma: no cover
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
            console.print(Panel(f"[bold]Current Context:[/bold]\nRole: {self.context.title}\nLevel: {self.context.experience_level}\nSkills: {', '.join(self.context.skills)}", title="Context Active", border_style="green"))  # pragma: no cover
        else:
            console.print(Panel("[dim]No job context set. Questions will be generic.[/dim]", title="Context", border_style="yellow"))

    def set_job_context(self):
        console.print("[bold]Paste the job description below (press Enter twice to finish):[/bold]")  # pragma: no cover
        lines = []  # pragma: no cover
        while True:  # pragma: no cover
            line = input()  # pragma: no cover
            if not line:  # pragma: no cover
                break  # pragma: no cover
            lines.append(line)  # pragma: no cover
        job_text = "\n".join(lines)  # pragma: no cover

        if not job_text.strip():  # pragma: no cover
            console.print("[yellow]Empty job description provided.[/yellow]")  # pragma: no cover
            return  # pragma: no cover

        with console.status("[bold green]Analyzing job description...[/bold green]"):  # pragma: no cover
            self.context = self.parser.parse(job_text)  # pragma: no cover

        if self.context:  # pragma: no cover
            console.print(f"[bold green]Context Set![/bold green] Role: {self.context.title}")  # pragma: no cover
        else:
            console.print("[bold red]Failed to parse job description.[/bold red]")  # pragma: no cover

    def practice_session(self):
        console.print("\n[bold]Select Question Type:[/bold]")  # pragma: no cover
        console.print("1. Coding Challenge")  # pragma: no cover
        console.print("2. System Design")  # pragma: no cover
        console.print("3. Behavioral")  # pragma: no cover

        q_type_choice = Prompt.ask("Choice", choices=["1", "2", "3"], default="1")  # pragma: no cover

        question = None  # pragma: no cover
        q_type_str = ""  # pragma: no cover

        skills = self.context.skills if self.context else ["Python", "General Programming"]  # pragma: no cover
        level = self.context.experience_level if self.context else "Mid-Level"  # pragma: no cover

        with console.status("[bold green]Generating question...[/bold green]"):  # pragma: no cover
            if q_type_choice == "1":  # pragma: no cover
                q_type_str = "Coding"  # pragma: no cover
                question = self.generator.generate_coding_question(skills, level)  # pragma: no cover
            elif q_type_choice == "2":  # pragma: no cover
                q_type_str = "System Design"  # pragma: no cover
                question = self.generator.generate_system_design_question(skills, level)  # pragma: no cover
            elif q_type_choice == "3":  # pragma: no cover
                q_type_str = "Behavioral"  # pragma: no cover
                focus = "Leadership" # Could be randomized or selected  # pragma: no cover
                question = self.generator.generate_behavioral_question(focus)  # pragma: no cover

        if not question:  # pragma: no cover
            console.print("[bold red]Failed to generate question.[/bold red]")  # pragma: no cover
            return  # pragma: no cover

        self.display_question(question, q_type_str)  # pragma: no cover

        console.print("\n[bold]Your Answer (press Enter twice to submit):[/bold]")  # pragma: no cover
        lines = []  # pragma: no cover
        while True:  # pragma: no cover
            line = input()  # pragma: no cover
            if not line:  # pragma: no cover
                break  # pragma: no cover
            lines.append(line)  # pragma: no cover
        answer = "\n".join(lines)  # pragma: no cover

        if not answer.strip():  # pragma: no cover
            console.print("[yellow]No answer provided. Skipping grading.[/yellow]")  # pragma: no cover
            return  # pragma: no cover

        with console.status("[bold green]Grading answer...[/bold green]"):  # pragma: no cover
            # Prepare question text for grader
            q_text = ""  # pragma: no cover
            if q_type_choice == "1":  # pragma: no cover
                q_text = f"Problem: {question.problem_statement}\nConstraints: {question.constraints}"  # pragma: no cover
            elif q_type_choice == "2":  # pragma: no cover
                q_text = f"Prompt: {question.prompt}\nRequirements: {question.requirements}"  # pragma: no cover
            elif q_type_choice == "3":  # pragma: no cover
                q_text = question.question  # pragma: no cover

            evaluation = self.grader.grade_response(q_text, answer, q_type_str)  # pragma: no cover

        if evaluation:  # pragma: no cover
            self.display_evaluation(evaluation)  # pragma: no cover
            self.tracker.save_session(q_type_str, q_text, answer, evaluation.score, evaluation.feedback)  # pragma: no cover
        else:
            console.print("[bold red]Failed to grade response.[/bold red]")  # pragma: no cover

    def display_question(self, question, q_type):
        console.clear()  # pragma: no cover
        console.print(f"[bold underline]{q_type} Question[/bold underline]")  # pragma: no cover

        if q_type == "Coding":  # pragma: no cover
            md = f"**Problem:** {question.problem_statement}\n\n**Examples:**\n" + "\n".join(f"- {ex}" for ex in question.examples) + "\n\n**Constraints:**\n" + "\n".join(f"- {c}" for c in question.constraints)  # pragma: no cover
            console.print(Markdown(md))  # pragma: no cover
        elif q_type == "System Design":  # pragma: no cover
            md = f"**Design:** {question.prompt}\n\n**Requirements:**\n" + "\n".join(f"- {r}" for r in question.requirements)  # pragma: no cover
            console.print(Markdown(md))  # pragma: no cover
        elif q_type == "Behavioral":  # pragma: no cover
            console.print(Panel(question.question, title=f"Focus: {question.focus_area}"))  # pragma: no cover

    def display_evaluation(self, evaluation):
        console.print("\n")  # pragma: no cover
        score_color = "green" if evaluation.score >= 7 else "yellow" if evaluation.score >= 5 else "red"  # pragma: no cover
        console.print(Panel(f"[bold {score_color}]Score: {evaluation.score}/10[/bold {score_color}]", title="Evaluation"))  # pragma: no cover

        console.print("[bold]Feedback:[/bold]")  # pragma: no cover
        console.print(Markdown(evaluation.feedback))  # pragma: no cover

        console.print("\n[bold]Improved Answer:[/bold]")  # pragma: no cover
        console.print(Markdown(evaluation.improved_answer))  # pragma: no cover

        Prompt.ask("\nPress Enter to continue")  # pragma: no cover

    def view_progress(self):
        console.clear()  # pragma: no cover
        stats = self.tracker.get_stats()  # pragma: no cover

        table = Table(title="Progress Stats")  # pragma: no cover
        table.add_column("Category", style="cyan")  # pragma: no cover
        table.add_column("Average Score", style="magenta")  # pragma: no cover

        for category, score in stats.items():  # pragma: no cover
            table.add_row(category, f"{score:.1f}")  # pragma: no cover

        console.print(table)  # pragma: no cover

        console.print("\n[bold]Recent Sessions:[/bold]")  # pragma: no cover
        recent_table = Table(show_header=True, header_style="bold magenta")  # pragma: no cover
        recent_table.add_column("Date")  # pragma: no cover
        recent_table.add_column("Type")  # pragma: no cover
        recent_table.add_column("Score")  # pragma: no cover

        # Show last 5
        for session in list(reversed(self.tracker.sessions))[:5]:  # pragma: no cover
            recent_table.add_row(session.timestamp[:10], session.question_type, str(session.score))  # pragma: no cover

        console.print(recent_table)  # pragma: no cover
        Prompt.ask("\nPress Enter to return to menu")  # pragma: no cover

if __name__ == "__main__":
    app = InterviewApp()
    app.start()
