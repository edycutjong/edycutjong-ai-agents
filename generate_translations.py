"""
One-time script to generate agent_translations.json
Uses raw urllib to call Google Translate API — zero dependencies.
Run: python generate_translations.py
"""

import json
import time
import sys
import urllib.request
import urllib.parse
from pathlib import Path

TARGET_LOCALES = ["id", "zh-CN", "es", "pt", "ja", "ko", "de", "fr", "ru", "ar", "hi"]
LOCALE_MAP = {"zh-CN": "zh"}

BASE_DIR = Path(__file__).parent

ACRONYMS = {"ai", "api", "css", "csv", "dns", "html", "http", "ip", "json",
            "jwt", "llm", "ml", "npm", "pdf", "qa", "rag", "rss", "seo",
            "sql", "ssh", "ssl", "svg", "ui", "url", "ux", "xml", "yaml",
            "sop", "cors", "cli", "crm", "readme", "ci", "cd"}


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
                    if main_py.exists() or agents_md.exists():
                        desc = extract_desc(agents_md) if agents_md.exists() else ""
                        agents[f"misc/{sub_cat.name}/{agent_dir.name}"] = {
                            "name": slug_to_name(agent_dir.name), "description": desc}
            continue
        for agent_dir in sorted(cat_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith('.'):
                continue
            main_py = agent_dir / "main.py"
            agents_md = agent_dir / "AGENTS.md"
            if main_py.exists() or agents_md.exists():
                desc = extract_desc(agents_md) if agents_md.exists() else ""
                agents[f"{cat_name}/{agent_dir.name}"] = {
                    "name": slug_to_name(agent_dir.name), "description": desc}
    return agents


def google_translate(text: str, target_lang: str) -> str:
    """Translate using Google's free translate API via urllib."""
    if not text or not text.strip():
        return ""
    url = "https://translate.googleapis.com/translate_a/single"
    params = urllib.parse.urlencode({
        "client": "gtx",
        "sl": "en",
        "tl": target_lang,
        "dt": "t",
        "q": text,
    })
    full_url = f"{url}?{params}"
    req = urllib.request.Request(full_url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            # Response structure: [[["translated text", "source text", ...]]]
            translated = "".join(part[0] for part in data[0] if part[0])
            return translated
        except Exception as e:
            if attempt == 2:
                return text  # Fallback to English
            time.sleep(0.5 * (attempt + 1))
    return text


def main():
    print("🔍 Discovering agents...")
    agents = discover_agents()
    keys = list(agents.keys())
    print(f"   Found {len(agents)} agents\n")

    translations = {k: {} for k in keys}
    total = len(keys) * len(TARGET_LOCALES)
    done = 0

    for lang in TARGET_LOCALES:
        our_locale = LOCALE_MAP.get(lang, lang)
        print(f"🌐 {lang} → {our_locale}")

        for i, key in enumerate(keys):
            agent = agents[key]
            name_tr = google_translate(agent["name"], lang)
            desc_tr = google_translate(agent["description"], lang)

            translations[key][our_locale] = {
                "name": name_tr,
                "description": desc_tr,
            }

            done += 1
            pct = int(done / total * 100)
            sys.stdout.write(f"\r   [{pct:3d}%] {done}/{total}")
            sys.stdout.flush()
            time.sleep(0.15)  # Gentle rate limit

        print(f"  ✓ {our_locale}")

    # Save
    out_file = BASE_DIR / "agent_translations.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    size_kb = out_file.stat().st_size / 1024
    print(f"\n✅ Saved {len(translations)} agents × {len(TARGET_LOCALES)} languages")
    print(f"   File: agent_translations.json ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
