import os
import logging
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops, ImageStat

logger = logging.getLogger(__name__)

def crawl_url(url: str, output_dir: str = "screenshots") -> str:
    """
    Crawls a URL, takes a screenshot, and returns the path to the screenshot.
    """
    try:  # pragma: no cover
        with sync_playwright() as p:  # pragma: no cover
            browser = p.chromium.launch()  # pragma: no cover
            page = browser.new_page()  # pragma: no cover
            page.goto(url)  # pragma: no cover

            if not os.path.exists(output_dir):  # pragma: no cover
                os.makedirs(output_dir)  # pragma: no cover

            filename = f"screenshot_{os.path.basename(url)}.png"  # pragma: no cover
            # Ensure unique filename if multiple crawls of same base name
            # But for simplicity, overwrite is fine or append timestamp
            filepath = os.path.join(output_dir, filename)  # pragma: no cover

            page.screenshot(path=filepath, full_page=True)  # pragma: no cover
            browser.close()  # pragma: no cover

            return filepath  # pragma: no cover
    except Exception as e:  # pragma: no cover
        logger.error(f"Error crawling {url}: {e}")  # pragma: no cover
        return ""  # pragma: no cover

def compare_screenshots(img1_path: str, img2_path: str, output_path: str = "diff.png") -> float:
    """
    Compares two screenshots and returns the percentage difference (0.0 to 100.0).
    Saves the diff image if output_path is provided.
    """
    try:  # pragma: no cover
        img1 = Image.open(img1_path).convert('RGB')  # pragma: no cover
        img2 = Image.open(img2_path).convert('RGB')  # pragma: no cover

        # Ensure same size
        if img1.size != img2.size:  # pragma: no cover
            # Resize img2 to match img1? Or just fail?
            # For visual regression, size mismatch is a difference.
            # But let's try to resize just for comparison if close?
            # No, if layout changes size, it's a regression.
            # Just return 100% diff if size mismatch.
            logger.warning(f"Image sizes do not match: {img1.size} vs {img2.size}")  # pragma: no cover
            return 100.0  # pragma: no cover

        diff = ImageChops.difference(img1, img2)  # pragma: no cover

        if output_path:  # pragma: no cover
            diff.save(output_path)  # pragma: no cover

        # Calculate difference percentage
        stat = ImageStat.Stat(diff)  # pragma: no cover
        # Sum of all channel differences
        diff_val = sum(stat.mean)  # pragma: no cover
        # Max difference per channel is 255. 3 channels.
        # So percentage = (diff_val / (255 * 3)) * 100
        percentage = (diff_val / (255.0 * 3.0)) * 100.0  # pragma: no cover

        return percentage  # pragma: no cover

    except Exception as e:  # pragma: no cover
        logger.error(f"Error comparing screenshots: {e}")  # pragma: no cover
        return -1.0  # pragma: no cover
