"""
Git Workflow Agent — analyzes git history and suggests workflow improvements.
Usage: python main.py [--log N] [--check-branches]
"""
import argparse, sys, subprocess


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Git Workflow Agent] Paste git log, branch info, or describe your workflow to get improvement suggestions and best practices."


def main():
    parser = argparse.ArgumentParser(description="Analyze git workflow and suggest improvements")
    parser.add_argument("--log", type=int, default=20, help="Number of recent commits to analyze (default: 20)")
    parser.add_argument("--check-branches", action="store_true", help="List stale branches")
    args = parser.parse_args()

    try:
        log = subprocess.run(
            ["git", "log", f"--max-count={args.log}", "--format=%s", "--no-merges"],
            capture_output=True, text=True, check=True
        ).stdout.strip()
    except Exception:
        print("Git Workflow Agent\nRun inside a git repository.")
        print("Usage: python main.py [--log 20] [--check-branches]")
        sys.exit(0)

    if not log:
        print("No commits found.")
        sys.exit(0)

    lines = log.splitlines()
    print(f"\n🔀 Git Workflow Analysis ({len(lines)} commits)\n")

    conv = sum(1 for l in lines if any(l.startswith(t) for t in ["feat", "fix", "chore", "docs", "refactor", "test"]))
    print(f"  Conventional commits : {conv}/{len(lines)} ({round(conv/len(lines)*100)}%)")
    if conv / len(lines) < 0.5:
        print("  ⚠️  Less than 50% use Conventional Commits — consider enforcing with a commit linter.")
    else:
        print("  ✅ Good commit message hygiene.")

    long_msgs = [l for l in lines if len(l) > 72]
    if long_msgs:
        print(f"  ⚠️  {len(long_msgs)} commit(s) exceed 72-char subject line limit.")

    if args.check_branches:
        try:
            branches = subprocess.run(
                ["git", "branch", "--sort=-committerdate", "--format=%(refname:short)"],
                capture_output=True, text=True
            ).stdout.strip().splitlines()
            print(f"\n  Branches ({len(branches)} total): {', '.join(branches[:10])}")
        except Exception:
            pass

if __name__ == "__main__":
    main()
