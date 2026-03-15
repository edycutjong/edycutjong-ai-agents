"""
fix_translations.py — One-time cleanup for agent_translations.json
Fixes:
  1. Add en.name to every agent (from slug)
  2. Strip Arabic boilerplate suffix from ar.description
  3. Fix double periods (..) in ru/hi descriptions
  4. Re-translate untranslated English descriptions (regex-tester etc.)
  5. Fix es "Optimizador rápido" → "Optimizador de Prompts"
  6. Fix pt "Gerador de Lesmas" → "Gerador de Slugs de URL"

Run: python fix_translations.py
"""

import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

BASE_DIR = Path(__file__).parent
TRANSLATIONS_FILE = BASE_DIR / "agent_translations.json"

ALL_LANGS = ["en", "id", "zh", "es", "pt", "ja", "ko", "de", "fr", "ru", "ar", "hi"]

ACRONYMS = {"ai", "api", "css", "csv", "dns", "html", "http", "ip", "json",
            "jwt", "llm", "ml", "npm", "pdf", "qa", "rag", "rss", "seo",
            "sql", "ssh", "ssl", "svg", "ui", "url", "ux", "xml", "yaml",
            "sop", "cors", "cli", "crm", "readme", "ci", "cd"}

ARABIC_BOILERPLATE = " تم تصميمه كمشروع وكلاء الذكاء الاصطناعي."
ARABIC_BOILERPLATE_ALT = "تم تصميمه كمشروع وكلاء الذكاء الاصطناعي"

# Google Translate locale codes
LOCALE_TO_GTRANSLATE = {"zh": "zh-CN"}


def slug_to_name(agent_key: str) -> str:
    """Convert agent key like 'ai-ml-ops/prompt-optimizer' to 'Prompt Optimizer'."""
    slug = agent_key.rsplit("/", 1)[-1]  # Take the last part
    words = slug.replace("-", " ").replace("_", " ").split()
    return " ".join(w.upper() if w.lower() in ACRONYMS else w.capitalize() for w in words)


