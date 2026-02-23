import os
import sys
import re
import logging
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

# Add parent directory to path to import config
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

try:
    from config import Config
    from agent.tools import (
        fetch_html, clean_html, convert_to_markdown,
        extract_images, save_markdown, download_image
    )
except ImportError:
    # Fallback
    try:
        from apps.agents.file_conversion.html_to_markdown_converter.config import Config
        from apps.agents.file_conversion.html_to_markdown_converter.agent.tools import (
            fetch_html, clean_html, convert_to_markdown,
            extract_images, save_markdown, download_image
        )
    except ImportError:
        # Last resort relative import if running from agent/
        sys.path.append(os.path.join(parent_dir, '..', '..', '..', '..'))
        from apps.agents.file_conversion.html_to_markdown_converter.config import Config
        from apps.agents.file_conversion.html_to_markdown_converter.agent.tools import (
            fetch_html, clean_html, convert_to_markdown,
            extract_images, save_markdown, download_image
        )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
config = Config()

class MarkdownConverterAgent:
    def __init__(self, output_dir: str = "output", download_images: bool = False):
        self.output_dir = output_dir
        self.download_images = download_images
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def process_url(self, url: str) -> str:
        """Processes a single URL and returns the path to the saved Markdown file."""
        logger.info(f"Processing URL: {url}")

        # 1. Fetch HTML
        html_content = fetch_html(url)
        if html_content.startswith("Error"):
            logger.error(html_content)
            return html_content

        # 2. Clean HTML
        cleaned_html = clean_html(html_content)

        # 3. Convert to Markdown
        markdown_content = convert_to_markdown(cleaned_html)

        # 4. Extract and Download Images (Optional)
        if self.download_images:
            img_dir = os.path.join(self.output_dir, "images")
            if not os.path.exists(img_dir):
                os.makedirs(img_dir)

            # Find images in Markdown
            # Regex for ![alt](url)
            img_pattern = re.compile(r'!\[.*?\]\((.*?)\)')
            matches = list(set(img_pattern.findall(markdown_content))) # Unique matches

            for img_url in matches:
                # Handle relative URLs
                full_img_url = img_url
                if not img_url.startswith(('http://', 'https://')):
                    full_img_url = urljoin(url, img_url)

                try:
                    local_path = download_image(full_img_url, img_dir)
                    if not local_path.startswith("Error"):
                        filename = os.path.basename(local_path)
                        # Replace in markdown
                        markdown_content = markdown_content.replace(img_url, f"images/{filename}")
                except Exception as e:
                    logger.warning(f"Failed to download image {full_img_url}: {e}")

        # 5. Save Markdown
        parsed = urlparse(url)
        filename = f"{parsed.netloc}{parsed.path}".replace('/', '_').replace(':', '')
        if not filename:
            filename = "index"
        if not filename.endswith('.md'):
            filename += ".md"

        # Truncate filename if too long
        if len(filename) > 200:
            filename = filename[:200] + ".md"

        saved_path = save_markdown(markdown_content, filename, self.output_dir)
        logger.info(f"Saved Markdown to: {saved_path}")
        return saved_path

    def process_batch(self, urls: List[str]) -> List[str]:
        """Processes a batch of URLs concurrently."""
        results = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(self.process_url, urls))
        return results
