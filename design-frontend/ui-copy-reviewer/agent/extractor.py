import os
import re
from bs4 import BeautifulSoup

class TextExtractor:
    def __init__(self):
        self.supported_extensions = {'.html', '.htm', '.jsx', '.tsx', '.js', '.ts', '.py'}
        # Attributes that likely contain UI copy
        self.copy_attributes = {'title', 'alt', 'placeholder', 'aria-label', 'label'}

        # 1. Text between tags: >Some Text<
        self.text_content_pattern = re.compile(r'>([^<{]+)<')

        # 2. Text in specific attributes: title="Some Text" or title='Some Text'
        self.attr_pattern = re.compile(r'\b(' + '|'.join(self.copy_attributes) + r')=(["\'])(.*?)\2')

    def extract_text_from_file(self, filepath):
        """
        Extracts UI text strings from a file.
        Returns a list of dictionaries: [{'text': '...', 'line': 1, 'context': '...', 'type': '...'}]
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        _, ext = os.path.splitext(filepath)
        if ext not in self.supported_extensions:
            return []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {filepath}: {e}")
            return []

        if ext in {'.html', '.htm'}:
            return self._extract_html(content)
        else:
            return self._extract_code(content) # Rename from _extract_jsx to cover JS/TS/Py too

    def _extract_html(self, content):
        results = []
        soup = BeautifulSoup(content, 'html.parser')

        # Extract text nodes
        for element in soup.find_all(string=True):
            text = element.strip()
            if text and element.parent.name not in ['script', 'style', 'head', 'meta', 'title']:
                results.append({
                    'text': text,
                    'line': None, # BS4 doesn't easily give line numbers
                    'type': 'content',
                    'tag': element.parent.name,
                    'context': str(element.parent)[:50] # Snippet
                })

        # Extract attributes
        for tag in soup.find_all(True):
            for attr in self.copy_attributes:
                if tag.has_attr(attr):
                    val = tag[attr]
                    if isinstance(val, list):
                        val = " ".join(val)
                    if val and val.strip():
                        results.append({
                            'text': val.strip(),
                            'line': None,
                            'type': 'attribute',
                            'tag': tag.name,
                            'attribute': attr,
                            'context': str(tag)[:50]
                        })
        return results

    def _extract_code(self, content):
        results = []
        lines = content.split('\n')

        # 3. Python f-strings or strings might be UI copy? Hard to tell.
        # For now, assume mainly JSX-like structures or attributes.

        for i, line in enumerate(lines):
            # Check for text content
            for match in self.text_content_pattern.finditer(line):
                text = match.group(1).strip()
                if text:
                    results.append({
                        'text': text,
                        'line': i + 1,
                        'type': 'content',
                        'context': line.strip()
                    })

            # Check for attributes
            for match in self.attr_pattern.finditer(line):
                attr_name = match.group(1)
                text = match.group(3).strip()
                if text:
                    results.append({
                        'text': text,
                        'line': i + 1,
                        'type': 'attribute',
                        'attribute': attr_name,
                        'context': line.strip()
                    })

        return results

# Wrapper function for ease of use
def extract_text_from_file(filepath):
    extractor = TextExtractor()
    return extractor.extract_text_from_file(filepath)
