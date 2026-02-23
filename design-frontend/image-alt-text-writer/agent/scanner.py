import os
from bs4 import BeautifulSoup
from typing import List, Dict, Optional

class ImageInfo:
    def __init__(self, src: str, alt: Optional[str], context: str, filepath: str, line_number: Optional[int] = None):
        self.src = src
        self.alt = alt
        self.context = context
        self.filepath = filepath
        self.line_number = line_number

    def to_dict(self):
        return {
            "src": self.src,
            "alt": self.alt,
            "context": self.context,
            "filepath": self.filepath,
            "line_number": self.line_number
        }

    def __repr__(self):
        return f"ImageInfo(src='{self.src}', alt='{self.alt}', filepath='{self.filepath}')"

class Scanner:
    def __init__(self):
        pass

    def scan_file(self, filepath: str) -> List[ImageInfo]:
        """Scans an HTML file for images missing alt text."""
        missing_alt_images = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Use lxml for speed and line numbers if available, fallback to html.parser
            try:
                soup = BeautifulSoup(content, 'lxml')
            except ImportError:
                soup = BeautifulSoup(content, 'html.parser')

            # Find all img tags
            images = soup.find_all('img')

            for img in images:
                src = img.get('src')
                if not src:
                    continue

                alt = img.get('alt')
                role = img.get('role')

                # Check if decorative (marked as presentation/none)
                if role in ['presentation', 'none']:
                    continue

                # Check if alt is missing or empty
                if alt is None or alt.strip() == "":
                    # Extract context (parent text)
                    parent = img.parent
                    context = parent.get_text(strip=True) if parent else ""
                    # Limit context length
                    context = context[:200] + "..." if len(context) > 200 else context

                    missing_alt_images.append(ImageInfo(
                        src=src,
                        alt=alt,
                        context=context,
                        filepath=filepath,
                        line_number=img.sourceline
                    ))

        except Exception as e:
            print(f"Error scanning file {filepath}: {e}")

        return missing_alt_images

    def scan_directory(self, directory: str, recursive: bool = False) -> List[ImageInfo]:
        """Scans a directory for HTML files."""
        all_missing_images = []

        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.html', '.htm', '.xhtml')):
                    filepath = os.path.join(root, file)
                    all_missing_images.extend(self.scan_file(filepath))

            if not recursive:
                break

        return all_missing_images
