"""
Dependency Updater Agent — scans Python projects for outdated pip dependencies,
updates them one by one, runs tests after each update, and rolls back on failure.
Usage: python main.py --dir <project_dir>
"""
import argparse
import json
import os
import shutil
import subprocess
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Dependency Updater] Provide a project directory to scan for outdated Python dependencies and update them safely."


def get_outdated(directory: str) -> list:
    """Get list of outdated pip packages in the given directory."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--outdated", "--format=json"],
            capture_output=True, text=True, cwd=directory, timeout=120
        )
        if result.returncode != 0:
            return []
        packages = json.loads(result.stdout)
        return packages
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        return []


def install_package(package: str, version: str, directory: str) -> tuple:
    """Install a specific version of a package. Returns (success, output)."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", f"{package}=={version}"],
            capture_output=True, text=True, cwd=directory, timeout=120
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Installation timed out"


def run_tests(test_command: str, directory: str) -> tuple:
    """Run test command. Returns (success, output)."""
    try:
        result = subprocess.run(
            test_command.split(),
            capture_output=True, text=True, cwd=directory, timeout=300
        )
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, "Tests timed out"
    except FileNotFoundError:
        return False, f"Command not found: {test_command}"


def rollback_package(package: str, old_version: str, directory: str) -> bool:
    """Roll back a package to its previous version."""
    success, _ = install_package(package, old_version, directory)
    return success


def update_dependencies(directory: str, test_command: str = "python -m pytest",
                        mode: str = "latest", ignore: list = None) -> dict:
    """Main update logic: find outdated deps, update one by one, test, rollback on failure."""
    if ignore is None:
        ignore = []

    report = {"success": [], "failed": [], "skipped": []}

    outdated = get_outdated(directory)
    if not outdated:
        return report

    for pkg_info in outdated:
        name = pkg_info.get("name", "")
        current = pkg_info.get("version", "")
        latest = pkg_info.get("latest_version", "")

        if name in ignore:
            report["skipped"].append({"package": name, "reason": "In ignore list"})
            continue

        if mode == "patch":
            # Only update if major.minor match
            cur_parts = current.split(".")
            lat_parts = latest.split(".")
            if len(cur_parts) >= 2 and len(lat_parts) >= 2:
                if cur_parts[:2] != lat_parts[:2]:
                    report["skipped"].append({"package": name, "reason": "Major/minor version change"})
                    continue
        elif mode == "minor":
            cur_parts = current.split(".")
            lat_parts = latest.split(".")
            if len(cur_parts) >= 1 and len(lat_parts) >= 1:
                if cur_parts[0] != lat_parts[0]:
                    report["skipped"].append({"package": name, "reason": "Major version change"})
                    continue

        print(f"\n🔄 Updating {name}: {current} → {latest}...")

        success, output = install_package(name, latest, directory)
        if not success:
            print(f"  ❌ Install failed for {name}")
            rollback_package(name, current, directory)
            report["failed"].append({"package": name, "version": latest, "reason": "Install failed"})
            continue

        print(f"  ✅ Installed {name}=={latest}")

        test_ok, test_output = run_tests(test_command, directory)
        if test_ok:
            print(f"  ✅ Tests passed for {name}")
            report["success"].append({"package": name, "from": current, "to": latest})
        else:
            print(f"  ❌ Tests failed — rolling back {name} to {current}")
            rollback_package(name, current, directory)
            report["failed"].append({"package": name, "version": latest, "reason": "Tests failed"})

    return report


def format_report(report: dict) -> str:
    """Format the update report."""
    lines = ["\n--- 📊 Dependency Update Report ---\n"]

    lines.append(f"  ✅ Successfully updated: {len(report['success'])}")
    lines.append(f"  ❌ Failed (rolled back): {len(report['failed'])}")
    lines.append(f"  ⏭️  Skipped: {len(report['skipped'])}")

    if report["success"]:
        lines.append("\n  Updated packages:")
        for p in report["success"]:
            lines.append(f"    - {p['package']}: {p['from']} → {p['to']}")

    if report["failed"]:
        lines.append("\n  Failed packages:")
        for p in report["failed"]:
            lines.append(f"    - {p['package']} ({p['reason']})")

    if report["skipped"]:
        lines.append("\n  Skipped packages:")
        for p in report["skipped"]:
            lines.append(f"    - {p['package']} ({p['reason']})")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Dependency Updater Agent")
    parser.add_argument("-d", "--dir", default=".", help="Directory to scan (default: .)")
    parser.add_argument("-t", "--test", default="python -m pytest",
                        help="Test command to run (default: python -m pytest)")
    parser.add_argument("-m", "--mode", choices=["latest", "minor", "patch"], default="latest",
                        help="Update mode: latest, minor, patch (default: latest)")
    parser.add_argument("-i", "--ignore", default="",
                        help="Comma-separated list of packages to ignore")
    args = parser.parse_args()

    directory = os.path.abspath(args.dir)
    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory")
        sys.exit(1)

    ignore_list = [p.strip() for p in args.ignore.split(",") if p.strip()]

    print(f"🔍 Scanning for outdated dependencies in {directory}...")
    report = update_dependencies(directory, args.test, args.mode, ignore_list)
    print(format_report(report))


if __name__ == "__main__":  # pragma: no cover
    main()
