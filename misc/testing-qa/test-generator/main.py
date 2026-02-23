import os
import sys
import subprocess
from dotenv import load_dotenv
from crewai import Crew, Process
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax

# Add current directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agent_config import TestGeneratorAgents, TestGeneratorTasks
from utils import setup_logging, print_banner, print_success, print_error, print_info

load_dotenv()
logger = setup_logging()
console = Console()

def run():
    print_banner()

    # Get input file
    default_file = "example_code.py"
    file_path = Prompt.ask("Enter the path to the python file to test", default=default_file)

    if not os.path.exists(file_path):
        print_error(f"File not found: {file_path}")
        return

    with open(file_path, "r") as f:
        code_content = f.read()

    # Initialize Agents and Tasks
    agents = TestGeneratorAgents()
    tasks = TestGeneratorTasks()

    code_analyst = agents.code_analyst()
    test_developer = agents.test_developer()
    qa_engineer = agents.qa_engineer()

    analyze_task = tasks.analyze_code_task(code_analyst, code_content)
    write_task = tasks.write_tests_task(test_developer)
    review_task = tasks.review_tests_task(qa_engineer)

    # Create Crew
    crew = Crew(
        agents=[code_analyst, test_developer, qa_engineer],
        tasks=[analyze_task, write_task, review_task],
        verbose=True,
        process=Process.sequential
    )

    print_info("Starting test generation process...")

    try:
        # Run Crew
        result = crew.kickoff()

        print_success("Test generation completed!")

        # Display result
        console.print("\n[bold]Generated Test Code:[/bold]\n")

        # Handle result - CrewAI returns a CrewOutput object in newer versions, or string in older
        result_str = str(result)

        syntax = Syntax(result_str, "python", theme="monokai", line_numbers=True)
        console.print(syntax)

        # Save to file
        base_name = os.path.basename(file_path)
        test_filename = f"test_{base_name}"
        save_path = os.path.join("tests", test_filename)

        if Confirm.ask(f"Save tests to {save_path}?", default=True):
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, "w") as f:
                f.write(result_str)
            print_success(f"Tests saved to {save_path}")

            # Run tests
            if Confirm.ask("Run tests now?", default=True):
                print_info("Running pytest...")
                # Ensure the current directory is in PYTHONPATH so the test can import the source module
                env = os.environ.copy()
                cwd = os.getcwd()
                env["PYTHONPATH"] = cwd + os.pathsep + env.get("PYTHONPATH", "")

                subprocess.run(["pytest", save_path, "-v"], env=env)

    except Exception as e:
        print_error(f"An error occurred: {e}")
        logger.exception("Error during execution")

if __name__ == "__main__":
    run()
