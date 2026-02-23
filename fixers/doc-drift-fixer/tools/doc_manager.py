import os
import re
import ast
from typing import List, Dict
import requests

class DocManager:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path

    def scan_docs(self) -> List[str]:
        """Scan the repository for markdown files."""
        docs = []
        for root, _, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(".md"):
                    docs.append(os.path.join(root, file))
        return docs

    def find_related_docs(self, source_file: str) -> List[str]:
        """Heuristic to find related documentation for a source file."""
        # This is a simple heuristic.
        # Ideally, we look for file name matches or cross-references.

        base_name = os.path.basename(source_file).split('.')[0]
        docs = self.scan_docs()
        related = []

        for doc in docs:
            doc_name = os.path.basename(doc).lower()
            if base_name.lower() in doc_name:
                related.append(doc)
            else:
                # Search content for mentions of the file name or classes?
                # That might be too slow for now.
                pass

        return related

    def check_links(self, doc_path: str) -> List[str]:
        """Check for broken links in a markdown file."""
        broken_links = []
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract links [text](url)
            links = re.findall(r'\[.*?\]\((.*?)\)', content)

            for link in links:
                if link.startswith('http'):
                    try:
                        response = requests.head(link, timeout=5)
                        if response.status_code >= 400:
                            broken_links.append(f"{link} (Status: {response.status_code})")
                    except requests.RequestException:
                         broken_links.append(f"{link} (Connection Error)")
                elif not link.startswith('#'):
                    # Local file link
                    # resolving relative paths
                    doc_dir = os.path.dirname(doc_path)
                    target = os.path.join(doc_dir, link)

                    # Handle anchors
                    if '#' in target:
                        target = target.split('#')[0]

                    if not os.path.exists(target):
                         broken_links.append(f"{link} (File not found)")

        except Exception as e:
            return [f"Error checking links in {doc_path}: {str(e)}"]

        return broken_links

    def verify_code_examples(self, doc_path: str) -> List[str]:
        """Verify syntax of code examples in markdown."""
        errors = []
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Regex to find python code blocks
            # Matches ```python\n ... \n```
            code_blocks = re.findall(r'```python\n(.*?)\n```', content, re.DOTALL)

            for i, code in enumerate(code_blocks):
                try:
                    ast.parse(code)
                except SyntaxError as e:
                    errors.append(f"Block {i+1}: SyntaxError: {e}")
        except Exception as e:
            return [f"Error verifying examples in {doc_path}: {str(e)}"]

        return errors
