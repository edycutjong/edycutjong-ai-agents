import os
import re
from bs4 import BeautifulSoup
from typing import Set, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import smart scanner
try:
    from .smart_scanner import analyze_component_with_llm
except ImportError:
    try:
        from smart_scanner import analyze_component_with_llm
    except ImportError:
        logger.warning("Smart scanner module not found. Smart scan will be disabled.")
        analyze_component_with_llm = None

# Extensions to scan
SCAN_EXTENSIONS = {'.html', '.htm', '.js', '.jsx', '.ts', '.tsx', '.vue', '.php'}

# Compiled regexes for scanning
CLASS_PATTERN = re.compile(r'["\']([a-zA-Z0-9_-]+(?:\s+[a-zA-Z0-9_-]+)*)["\']')
ATTR_PATTERN = re.compile(r'\b(class|className)\s*=\s*(?:\{`([^`]+)`\}|["\']([^"\']+)["\'])')
TEMPLATE_LITERAL_PATTERN = re.compile(r'\$\{[^}]+\}')

def scan_directory(directory: str, smart_scan: bool = False) -> Set[str]:
    """
    Recursively scans a directory for files and extracts used CSS classes and IDs.
    Returns a set of selectors (e.g., '.class-name', '#id-name', 'tagname').
    """
    used_selectors = set()

    for root, _, files in os.walk(directory):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in SCAN_EXTENSIONS:
                filepath = os.path.join(root, file)
                try:
                    selectors = scan_file(filepath, smart_scan)
                    used_selectors.update(selectors)
                except Exception as e:
                    logger.error(f"Error scanning file {filepath}: {e}")

    return used_selectors

def scan_file(filepath: str, smart_scan: bool = False) -> Set[str]:
    """
    Scans a single file for CSS usage.
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    ext = os.path.splitext(filepath)[1].lower()
    selectors = set()

    if ext in {'.html', '.htm', '.php'}:  # PHP often contains HTML
        selectors.update(_scan_html(content))

    # Also scan all files with regex for dynamic usage or JS/JSX/TSX
    selectors.update(_scan_regex(content))

    # Smart scan for JS-like files
    if smart_scan and analyze_component_with_llm and ext in {'.js', '.jsx', '.ts', '.tsx', '.vue'}:
        try:
            smart_selectors = analyze_component_with_llm(content, filepath)
            selectors.update(smart_selectors)
        except Exception as e:
            logger.error(f"Smart scan failed for {filepath}: {e}")

    return selectors

def _scan_html(content: str) -> Set[str]:
    selectors = set()
    soup = BeautifulSoup(content, 'html.parser')

    for tag in soup.find_all(True):
        selectors.add(tag.name)  # Add tag name

        # Add classes
        if tag.get('class'):
            classes = tag.get('class')
            if isinstance(classes, list):
                for cls in classes:
                    selectors.add(f".{cls}")
            else:
                 # In case it's a string (though soup usually splits it)
                for cls in classes.split():
                    selectors.add(f".{cls}")

        # Add IDs
        if tag.get('id'):
            id_val = tag.get('id')
            selectors.add(f"#{id_val}")

    return selectors

def _scan_regex(content: str) -> Set[str]:
    selectors = set()

    matches = CLASS_PATTERN.findall(content)
    for match in matches:
        # Split by space in case of "class1 class2"
        for part in match.split():
             # Basic heuristic: if it looks like a class name, assume it is used
             # This might produce false positives but safer than false negatives
             selectors.add(f".{part}")
             # Also add as ID if it could be an ID (hard to distinguish without context)
             selectors.add(f"#{part}")

    # Specifically for JS/React className
    attr_matches = ATTR_PATTERN.findall(content)
    for match in attr_matches:
        # match is tuple: (attr_name, template_literal_content, string_content)
        val = match[1] if match[1] else match[2]
        if val:
            # Clean up template literals a bit (remove ${...})
            val = TEMPLATE_LITERAL_PATTERN.sub('', val)
            for part in val.split():
                if part.strip():
                    selectors.add(f".{part.strip()}")

    return selectors

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        found = scan_file(sys.argv[1])
        print(f"Found {len(found)} selectors: {sorted(list(found))}")
