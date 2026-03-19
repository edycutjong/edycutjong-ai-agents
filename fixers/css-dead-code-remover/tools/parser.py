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

def parse_css_file(filepath: str) -> List[CSSRule]:
    """
    Parses a CSS file and returns a list of CSSRule objects.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            css_content = f.read()
    except Exception as e:  # pragma: no cover
        logging.error(f"Error reading file {filepath}: {e}")  # pragma: no cover
        return []  # pragma: no cover

    parser = cssutils.CSSParser()
    try:
        stylesheet = parser.parseString(css_content)
    except Exception as e:  # pragma: no cover
        logging.error(f"Error parsing CSS content in {filepath}: {e}")  # pragma: no cover
        return []  # pragma: no cover

    rules = []

    for rule in stylesheet:
        try:
            if rule.type == rule.STYLE_RULE:
                _process_style_rule(rule, rules)
            elif rule.type == rule.MEDIA_RULE:
                _process_media_rule(rule, rules)
            # Add handling for other rule types if needed (e.g., @supports)
        except Exception as e:  # pragma: no cover
            logging.warning(f"Error processing rule: {e}")  # pragma: no cover
            continue  # pragma: no cover

    return rules

def _process_style_rule(rule, rules_list: List[CSSRule], media: Optional[List[str]] = None):
    try:
        selectors = [s.selectorText for s in rule.selectorList]
        properties = {p.name: p.value for p in rule.style}

        rules_list.append(CSSRule(
            selectors=selectors,
            properties=properties,
            media=media,
            original_text=rule.cssText
        ))
    except Exception as e:  # pragma: no cover
        logging.warning(f"Skipping style rule due to error: {e}")  # pragma: no cover

def _process_media_rule(media_rule, rules_list: List[CSSRule]):
    try:
        media_query = media_rule.media.mediaText
        for rule in media_rule:
            if rule.type == rule.STYLE_RULE:
                _process_style_rule(rule, rules_list, media=[media_query])
    except Exception as e:  # pragma: no cover
        logging.warning(f"Skipping media rule due to error: {e}")  # pragma: no cover

if __name__ == "__main__":
    import sys  # pragma: no cover
    if len(sys.argv) > 1:  # pragma: no cover
        parsed_rules = parse_css_file(sys.argv[1])  # pragma: no cover
        for r in parsed_rules:  # pragma: no cover
            print(f"Selectors: {r.selectors}")  # pragma: no cover
            print(f"Media: {r.media}")  # pragma: no cover
            print("-" * 20)  # pragma: no cover
