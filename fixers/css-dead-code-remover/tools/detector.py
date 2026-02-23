import re
import logging
from typing import Set, List, Pattern, Dict
from .parser import CSSRule

logger = logging.getLogger(__name__)

def find_unused_rules(
    rules: List[CSSRule],
    used_selectors: Set[str],
    safelist: List[str] = None
) -> List[CSSRule]:
    """
    Identifies CSS rules whose selectors are not used in the codebase.
    Returns a list of unused CSSRule objects.
    """
    if safelist is None:
        safelist = []

    unused_rules = []

    # Compile safelist regexes
    safelist_patterns = [re.compile(p) for p in safelist]

    for rule in rules:
        is_used = False

        for selector in rule.selectors:
            # Check if selector is used or safelisted
            if _is_safelisted(selector, safelist_patterns):
                is_used = True
                break

            if _is_selector_used(selector, used_selectors):
                is_used = True
                break

        if not is_used:
            unused_rules.append(rule)

    return unused_rules

def audit_media_queries(rules: List[CSSRule]) -> Dict[str, int]:
    """
    Analyzes media query usage.
    Returns a dictionary mapping media query strings to the count of rules using them.
    'None' key represents rules without media queries.
    """
    stats = {}

    for rule in rules:
        if rule.media:
            # Media is a list, usually one query string per rule if parsed correctly
            # But could be multiple? cssutils usually returns the media list for the block
            # For simplicity, join them or take the first
            media_key = ", ".join(rule.media)
            stats[media_key] = stats.get(media_key, 0) + 1
        else:
            stats['No Media Query'] = stats.get('No Media Query', 0) + 1

    return stats

def _is_selector_used(selector: str, used_selectors: Set[str]) -> bool:
    """
    Checks if a CSS selector matches any used selector.
    """
    # Normalize selector
    clean_selector = selector.strip()

    # Handle pseudo-classes/elements (e.g., .btn:hover -> .btn)
    base_selector = re.split(r'[:]{1,2}', clean_selector)[0]

    # Extract all classes, IDs, and tags
    class_id_tokens = re.findall(r'([.#][a-zA-Z0-9_-]+)', base_selector)

    if class_id_tokens:
        # Check if ALL classes/IDs are used
        for token in class_id_tokens:
            if token not in used_selectors:
                return False
        return True

    # If no classes/IDs, check tags
    if '*' in base_selector or 'body' in base_selector or 'html' in base_selector:
        return True

    return True

def _is_safelisted(selector: str, safelist_patterns: List[Pattern]) -> bool:
    """
    Checks if a selector matches any safelist pattern.
    """
    for pattern in safelist_patterns:
        if pattern.search(selector):
            return True
    return False
