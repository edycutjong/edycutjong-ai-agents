import os
import cssutils
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Suppress cssutils warnings
cssutils.log.setLevel(logging.CRITICAL)

@dataclass
class CSSRule:
    selectors: List[str]
    properties: Dict[str, str]
    media: Optional[List[str]] = None
    original_text: str = ""
    source_file: str = ""

def parse_css_file(filepath: str) -> List[CSSRule]:
    """
    Parses a CSS file and returns a list of CSSRule objects.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:
        logging.error(f"Error reading file {filepath}: {e}")
        return []

    parser = cssutils.CSSParser()
    try:
        stylesheet = parser.parseString(css_content)
    except Exception as e:
        logging.error(f"Error parsing CSS content in {filepath}: {e}")
        return []

    rules = []
    source_filename = os.path.basename(filepath)

    for rule in stylesheet:
        try:
            if rule.type == rule.STYLE_RULE:
                _process_style_rule(rule, rules, source_file=source_filename)
            elif rule.type == rule.MEDIA_RULE:
                _process_media_rule(rule, rules, source_file=source_filename)
            # Add handling for other rule types if needed (e.g., @supports)
        except Exception as e:
            logging.warning(f"Error processing rule: {e}")
            continue

    return rules

def _process_style_rule(rule, rules_list: List[CSSRule], media: Optional[List[str]] = None, source_file: str = ""):
    try:
        selectors = [s.selectorText for s in rule.selectorList]
        properties = {p.name: p.value for p in rule.style}

        rules_list.append(CSSRule(
            selectors=selectors,
            properties=properties,
            media=media,
            original_text=rule.cssText,
            source_file=source_file
        ))
    except Exception as e:
        logging.warning(f"Skipping style rule due to error: {e}")

def _process_media_rule(media_rule, rules_list: List[CSSRule], source_file: str = ""):
    try:
        media_query = media_rule.media.mediaText
        for rule in media_rule:
            if rule.type == rule.STYLE_RULE:
                _process_style_rule(rule, rules_list, media=[media_query], source_file=source_file)
    except Exception as e:
        logging.warning(f"Skipping media rule due to error: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        parsed_rules = parse_css_file(sys.argv[1])
        for r in parsed_rules:
            print(f"Selectors: {r.selectors}")
            print(f"Media: {r.media}")
            print("-" * 20)
