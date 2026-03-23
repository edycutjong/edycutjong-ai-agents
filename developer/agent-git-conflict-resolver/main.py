"""
Git Conflict Resolver Agent — parses git merge conflicts and suggests resolutions.
Usage: python main.py <file_with_conflicts>
"""
import argparse
import os
import re
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Git Conflict Resolver] Provide a file with merge conflicts to get resolution suggestions."


CONFLICT_START = re.compile(r"^<<<<<<<\s*(.*)")
CONFLICT_MID = re.compile(r"^=======")
CONFLICT_END = re.compile(r"^>>>>>>>\s*(.*)")


def parse_conflicts(content: str) -> list:
    conflicts = []
    current = None
    section = None
    for i, line in enumerate(content.splitlines(), 1):
        m_start = CONFLICT_START.match(line)
        m_mid = CONFLICT_MID.match(line)
        m_end = CONFLICT_END.match(line)
        if m_start:
            current = {"start_line": i, "ours_branch": m_start.group(1).strip(),
                        "ours": [], "theirs": [], "theirs_branch": ""}
            section = "ours"
        elif m_mid and current:
            section = "theirs"
        elif m_end and current:
            current["end_line"] = i
            current["theirs_branch"] = m_end.group(1).strip()
            conflicts.append(current)
            current = None
            section = None
        elif current and section == "ours":
            current["ours"].append(line)
        elif current and section == "theirs":
            current["theirs"].append(line)
    return conflicts


def suggest_resolution(conflict: dict) -> str:
    ours = "\n".join(conflict["ours"]).strip()
    theirs = "\n".join(conflict["theirs"]).strip()
    if not ours:
        return "ACCEPT_THEIRS"
    if not theirs:
        return "ACCEPT_OURS"
    if ours == theirs:
        return "IDENTICAL"
    ours_longer = len(ours) > len(theirs) * 1.5
    theirs_longer = len(theirs) > len(ours) * 1.5
    if ours_longer:
        return "PREFER_OURS"
    if theirs_longer:
        return "PREFER_THEIRS"
    return "MANUAL_MERGE"


def resolve_file(content: str, strategy: str = "auto") -> str:
    conflicts = parse_conflicts(content)
    if not conflicts:
        return content
    result = content
    for conflict in reversed(conflicts):
        ours_text = "\n".join(conflict["ours"])
        theirs_text = "\n".join(conflict["theirs"])
        if strategy == "ours":
            replacement = ours_text
        elif strategy == "theirs":
            replacement = theirs_text
        else:
            suggestion = suggest_resolution(conflict)
            if suggestion in ("ACCEPT_THEIRS", "PREFER_THEIRS"):
                replacement = theirs_text
            else:
                replacement = ours_text
        start_marker = f"<<<<<<< {conflict['ours_branch']}"
        end_marker = f">>>>>>> {conflict['theirs_branch']}"
        block = result[result.index(start_marker):result.index(end_marker) + len(end_marker)]
        result = result.replace(block, replacement, 1)
    return result


def format_report(conflicts: list) -> str:
    if not conflicts:
        return "✅ No merge conflicts found."
    lines = [f"⚔️  Found {len(conflicts)} conflict(s)\n"]
    for i, c in enumerate(conflicts, 1):
        suggestion = suggest_resolution(c)
        lines.append(f"  #{i} Lines {c['start_line']}-{c['end_line']}: "
                     f"{c['ours_branch']} vs {c['theirs_branch']} → {suggestion}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Git Conflict Resolver Agent")
    parser.add_argument("file", nargs="?", help="File with merge conflicts")
    parser.add_argument("--strategy", choices=["ours", "theirs", "auto"], default="auto")
    args = parser.parse_args()
    if not args.file:
        print("Git Conflict Resolver Agent\nUsage: python main.py <file>")
        sys.exit(0)
    content = open(args.file).read()
    conflicts = parse_conflicts(content)
    print(format_report(conflicts))


if __name__ == "__main__":
    main()
