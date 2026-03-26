"""
License Scanner Agent — scans dependencies for license types and flags incompatibilities.
Usage: python main.py <project_dir>
"""
import argparse
import json
import os
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[License Scanner] Provide a project directory to scan dependencies for license compliance."


COPYLEFT = {"GPL-2.0", "GPL-3.0", "AGPL-3.0", "LGPL-2.1", "LGPL-3.0", "MPL-2.0", "EUPL-1.2",
            "GPL-2.0-only", "GPL-3.0-only", "AGPL-3.0-only", "GPL-2.0-or-later", "GPL-3.0-or-later"}
PERMISSIVE = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "Unlicense",
              "0BSD", "CC0-1.0", "Zlib", "BlueOak-1.0.0"}


def scan_npm(project_dir: str) -> list:
    nm = os.path.join(project_dir, "node_modules")
    results = []
    if not os.path.isdir(nm):
        return results
    for pkg in os.listdir(nm):
        if pkg.startswith("."):
            continue
        pkg_json = os.path.join(nm, pkg, "package.json")
        if not os.path.isfile(pkg_json):
            continue
        try:
            data = json.load(open(pkg_json))
            license_val = data.get("license", "UNKNOWN")
            if isinstance(license_val, dict):
                license_val = license_val.get("type", "UNKNOWN")
            results.append({"package": data.get("name", pkg), "license": str(license_val),
                            "version": data.get("version", "?")})
        except (json.JSONDecodeError, OSError):
            results.append({"package": pkg, "license": "PARSE_ERROR", "version": "?"})
    return results


def scan_pip(project_dir: str) -> list:
    results = []
    req = os.path.join(project_dir, "requirements.txt")
    if not os.path.isfile(req):
        return results
    for line in open(req).read().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        pkg = line.split("==")[0].split(">=")[0].split("<=")[0].split("<")[0].split(">")[0].strip()
        results.append({"package": pkg, "license": "NEEDS_CHECK", "version": "?"})
    return results


def check_compatibility(deps: list, project_license: str = "MIT") -> list:
    issues = []
    for dep in deps:
        lic = dep["license"].upper().replace(" ", "-")
        if any(cl.upper() in lic for cl in COPYLEFT):
            issues.append({**dep, "issue": "COPYLEFT_IN_PERMISSIVE",
                           "message": f"Copyleft license '{dep['license']}' incompatible with {project_license}"})
        elif dep["license"] in ("UNKNOWN", "PARSE_ERROR", "NEEDS_CHECK"):
            issues.append({**dep, "issue": "UNKNOWN_LICENSE",
                           "message": f"License unknown — manual review needed"})
    return issues


def format_report(deps: list, issues: list) -> str:
    lines = [f"📜 License Scan — {len(deps)} packages scanned\n"]
    if not issues:
        lines.append("✅ All licenses are compatible.")
    else:
        lines.append(f"⚠️  {len(issues)} issue(s) found:\n")
        for issue in issues:
            icon = "🔴" if issue["issue"] == "COPYLEFT_IN_PERMISSIVE" else "🟡"
            lines.append(f"  {icon} {issue['package']}@{issue['version']}: {issue['message']}")
    # Summary
    from collections import Counter
    lic_counts = Counter(d["license"] for d in deps)
    lines.append("\n  License distribution:")
    for lic, count in lic_counts.most_common(10):
        lines.append(f"    - {lic}: {count}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="License Scanner Agent")
    parser.add_argument("directory", nargs="?", help="Project directory to scan")
    parser.add_argument("--license", default="MIT", help="Project license (default: MIT)")
    args = parser.parse_args()
    if not args.directory:
        print("License Scanner Agent\nUsage: python main.py <project_dir>")
        sys.exit(0)
    deps = scan_npm(args.directory) + scan_pip(args.directory)
    if not deps:
        print("No dependencies found to scan.")
        sys.exit(0)
    issues = check_compatibility(deps, args.license)
    print(format_report(deps, issues))


if __name__ == "__main__":  # pragma: no cover
    main()
