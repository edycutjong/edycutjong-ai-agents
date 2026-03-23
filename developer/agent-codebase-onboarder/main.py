"""
Codebase Onboarder Agent — analyzes a project and generates an onboarding guide.
Usage: python main.py <project_dir>
"""
import argparse
import os
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Codebase Onboarder] Provide a project directory path to generate an onboarding guide."


FILE_TYPES = {
    ".py": "Python", ".ts": "TypeScript", ".js": "JavaScript", ".go": "Go",
    ".rs": "Rust", ".java": "Java", ".rb": "Ruby", ".swift": "Swift",
    ".kt": "Kotlin", ".cpp": "C++", ".c": "C", ".cs": "C#",
}


def scan_project(root: str) -> dict:
    stats = {"files": 0, "dirs": 0, "languages": {}, "key_files": [], "total_lines": 0}
    key_file_names = {"README.md", "package.json", "Makefile", "Dockerfile",
                      "requirements.txt", "Cargo.toml", "go.mod", ".env.example",
                      "tsconfig.json", "setup.py", "pyproject.toml"}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".git", "__pycache__", "venv", ".venv", "dist"}]
        stats["dirs"] += len(dirnames)
        for f in filenames:
            stats["files"] += 1
            ext = os.path.splitext(f)[1].lower()
            if ext in FILE_TYPES:
                lang = FILE_TYPES[ext]
                stats["languages"][lang] = stats["languages"].get(lang, 0) + 1
            if f in key_file_names:
                stats["key_files"].append(os.path.relpath(os.path.join(dirpath, f), root))
            fp = os.path.join(dirpath, f)
            try:
                with open(fp, "r", errors="ignore") as fh:
                    stats["total_lines"] += sum(1 for _ in fh)
            except (OSError, UnicodeDecodeError):
                pass
    return stats


def detect_framework(stats: dict, root: str) -> list:
    frameworks = []
    pkg = os.path.join(root, "package.json")
    if os.path.isfile(pkg):
        try:
            content = open(pkg).read()
            for fw in ["react", "vue", "angular", "next", "express", "fastify", "nest"]:
                if fw in content.lower():
                    frameworks.append(fw.capitalize())
        except OSError:
            pass
    req = os.path.join(root, "requirements.txt")
    if os.path.isfile(req):
        try:
            content = open(req).read()
            for fw in ["django", "flask", "fastapi", "celery"]:
                if fw in content.lower():
                    frameworks.append(fw.capitalize())
        except OSError:
            pass
    return frameworks


def generate_guide(stats: dict, frameworks: list) -> str:
    lines = ["# 🚀 Onboarding Guide\n"]
    lines.append(f"**Files:** {stats['files']} | **Directories:** {stats['dirs']} | **Lines:** {stats['total_lines']:,}\n")
    if stats["languages"]:
        top = sorted(stats["languages"].items(), key=lambda x: -x[1])
        lines.append("## Languages")
        for lang, count in top[:5]:
            lines.append(f"  - {lang}: {count} files")
    if frameworks:
        lines.append(f"\n## Frameworks Detected\n  {', '.join(frameworks)}")
    if stats["key_files"]:
        lines.append("\n## Key Files")
        for f in sorted(stats["key_files"]):
            lines.append(f"  - {f}")
    lines.append("\n## Getting Started\n  1. Clone the repository\n  2. Install dependencies\n  3. Review key files above\n  4. Run the development server")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Codebase Onboarder Agent")
    parser.add_argument("directory", nargs="?", help="Project directory to analyze")
    args = parser.parse_args()
    if not args.directory:
        print("Codebase Onboarder Agent\nUsage: python main.py <project_dir>")
        sys.exit(0)
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a directory")
        sys.exit(1)
    stats = scan_project(args.directory)
    frameworks = detect_framework(stats, args.directory)
    print(generate_guide(stats, frameworks))


if __name__ == "__main__":
    main()
