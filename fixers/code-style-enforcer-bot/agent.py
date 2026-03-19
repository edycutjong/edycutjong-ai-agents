import sys
import os
import time
from rich.prompt import Prompt

# Ensure we can import modules from the current directory
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.ui import print_header, print_success, print_error, print_warning, print_info, spinner, ask_user, print_code_block, console
from utils.config import config
from utils.gamification import gamification
from tools.checker import StyleChecker
from tools.fixer import StyleFixer
from tools.ai import ai_helper

def main():
    print_header()

    checker = StyleChecker(ignore_patterns=config.ignore_patterns)
    fixer = StyleFixer(ignore_patterns=config.ignore_patterns)

    print_info(f"Loaded config: Tone={config.tone}, Auto-fix={config.auto_fix}")
    console.print(gamification.get_stats_summary(), style="bold purple")

    while True:
        console.print("\n[bold cyan]Commands:[/bold cyan] [green]scan[/green], [green]fix[/green], [green]chat[/green], [green]stats[/green], [red]quit[/red]")
        command = Prompt.ask("What would you like to do?", choices=["scan", "fix", "chat", "stats", "quit"], default="scan")

        if command == "quit":
            print_info("Goodbye! Keep your code clean! 👋")
            break

        elif command == "stats":
            console.print(gamification.get_stats_summary(), style="bold purple")  # pragma: no cover

        elif command == "scan":
            path = ask_user("Enter path to scan (default: .):") or "."
            with spinner(f"Scanning {path}..."):
                issues = checker.scan_directory(path)

            if not issues:
                print_success("No style issues found! Great job! ✨")  # pragma: no cover
                gamification.record_clean_run()  # pragma: no cover
            else:
                print_warning(f"Found {len(issues)} issues.")
                for issue in issues[:10]:  # Show first 10
                    console.print(f"[bold yellow]{issue['path']}:{issue['row']}:{issue['col']}[/bold yellow] - {issue['code']}: {issue['text']}")
                if len(issues) > 10:
                    console.print(f"...and {len(issues) - 10} more.")  # pragma: no cover

                if ask_user("Do you want an explanation for any rule? (y/n)") == "y":
                    code = ask_user("Enter rule code (e.g. E501):")  # pragma: no cover
                    desc = next((i['text'] for i in issues if i['code'] == code), "Unknown rule")  # pragma: no cover
                    explanation = ai_helper.explain_rule(code, desc)  # pragma: no cover
                    console.print(f"[bold blue]AI Explanation:[/bold blue] {explanation}")  # pragma: no cover

        elif command == "fix":  # pragma: no cover
            path = ask_user("Enter file or directory to fix (default: .):") or "."  # pragma: no cover
            if os.path.isfile(path):  # pragma: no cover
                files = [path]  # pragma: no cover
            else:
                files = []  # pragma: no cover
                for root, _, fs in os.walk(path):  # pragma: no cover
                    for f in fs:  # pragma: no cover
                        if f.endswith(".py"):  # pragma: no cover
                            files.append(os.path.join(root, f))  # pragma: no cover

            fixed_count = 0  # pragma: no cover
            with spinner(f"Fixing {len(files)} files..."):  # pragma: no cover
                for filepath in files:  # pragma: no cover
                    if fixer.fix_file(filepath):  # pragma: no cover
                        fixed_count += 1  # pragma: no cover

            if fixed_count > 0:  # pragma: no cover
                print_success(f"Fixed {fixed_count} files!")  # pragma: no cover
                gamification.record_fix(fixed_count)  # pragma: no cover
            else:
                print_info("No files needed fixing or fixes failed.")  # pragma: no cover

        elif command == "chat":  # pragma: no cover
            print_info("Chat with the Style Bot! (Type 'exit' to go back)")  # pragma: no cover
            while True:  # pragma: no cover
                user_input = ask_user("You:")  # pragma: no cover
                if user_input.lower() in ["exit", "quit"]:  # pragma: no cover
                    break  # pragma: no cover

                # Simple chat handling - could be expanded
                if "vibe" in user_input.lower():  # pragma: no cover
                    code = ask_user("Paste code snippet to check vibe:")  # pragma: no cover
                    response = ai_helper.check_vibe(code)  # pragma: no cover
                elif "explain" in user_input.lower():  # pragma: no cover
                    rule = ask_user("Which rule code?")  # pragma: no cover
                    response = ai_helper.explain_rule(rule, "User asked for explanation")  # pragma: no cover
                else:
                    # Generic chat fallback to AI
                    if ai_helper.llm:  # pragma: no cover
                        from langchain_core.messages import HumanMessage  # pragma: no cover
                        response = ai_helper.llm.invoke([HumanMessage(content=user_input)]).content  # pragma: no cover
                    else:
                        response = "I can only explain rules or check vibes right now (Mocked AI)."  # pragma: no cover

                console.print(f"[bold magenta]Bot:[/bold magenta] {response}")  # pragma: no cover

if __name__ == "__main__":
    try:  # pragma: no cover
        main()  # pragma: no cover
    except KeyboardInterrupt:  # pragma: no cover
        print("\nGoodbye!")  # pragma: no cover
