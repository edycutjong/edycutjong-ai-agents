"""
Docker Slimmer Agent — analyzes Dockerfiles and suggests optimizations to reduce image size.
Usage: python main.py <Dockerfile>
"""
import argparse
import os
import re
import sys


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[Docker Slimmer] Provide a Dockerfile to get optimization suggestions for smaller images."


CHECKS = [
    (r"^FROM\s+(?!.*:.*-(?:slim|alpine|distroless))(?!.*scratch)", "LARGE_BASE",
     "Use slim/alpine base image to reduce size"),
    (r"^RUN\s+apt-get\s+install(?!.*--no-install-recommends)", "NO_RECOMMENDS",
     "Add --no-install-recommends to apt-get install"),
    (r"^COPY\s+\.\s+\.", "COPY_ALL",
     "COPY . . copies everything — use .dockerignore or selective COPY"),
    (r"^RUN\s+pip\s+install(?!.*--no-cache-dir)", "PIP_CACHE",
     "Add --no-cache-dir to pip install"),
    (r"^RUN\s+npm\s+install(?!.*--production)(?!.*ci)", "NPM_DEV",
     "Use npm ci --production to skip devDependencies"),
    (r"^RUN\s+curl\b.*&&[^&]*$", "LAYER_MERGE",
     "Merge download + install into single RUN to reduce layers"),
]


def analyze_dockerfile(content: str) -> list:
    findings = []
    lines = content.splitlines()
    has_multistage = sum(1 for l in lines if re.match(r"^FROM\s+", l, re.I)) > 1
    run_count = sum(1 for l in lines if re.match(r"^RUN\s+", l, re.I))

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        for pattern, code, msg in CHECKS:
            if re.match(pattern, stripped, re.IGNORECASE):
                findings.append({"line": i, "code": code, "message": msg, "content": stripped[:60]})

    if not has_multistage and run_count > 3:
        findings.append({"line": 0, "code": "MULTISTAGE",
                         "message": "Consider multi-stage build to separate build and runtime",
                         "content": ""})

    if run_count > 5:
        findings.append({"line": 0, "code": "TOO_MANY_LAYERS",
                         "message": f"{run_count} RUN instructions — merge where possible to reduce layers",
                         "content": ""})

    has_cleanup = any("rm -rf" in l and ("apt" in l or "cache" in l) for l in lines)
    if not has_cleanup and any("apt-get install" in l for l in lines):
        findings.append({"line": 0, "code": "NO_CLEANUP",
                         "message": "Add 'rm -rf /var/lib/apt/lists/*' after apt-get install",
                         "content": ""})

    return findings


def format_report(findings: list) -> str:
    if not findings:
        return "✅ Dockerfile looks optimized — no suggestions."
    lines = [f"🐳 Docker Slimmer — {len(findings)} optimization(s)\n"]
    for f in findings:
        loc = f"L{f['line']}" if f["line"] else "General"
        lines.append(f"  ⚡ [{f['code']}] {loc}: {f['message']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Docker Slimmer Agent")
    parser.add_argument("dockerfile", nargs="?", help="Path to Dockerfile")
    args = parser.parse_args()
    if not args.dockerfile:
        print("Docker Slimmer Agent\nUsage: python main.py <Dockerfile>")
        sys.exit(0)
    if not os.path.isfile(args.dockerfile):
        print(f"Error: {args.dockerfile} not found")
        sys.exit(1)
    content = open(args.dockerfile).read()
    findings = analyze_dockerfile(content)
    print(format_report(findings))


if __name__ == "__main__":  # pragma: no cover
    main()