def google_translate(text: str, target_lang: str) -> str:
    """Translate using Google's free translate API."""
    if not text or not text.strip():
        return ""
    gt_lang = LOCALE_TO_GTRANSLATE.get(target_lang, target_lang)
    url = "https://translate.googleapis.com/translate_a/single"
    params = urllib.parse.urlencode({
        "client": "gtx",
        "sl": "en",
        "tl": gt_lang,
        "dt": "t",
        "q": text,
    })
    full_url = f"{url}?{params}"
    req = urllib.request.Request(full_url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            translated = "".join(part[0] for part in data[0] if part[0])
            return translated
        except Exception:
            if attempt == 2:
                return text
            time.sleep(0.5 * (attempt + 1))
    return text


def fix_double_period(text: str) -> str:
    """Fix '..' at end of text → '.'"""
    if text.endswith(".."):
        return text[:-1]
    return text


def strip_arabic_boilerplate(text: str) -> str:
    """Remove the boilerplate phrase from Arabic descriptions."""
    if ARABIC_BOILERPLATE in text:
        text = text.replace(ARABIC_BOILERPLATE, "")
    if text.endswith(ARABIC_BOILERPLATE_ALT):
        text = text[: -len(ARABIC_BOILERPLATE_ALT)].rstrip()
    # Clean trailing period if now doubled
    text = text.rstrip()
    if text.endswith(".."):
        text = text[:-1]
    return text


def main():
    print("📂 Loading agent_translations.json...")
    data = json.loads(TRANSLATIONS_FILE.read_text(encoding="utf-8"))
    print(f"   Found {len(data)} agents\n")

    stats = {
        "en_name_added": 0,
        "ar_boilerplate_stripped": 0,
        "double_period_fixed": 0,
        "retranslated": 0,
        "manual_fixes": 0,
    }

    # ────────────────────────────────────────────────────────
    # Fix 1: Add en.name to every agent
    # ────────────────────────────────────────────────────────
    print("🔧 Fix 1: Adding en.name to every agent...")
    for key, langs in data.items():
        en_entry = langs.get("en", {})
        if "name" not in en_entry:
            en_name = slug_to_name(key)
            if "en" not in langs:
                langs["en"] = {}
            langs["en"]["name"] = en_name
            stats["en_name_added"] += 1
    print(f"   Added en.name to {stats['en_name_added']} agents\n")

    # ────────────────────────────────────────────────────────
    # Fix 2: Strip Arabic boilerplate
    # ────────────────────────────────────────────────────────
    print("🔧 Fix 2: Stripping Arabic boilerplate...")
    for key, langs in data.items():
        ar = langs.get("ar", {})
        desc = ar.get("description", "")
        if ARABIC_BOILERPLATE_ALT in desc:
            ar["description"] = strip_arabic_boilerplate(desc)
            stats["ar_boilerplate_stripped"] += 1
    print(f"   Stripped boilerplate from {stats['ar_boilerplate_stripped']} agents\n")

    # ────────────────────────────────────────────────────────
    # Fix 3: Fix double periods in ru/hi
    # ────────────────────────────────────────────────────────
    print("🔧 Fix 3: Fixing double periods in ru/hi...")
    for key, langs in data.items():
        for lang in ["ru", "hi"]:
            entry = langs.get(lang, {})
            desc = entry.get("description", "")
            if desc.endswith(".."):
                entry["description"] = fix_double_period(desc)
                stats["double_period_fixed"] += 1
    print(f"   Fixed {stats['double_period_fixed']} double periods\n")

    # ────────────────────────────────────────────────────────
    # Fix 4: Re-translate entries that match English verbatim
    # ────────────────────────────────────────────────────────
    print("🔧 Fix 4: Finding untranslated (English-identical) descriptions...")
    retranslate_queue = []
    for key, langs in data.items():
        en_desc = langs.get("en", {}).get("description", "")
        if not en_desc:
            continue
        for lang in ["es", "pt", "de", "fr"]:
            foreign_desc = langs.get(lang, {}).get("description", "")
            if foreign_desc == en_desc:
                retranslate_queue.append((key, lang, en_desc))

    print(f"   Found {len(retranslate_queue)} untranslated descriptions to fix")
    for key, lang, en_desc in retranslate_queue:
        translated = google_translate(en_desc, lang)
        if translated and translated != en_desc:
            data[key][lang]["description"] = translated
            stats["retranslated"] += 1
            print(f"   ✓ {key}.{lang}")
        time.sleep(0.2)
    print(f"   Re-translated {stats['retranslated']} descriptions\n")

    # ────────────────────────────────────────────────────────
    # Fix 5: Manual fix — prompt-optimizer es.name
    # ────────────────────────────────────────────────────────
    print("🔧 Fix 5: Manual fix — prompt-optimizer es.name...")
    po = data.get("ai-ml-ops/prompt-optimizer", {})
    if po.get("es", {}).get("name") == "Optimizador rápido":
        po["es"]["name"] = "Optimizador de Prompts"
        stats["manual_fixes"] += 1
        print("   ✓ Fixed es.name → 'Optimizador de Prompts'")
    else:
        print("   ⏭ Already fixed or not found")

    # ────────────────────────────────────────────────────────
    # Fix 6: Manual fix — slug-generator pt.name
    # ────────────────────────────────────────────────────────
    print("🔧 Fix 6: Manual fix — slug-generator pt.name...")
    sg = data.get("content-writing/slug-generator", {})
    if sg.get("pt", {}).get("name") == "Gerador de Lesmas":
        sg["pt"]["name"] = "Gerador de Slugs de URL"
        stats["manual_fixes"] += 1
        print("   ✓ Fixed pt.name → 'Gerador de Slugs de URL'")
    else:
        print("   ⏭ Already fixed or not found")

    # ────────────────────────────────────────────────────────
    # Ensure every agent has all 12 language keys
    # ────────────────────────────────────────────────────────
    print("\n🔧 Ensuring every agent has all 12 language keys...")
    missing_langs = 0
    for key, langs in data.items():
        for lang in ALL_LANGS:
            if lang not in langs:
                langs[lang] = {"name": "", "description": ""}
                missing_langs += 1
            else:
                if "name" not in langs[lang]:
                    langs[lang]["name"] = ""
                if "description" not in langs[lang]:
                    langs[lang]["description"] = ""
    print(f"   Added {missing_langs} missing language entries\n")

    # ────────────────────────────────────────────────────────
    # Save
    # ────────────────────────────────────────────────────────
    print("💾 Saving...")
    with open(TRANSLATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    size_kb = TRANSLATIONS_FILE.stat().st_size / 1024
    print(f"\n✅ Done! ({size_kb:.1f} KB)")
    print(f"   Summary:")
    for k, v in stats.items():
        print(f"     {k}: {v}")


if __name__ == "__main__":
    main()
