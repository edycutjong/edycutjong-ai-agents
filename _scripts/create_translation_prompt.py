"""
Script to identify agents missing from agent_translations.json
and generate an LLM prompt to translate them.
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
TRANSLATIONS_FILE = BASE_DIR / "_scripts" / "agent_translations.json"

TARGET_LOCALES = ["id", "zh", "es", "pt", "ja", "ko", "de", "fr", "ru", "ar", "hi"]

ACRONYMS = {"ai", "api", "css", "csv", "dns", "html", "http", "ip", "json",
            "jwt", "llm", "ml", "npm", "pdf", "qa", "rag", "rss", "seo",
            "sql", "ssh", "ssl", "svg", "ui", "url", "ux", "xml", "yaml",
            "sop", "cors", "cli", "crm", "readme", "ci", "cd",
            "prompt", "slug", "regex", "graphql", "oauth", "webhook",
            "postman", "crud", "dockerfile", "monorepo", "ci/cd"}

def slug_to_name(slug: str) -> str:
    words = slug.replace("-", " ").replace("_", " ").split()
    return " ".join(w.upper() if w.lower() in ACRONYMS else w.capitalize() for w in words)

def extract_desc(agents_md: Path) -> str:
    try:
        content = agents_md.read_text(encoding="utf-8")
        for line in content.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("---") and len(line) > 20:
                clean = line.lstrip("- *>").strip()
                return clean[:200]
    except Exception:
        pass
    return ""

def discover_agents():
    agents = {}
    for cat_dir in sorted(BASE_DIR.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith(('.', '_')):
            continue
        if cat_dir.name in ('__pycache__', 'node_modules', '.git'):
            continue
        cat_name = cat_dir.name
        if cat_name == "misc":
            for sub_cat in sorted(cat_dir.iterdir()):
                if not sub_cat.is_dir() or sub_cat.name.startswith('.'):
                    continue
                for agent_dir in sorted(sub_cat.iterdir()):
                    if not agent_dir.is_dir():
                        continue
                    main_py = agent_dir / "main.py"
                    agents_md = agent_dir / "AGENTS.md"
                    app_py = agent_dir / "app.py"
                    if main_py.exists() or agents_md.exists() or app_py.exists():
                        desc = extract_desc(agents_md) if agents_md.exists() else ""
                        agents[f"misc/{sub_cat.name}/{agent_dir.name}"] = {
                            "name": slug_to_name(agent_dir.name), "description": desc}
            continue
        for agent_dir in sorted(cat_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith('.'):
                continue
            main_py = agent_dir / "main.py"
            agents_md = agent_dir / "AGENTS.md"
            app_py = agent_dir / "app.py"
            if main_py.exists() or agents_md.exists() or app_py.exists():
                desc = extract_desc(agents_md) if agents_md.exists() else ""
                agents[f"{cat_name}/{agent_dir.name}"] = {
                    "name": slug_to_name(agent_dir.name), "description": desc}
    return agents

def main():
    if not TRANSLATIONS_FILE.exists():
        print(f"Error: {TRANSLATIONS_FILE} not found.")
        return

    with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as f:
        translations = json.load(f)

    # discover_agents returns dict like: {"category/slug": {"name": "...", "description": "..."}}
    agents = discover_agents()

    missing_agents = {}
    for key, data in agents.items():
        if key not in translations:
            missing_agents[key] = data

    if not missing_agents:
        print("All agents are already in agent_translations.json! No missing translations.")
        return

    print(f"Found {len(missing_agents)} missing agents.\n")
    print("=================== PROMPT ===================\n")
    print("Please translate the following app names and descriptions into these languages:")
    print(", ".join(TARGET_LOCALES) + " (and include the original 'en' as well).")
    print("\nPlease return the result as a valid JSON object matching this exact structure:")
    print("""{
  "category/agent-slug": {
    "id": { "name": "...", "description": "..." },
    "zh": { "name": "...", "description": "..." },
    "es": { "name": "...", "description": "..." },
    "pt": { "name": "...", "description": "..." },
    "ja": { "name": "...", "description": "..." },
    "ko": { "name": "...", "description": "..." },
    "de": { "name": "...", "description": "..." },
    "fr": { "name": "...", "description": "..." },
    "ru": { "name": "...", "description": "..." },
    "ar": { "name": "...", "description": "..." },
    "hi": { "name": "...", "description": "..." },
    "en": { "description": "English description" }
  }
}""")
    print("\nHere are the new apps to translate (provided in English):\n")
    
    source_data = {}
    for key, data in missing_agents.items():
        source_data[key] = {
            "name": data.get("name", ""),
            "description": data.get("description", "")
        }
    
    print(json.dumps(source_data, indent=2, ensure_ascii=False))
    print("\n==============================================\n")

if __name__ == "__main__":
    main()
