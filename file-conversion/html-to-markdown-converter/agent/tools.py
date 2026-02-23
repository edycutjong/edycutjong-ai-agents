import os
import sys
import re
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urljoin, urlparse
from langchain_core.tools import tool
from typing import List, Optional

# Add parent directory to path to import config
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

try:
    from config import Config
except ImportError:
    # Fallback for when running from root
    from apps.agents.file_conversion.html_to_markdown_converter.config import Config

config = Config()

def fetch_html(url: str) -> str:
    """Fetches HTML content from a URL."""
    try:
        response = requests.get(url, headers={'User-Agent': config.USER_AGENT}, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {e}"

def clean_html(html_content: str, remove_tags: Optional[List[str]] = None) -> str:
    """Removes boilerplate (nav, footer, ads) from HTML content."""
    if not html_content:
        return ""

    soup = BeautifulSoup(html_content, 'lxml')

    tags_to_remove = remove_tags if remove_tags else config.REMOVE_TAGS

    for tag in tags_to_remove:
        for element in soup.find_all(tag):
            element.decompose()

    # Remove hidden elements
    for element in soup.find_all(style=re.compile(r'display:\s*none')):
        element.decompose()

    # Try to find the main content if possible
    # Heuristics: <main>, <article>, <div class="content">, etc.
    main_content = soup.find('main') or soup.find('article')

    if not main_content:
        # Fallback to body or keep everything if no main container found
        main_content = soup.body or soup

    return str(main_content)

def convert_to_markdown(html_content: str) -> str:
    """Converts HTML content to Markdown."""
    if not html_content:
        return ""

    # markdownify options can be tweaked
    return md(html_content, heading_style="ATX", strip=['script', 'style'])

def extract_images(html_content: str, base_url: str) -> List[str]:
    """Extracts image URLs from HTML content."""
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'lxml')
    images = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            full_url = urljoin(base_url, src)
            images.append(full_url)
    return images

def download_image(url: str, save_dir: str) -> str:
    """Downloads an image and returns the local path."""
    try:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        parsed_url = urlparse(url)
        path = parsed_url.path
        filename = os.path.basename(path)
        if not filename:
            filename = "image_" + str(hash(url)) + ".png" # Fallback

        filepath = os.path.join(save_dir, filename)

        response = requests.get(url, headers={'User-Agent': config.USER_AGENT}, stream=True, timeout=10)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return filepath
    except Exception as e:
        return f"Error downloading {url}: {e}"

def save_markdown(content: str, filename: str, output_dir: str = "output") -> str:
    """Saves Markdown content to a file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath

# LangChain Tools
@tool
def fetch_html_tool(url: str) -> str:
    """Fetches HTML from a URL."""
    return fetch_html(url)

@tool
def clean_html_tool(html_content: str) -> str:
    """Cleans HTML content by removing boilerplate."""
    return clean_html(html_content)

@tool
def convert_to_markdown_tool(html_content: str) -> str:
    """Converts HTML string to Markdown."""
    return convert_to_markdown(html_content)

@tool
def extract_images_tool(html_content: str, base_url: str) -> List[str]:
    """Extracts all image URLs from the HTML content."""
    return extract_images(html_content, base_url)

@tool
def save_markdown_tool(content: str, filename: str) -> str:
    """Saves markdown content to a file."""
    return save_markdown(content, filename)
