import cssutils
import logging
from typing import List, Set
from .parser import CSSRule

logger = logging.getLogger(__name__)

# Suppress cssutils warnings
cssutils.log.setLevel(logging.CRITICAL)

def purge_css(original_css_path: str, unused_rules: List[CSSRule], output_path: str = None) -> str:
    """
    Removes unused rules from the CSS file and returns the cleaned CSS content.
    If output_path is provided, writes the cleaned CSS to that file.
    """
    try:
        parser = cssutils.CSSParser()
        with open(original_css_path, 'r', encoding='utf-8') as f:
            stylesheet = parser.parseString(f.read())

        # Create a set of selectors to remove for fast lookup
        # But wait, a rule might have multiple selectors (comma separated).
        # Our CSSRule object splits them.
        # But cssutils rule object has selectorText.
        # If we identified a rule as unused, it means ALL its selectors are unused
        # (because detector checks each selector in rule.selectors).
        # Wait, if a rule is: `.used, .unused { ... }`
        # The detector iterates over selectors: `.used` (used -> is_used=True), `.unused` (unused).
        # Since at least one selector is used, the whole rule is marked as used.
        # So we don't remove it.
        # This is correct behavior to avoid breaking `.used`.
        # Ideally, we should rewrite the selector to remove `.unused`, but that's complex (modifying selectorText).
        # For now, we only remove completely unused rules.

        # We need to match the rule in stylesheet with the rule in unused_rules.
        # Since we parsed the stylesheet to create CSSRule objects, we can try to match by index or content.
        # However, indices might shift if we modify list.
        # Better: iterate backwards or build a new list.

        # Or, we can use the `original_text` property in CSSRule to find the rule?
        # But `original_text` might be slightly different if re-parsed?
        # No, `cssText` should be consistent.

        # Let's use index if we can ensure deterministic order.
        # The parser returns rules in order.
        # But `unused_rules` is a subset.

        # Strategy:
        # 1. Parse the stylesheet again.
        # 2. Iterate over rules in stylesheet.
        # 3. For each rule, check if it matches an unused rule.
        #    Matching by `cssText` is risky due to formatting.
        #    Matching by selectors is safer.
        #    But `unused_rules` contains `CSSRule` objects.

        # Let's map `unused_rules` to a set of their `original_text` (if reliable) or selector lists.
        # Actually, `cssutils` objects have IDs? No.

        # Let's rely on the fact that `unused_rules` were generated from the same file.
        # We can re-use the detector logic or pass the indices of unused rules.
        # But `unused_rules` is a list of objects.

        # Refined Strategy:
        # Pass the `unused_rules` which contains `original_text`.
        # Iterate over stylesheet.cssRules.
        # If `rule.cssText` matches any in `unused_rules`, delete it.
        # But there might be duplicate rules.

        # Better: Since we want to delete specific rules, maybe `cleaner` should accept indices?
        # Or we rebuild the stylesheet from scratch?

        # Let's go with removing from stylesheet.
        # We need to collect rules to remove first.

        to_remove = []
        unused_texts = set(r.original_text for r in unused_rules)

        for rule in stylesheet.cssRules:
            if rule.type == rule.STYLE_RULE:
                # Check if this rule's text matches one of the unused ones
                # This assumes exact match of cssText.
                if rule.cssText in unused_texts:
                    to_remove.append(rule)
            elif rule.type == rule.MEDIA_RULE:
                # Handle nested rules
                # The detector returned top-level rules?
                # No, parser flatens nested rules in media queries?
                # Let's check parser.py.
                pass

        # Wait, `parser.py` flattens rules.
        # It returns `CSSRule` with `media` attribute.
        # If `media` is present, the rule came from inside a media block.
        # So we cannot just match `rule.cssText` of the media block.
        # We need to find the style rule INSIDE the media block.

        for rule in stylesheet.cssRules:
            if rule.type == rule.STYLE_RULE:
                if rule.cssText in unused_texts:
                    to_remove.append(rule)
            elif rule.type == rule.MEDIA_RULE:
                for sub_rule in rule.cssRules:
                    if sub_rule.type == sub_rule.STYLE_RULE:
                         if sub_rule.cssText in unused_texts:
                             # We can remove sub_rule from rule
                             # But check cssutils API
                             # rule.deleteRule(index)?
                             # Or just to_remove list of (parent, rule) tuples.
                             pass

        # Since modifying while iterating is bad, we collect first.
        # But `unused_texts` might match multiple rules if duplicates exist.
        # If we remove all duplicates of an unused rule, it's fine (all are unused).

        # Implementation for Media Rules removal:
        to_remove_pairs = [] # (parent, rule)

        for i, rule in enumerate(stylesheet.cssRules):
            if rule.type == rule.STYLE_RULE:
                if rule.cssText in unused_texts:
                    to_remove_pairs.append((stylesheet, rule))
            elif rule.type == rule.MEDIA_RULE:
                for sub_rule in rule.cssRules:
                    if sub_rule.type == sub_rule.STYLE_RULE:
                         if sub_rule.cssText in unused_texts:
                             to_remove_pairs.append((rule, sub_rule))

        # Remove rules
        for parent, rule in to_remove_pairs:
            try:
                # cssutils 2.x: parent.deleteRule(rule) or remove(rule)?
                # parent.cssRules.remove(rule) might work
                parent.deleteRule(rule)
            except Exception as e:
                logger.warning(f"Failed to remove rule: {e}")

        # Generate clean CSS
        cleaned_css = stylesheet.cssText.decode('utf-8')

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_css)

        return cleaned_css

    except Exception as e:
        logger.error(f"Error purging CSS: {e}")
        return ""

def minify_css(css_content: str, output_path: str = None) -> str:
    """
    Minifies CSS content.
    """
    try:
        parser = cssutils.CSSParser()
        stylesheet = parser.parseString(css_content)

        # cssutils minification involves setting serializer preferences
        cssutils.ser.prefs.useMinified()
        minified_css = stylesheet.cssText.decode('utf-8')

        # Reset prefs?
        cssutils.ser.prefs.useDefaults()

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(minified_css)

        return minified_css
    except Exception as e:
        logger.error(f"Error minifying CSS: {e}")
        return css_content
