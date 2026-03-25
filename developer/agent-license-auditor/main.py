"""
License Auditor Agent — audits Python project dependencies for license compliance,
flags incompatible licenses, and generates reports in Markdown, JSON, or CSV.
Usage: python main.py --dir <project_dir>
"""
import argparse
import csv
import io
import json
import os
import sys

try:
    from importlib.metadata import distributions, PackageNotFoundError
except ImportError:
    from importlib_metadata import distributions, PackageNotFoundError


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[License Auditor] Provide a project directory to audit dependencies for license compliance."


def normalize_license(license_str) -> str:
    """Normalize license value to a clean string."""
    if license_str is None:
        return "UNKNOWN"
    if isinstance(license_str, list):
        return ", ".join(license_str)
    s = str(license_str).strip()
    return s if s else "UNKNOWN"


def check_blocked(license_str: str, block_list: list) -> bool:
    """Check if a license string matches any blocked license."""
    upper = license_str.upper()
    return any(b.upper() in upper for b in block_list if b)


def get_installed_licenses() -> list:
    """Get license info for all installed packages using importlib.metadata."""
    results = []
    seen = set()
    for dist in distributions():
        name = dist.metadata.get("Name", "unknown")
        if name in seen:
            continue
        seen.add(name)

        version = dist.metadata.get("Version", "?")
        license_val = dist.metadata.get("License", "")
        home_page = dist.metadata.get("Home-page", "N/A")
        author = dist.metadata.get("Author", "N/A")

        # Some packages use classifiers instead of License field
        if not license_val or license_val == "UNKNOWN":
            classifiers = dist.metadata.get_all("Classifier") or []
            lic_classifiers = [
                c.split(" :: ")[-1] for c in classifiers
                if c.startswith("License ::")
            ]
            if lic_classifiers:
                license_val = ", ".join(lic_classifiers)

        results.append({
            "package": f"{name}@{version}",
            "name": name,
            "version": version,
            "license": normalize_license(license_val),
            "repository": home_page or "N/A",
            "author": author or "N/A",
        })

    return sorted(results, key=lambda x: x["package"].lower())


def audit_licenses(packages: list, block_list: list, allow_list: list) -> tuple:
    """Audit packages against block/allow lists. Returns (report_data, blocked_count, unknown_count)."""
    report_data = []
    blocked_count = 0
    unknown_count = 0

    for pkg in packages:
        lic = pkg["license"]
        status = "OK"

        if lic in ("UNKNOWN", "") or "UNKNOWN" in lic:
            status = "MISSING_LICENSE"
            unknown_count += 1
        elif block_list and check_blocked(lic, block_list):
            status = "BLOCKED_LICENSE"
            blocked_count += 1
        elif allow_list and not check_blocked(lic, allow_list):
            status = "NOT_ALLOWED_LICENSE"
            blocked_count += 1

        report_data.append({
            "package": pkg["package"],
            "license": lic,
            "status": status,
            "repository": pkg["repository"],
            "author": pkg["author"],
        })

    return report_data, blocked_count, unknown_count


def format_markdown(report_data: list) -> str:
    """Format report as Markdown."""
    lines = [
        "# Third-Party Licenses\n",
        "This document describes the licenses of the third-party dependencies used in this project.\n",
        "| Package | License | Status | Repository |",
        "|---|---|---|---|",
    ]
    for r in report_data:
        lines.append(f"| {r['package']} | {r['license']} | {r['status']} | {r['repository']} |")
    return "\n".join(lines) + "\n"


def format_csv(report_data: list) -> str:
    """Format report as CSV string."""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["package", "license", "status", "repository"])
    writer.writeheader()
    for r in report_data:
        writer.writerow({k: r[k] for k in ["package", "license", "status", "repository"]})
    return output.getvalue()


def print_console_report(report_data: list, blocked_count: int, unknown_count: int):
    """Print a colored console report."""
    print("\n--- 📜 License Audit Report ---\n")

    for r in report_data:
        if r["status"] != "OK":
            icon = "⛔" if "BLOCKED" in r["status"] or "NOT_ALLOWED" in r["status"] else "⚠️"
            print(f"  {icon} {r['package']}: {r['status']} ({r['license']})")

    if blocked_count == 0 and unknown_count == 0:
        print("  ✅ All dependencies align with license policies (0 blocked or unknown licenses found).\n")
    else:
        print(f"\n  ⚠️  Found {unknown_count} packages with unknown licenses.")
        print(f"  ⛔ Found {blocked_count} packages with blocked licenses.\n")


def main():
    parser = argparse.ArgumentParser(description="License Auditor Agent")
    parser.add_argument("-d", "--dir", default=".", help="Directory to scan (default: .)")
    parser.add_argument("-o", "--out", default="THIRD_PARTY_LICENSES.md",
                        help="Output file path (default: THIRD_PARTY_LICENSES.md)")
    parser.add_argument("-f", "--format", choices=["md", "json", "csv"], default="md",
                        help="Report format: md, json, csv (default: md)")
    parser.add_argument("-a", "--allow", default="",
                        help="Comma-separated allowed licenses")
    parser.add_argument("-b", "--block", default="GPL,AGPL",
                        help="Comma-separated blocked licenses (default: GPL,AGPL)")
    parser.add_argument("--fail-on-blocked", action="store_true", default=True,
                        help="Exit with code 1 if blocked license found")
    args = parser.parse_args()

    block_list = [s.strip() for s in args.block.split(",") if s.strip()]
    allow_list = [s.strip() for s in args.allow.split(",") if s.strip()]

    print("🔍 Scanning installed packages...")
    packages = get_installed_licenses()
    print(f"  Found {len(packages)} packages.\n")

    report_data, blocked_count, unknown_count = audit_licenses(packages, block_list, allow_list)
    print_console_report(report_data, blocked_count, unknown_count)

    # Write output file
    out_path = os.path.abspath(args.out)
    fmt = args.format.lower()

    if fmt == "json":
        with open(out_path, "w") as f:
            json.dump(report_data, f, indent=2)
    elif fmt == "csv":
        with open(out_path, "w", newline="") as f:
            f.write(format_csv(report_data))
    else:
        with open(out_path, "w") as f:
            f.write(format_markdown(report_data))

    print(f"📄 Report saved to {out_path}")

    if blocked_count > 0 and args.fail_on_blocked:
        print("\n⛔ Audit failed due to blocked licenses!")
        sys.exit(1)


if __name__ == "__main__":
    main()
