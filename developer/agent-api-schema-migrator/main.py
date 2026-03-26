"""
API Schema Migrator Agent — detects breaking changes between API schema versions
and generates migration guides.
Usage: python main.py <old_schema.json> <new_schema.json>
"""
import argparse
import json
import sys
import os


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[API Schema Migrator] Provide two API schema versions (JSON/OpenAPI) to detect breaking changes and generate a migration guide."


def load_schema(path: str) -> dict:
    if not os.path.isfile(path):
        return json.loads(path)
    with open(path) as f:
        return json.load(f)


def find_removed_fields(old: dict, new: dict, path: str = "") -> list:
    issues = []
    for key in old:
        full = f"{path}.{key}" if path else key
        if key not in new:
            issues.append({"type": "REMOVED", "path": full, "severity": "BREAKING"})
        elif isinstance(old[key], dict) and isinstance(new.get(key), dict):
            issues.extend(find_removed_fields(old[key], new[key], full))
    return issues


def find_added_fields(old: dict, new: dict, path: str = "") -> list:
    additions = []
    for key in new:
        full = f"{path}.{key}" if path else key
        if key not in old:
            additions.append({"type": "ADDED", "path": full, "severity": "SAFE"})
        elif isinstance(new[key], dict) and isinstance(old.get(key), dict):
            additions.extend(find_added_fields(old[key], new[key], full))
    return additions


def find_type_changes(old: dict, new: dict, path: str = "") -> list:
    changes = []
    for key in old:
        if key not in new:
            continue
        full = f"{path}.{key}" if path else key
        if type(old[key]) != type(new[key]):
            changes.append({
                "type": "TYPE_CHANGE", "path": full, "severity": "BREAKING",
                "old_type": type(old[key]).__name__, "new_type": type(new[key]).__name__
            })
        elif isinstance(old[key], dict) and isinstance(new[key], dict):
            changes.extend(find_type_changes(old[key], new[key], full))
    return changes


def compare_schemas(old: dict, new: dict) -> dict:
    removed = find_removed_fields(old, new)
    added = find_added_fields(old, new)
    type_changes = find_type_changes(old, new)
    all_issues = removed + added + type_changes
    breaking = [i for i in all_issues if i["severity"] == "BREAKING"]
    return {
        "total_changes": len(all_issues),
        "breaking_changes": len(breaking),
        "changes": all_issues,
        "migration_required": len(breaking) > 0,
    }


def generate_migration_guide(result: dict) -> str:
    lines = ["# Migration Guide\n"]
    if not result["migration_required"]:
        lines.append("✅ No breaking changes detected — safe to upgrade.\n")
        return "\n".join(lines)
    lines.append(f"⚠️  {result['breaking_changes']} breaking change(s) found.\n")
    for c in result["changes"]:
        icon = "🔴" if c["severity"] == "BREAKING" else "🟢"
        detail = f" ({c.get('old_type', '')} → {c.get('new_type', '')})" if c["type"] == "TYPE_CHANGE" else ""
        lines.append(f"  {icon} [{c['type']}] {c['path']}{detail}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="API Schema Migrator")
    parser.add_argument("old", nargs="?", help="Old schema file (JSON)")
    parser.add_argument("new", nargs="?", help="New schema file (JSON)")
    args = parser.parse_args()
    if not args.old or not args.new:
        print("API Schema Migrator Agent\nUsage: python main.py <old.json> <new.json>")
        sys.exit(0)
    old_schema = load_schema(args.old)
    new_schema = load_schema(args.new)
    result = compare_schemas(old_schema, new_schema)
    print(generate_migration_guide(result))


if __name__ == "__main__":  # pragma: no cover
    main()
