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
            console.print(gamification.get_stats_summary(), style="bold purple")

        elif command == "scan":
            path = ask_user("Enter path to scan (default: .):") or "."
            with spinner(f"Scanning {path}..."):
                issues = checker.scan_directory(path)

            if not issues:
                print_success("No style issues found! Great job! ✨")
                gamification.record_clean_run()
            else:
                print_warning(f"Found {len(issues)} issues.")
                for issue in issues[:10]:  # Show first 10
                    console.print(f"[bold yellow]{issue['path']}:{issue['row']}:{issue['col']}[/bold yellow] - {issue['code']}: {issue['text']}")
                if len(issues) > 10:
                    console.print(f"...and {len(issues) - 10} more.")

                if ask_user("Do you want an explanation for any rule? (y/n)") == "y":
                    code = ask_user("Enter rule code (e.g. E501):")
                    desc = next((i['text'] for i in issues if i['code'] == code), "Unknown rule")
                    explanation = ai_helper.explain_rule(code, desc)
                    console.print(f"[bold blue]AI Explanation:[/bold blue] {explanation}")

        elif command == "fix":
            path = ask_user("Enter file or directory to fix (default: .):") or "."
            if os.path.isfile(path):
                files = [path]
            else:
                files = []
                for root, _, fs in os.walk(path):
                    for f in fs:
                        if f.endswith(".py"):
                            files.append(os.path.join(root, f))

            fixed_count = 0
            with spinner(f"Fixing {len(files)} files..."):
                for filepath in files:
                    if fixer.fix_file(filepath):
                        fixed_count += 1

            if fixed_count > 0:
                print_success(f"Fixed {fixed_count} files!")
                gamification.record_fix(fixed_count)
            else:
                print_info("No files needed fixing or fixes failed.")

        elif command == "chat":
            print_info("Chat with the Style Bot! (Type 'exit' to go back)")
            while True:
                user_input = ask_user("You:")
                if user_input.lower() in ["exit", "quit"]:
                    break

                # Simple chat handling - could be expanded
                if "vibe" in user_input.lower():
                    code = ask_user("Paste code snippet to check vibe:")
                    response = ai_helper.check_vibe(code)
                elif "explain" in user_input.lower():
                    rule = ask_user("Which rule code?")
                    response = ai_helper.explain_rule(rule, "User asked for explanation")
                else:
                    # Generic chat fallback to AI
                    if ai_helper.llm:
                        from langchain_core.messages import HumanMessage
                        response = ai_helper.llm.invoke([HumanMessage(content=user_input)]).content
                    else:
                        response = "I can only explain rules or check vibes right now (Mocked AI)."

                console.print(f"[bold magenta]Bot:[/bold magenta] {response}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")
