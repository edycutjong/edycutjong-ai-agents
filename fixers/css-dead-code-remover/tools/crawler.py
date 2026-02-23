import os
import logging
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageStat

logger = logging.getLogger(__name__)

def crawl_url(url: str, output_dir: str = "screenshots") -> str:
    """
    Crawls a URL, takes a screenshot, and returns the path to the screenshot.
    """
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            filename = f"screenshot_{os.path.basename(url)}.png"
            # Ensure unique filename if multiple crawls of same base name
            # But for simplicity, overwrite is fine or append timestamp
            filepath = os.path.join(output_dir, filename)

            page.screenshot(path=filepath, full_page=True)
            browser.close()

            return filepath
    except Exception as e:
        logger.error(f"Error crawling {url}: {e}")
        return ""

def compare_screenshots(img1_path: str, img2_path: str, output_path: str = "diff.png") -> float:
    """
    Compares two screenshots and returns the percentage difference (0.0 to 100.0).
    Saves the diff image if output_path is provided.
    """
    try:
        img1 = Image.open(img1_path).convert('RGB')
        img2 = Image.open(img2_path).convert('RGB')

        # Ensure same size
        if img1.size != img2.size:
            # Resize img2 to match img1? Or just fail?
            # For visual regression, size mismatch is a difference.
            # But let's try to resize just for comparison if close?
            # No, if layout changes size, it's a regression.
            # Just return 100% diff if size mismatch.
            logger.warning(f"Image sizes do not match: {img1.size} vs {img2.size}")
            return 100.0

        diff = ImageChops.difference(img1, img2)

        if output_path:
            diff.save(output_path)

        # Calculate difference percentage
        stat = ImageStat.Stat(diff)
        # Sum of all channel differences
        diff_val = sum(stat.mean)
        # Max difference per channel is 255. 3 channels.
        # So percentage = (diff_val / (255 * 3)) * 100
        percentage = (diff_val / (255.0 * 3.0)) * 100.0

        return percentage

    except Exception as e:
        logger.error(f"Error comparing screenshots: {e}")
        return -1.0
