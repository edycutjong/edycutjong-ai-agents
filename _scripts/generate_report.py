#!/usr/bin/env python3
import os
import json
import glob

# Assumes script is run from apps/agents directory like `python _scripts/generate_report.py`
base_dir = "."
translations_file = "_scripts/agent_translations.json"
coverage_file = "_scripts/coverage.json"
report_path = "agent_status_report.md"

# Load JSON data
try:
    with open(translations_file, "r") as f:
        translations = json.load(f)
except Exception:
    translations = {}

try:
    with open(coverage_file, "r") as f:
        cov_data = json.load(f)
        coverage = {item["agent"].lstrip("./"): item["coverage"] for item in cov_data.get("agents", [])}
except Exception:
    coverage = {}

# Find agents
agent_dirs_raw = []
for r, dirs, files in os.walk(base_dir):
    # skip hidden/unwanted
    if ".git" in r or "venv" in r or "__pycache__" in r or "_scripts" in r or "node_modules" in r:
        continue
    # skip known non-agent subdirectories
    if "/fixtures/" in r or r.endswith("/fixtures"):
        continue
    if "AGENTS.md" in files or "main.py" in files or "app.py" in files:
        # Use relative path skipping the internal './'
        path_clean = r.lstrip("./")
        # e.g., 'misc/ai-frameworks/autogen-agent' or 'ai-ml-ops/embedding-explorer'
        parts = path_clean.split("/")
        if len(parts) >= 2:
            agent = parts[-1]
            category = parts[-2]
            trans_key = f"{category}/{agent}"
            agent_dirs_raw.append((trans_key, r, path_clean))

# Deduplicate: remove entries whose path is a subdirectory of another discovered agent
# This prevents false positives from nested agent/, ui/, and duplicate-named subdirs
agent_paths = sorted(set(item[1] for item in agent_dirs_raw))
nested_paths = set()
for i, p1 in enumerate(agent_paths):
    for p2 in agent_paths:
        if p1 != p2 and p2.startswith(p1 + "/"):
            nested_paths.add(p2)

agent_dirs = [(k, p, pc) for k, p, pc in agent_dirs_raw if p not in nested_paths]

total = len(agent_dirs)
built_agents = []
spec_only_agents = []
invalid_folders = []

for trans_key, path, path_clean in sorted(agent_dirs):
    spec = os.path.exists(os.path.join(path, "AGENTS.md"))
    build_files = glob.glob(os.path.join(path, "*.py"))
    build = any(f.endswith("main.py") or f.endswith("app.py") for f in build_files)
    
    test_files = glob.glob(os.path.join(path, "test_*.py")) + glob.glob(os.path.join(path, "tests", "test_*.py"))
    tests = len(test_files) > 0
    
    trans = trans_key in translations
    # Try trans_key first (e.g. "ai-frameworks/autogen-agent"),
    # then full path (e.g. "misc/ai-frameworks/autogen-agent")
    cov = coverage.get(trans_key, coverage.get(path_clean, "N/A"))
    
    if not spec and not build:
        invalid_folders.append(trans_key)
    elif spec and not build:
        spec_only_agents.append(trans_key)
    else:
        built_agents.append({
            "id": trans_key,
            "tests": "✅" if tests else "❌",
            "trans": "✅" if trans else "❌",
            "cov": str(cov) + "%" if cov != "N/A" else "N/A"
        })

print(f"Generating report to {report_path}...")

with open(report_path, "w", encoding="utf-8") as f:
    f.write("# 🤖 AI Agents Status Report\n\n")
    f.write(f"**Total Agent Directories Analyzed:** {total - len(invalid_folders)}\n\n")
    
    f.write("## 🏗️ Spec Only (Not Built Yet)\n")
    f.write("These agents have an `AGENTS.md` specification but are missing their main executable (`main.py`/`app.py`).\n\n")
    if spec_only_agents:
        for a in spec_only_agents:
            f.write(f"- `{a}`\n")
    else:
        f.write("*All agents are fully built!*\n")
        
    f.write("\n## ✅ Fully Built Agents\n")
    f.write("These agents have implementation code. Below is their compliance with tests and translations.\n\n")
    f.write("| Agent | Tests | Translations | Coverage |\n")
    f.write("|-------|-------|--------------|----------|\n")
    for a in built_agents:
        f.write(f"| `{a['id']}` | {a['tests']} | {a['trans']} | {a['cov']} |\n")

    if invalid_folders:
        f.write("\n## 📁 Ignored Category Folders\n")
        f.write("These paths were ignored as they don't contain agent definition files:\n")
        for inv in invalid_folders:
            f.write(f"- `{inv}`\n")

print("Report successfully generated!")
