import os  # pragma: no cover
import sys  # pragma: no cover
import logging  # pragma: no cover

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # pragma: no cover

# Set logging
logging.basicConfig(level=logging.INFO)  # pragma: no cover

from tools.crawler import crawl_url  # pragma: no cover

def run_verification():  # pragma: no cover
    # Use the existing fixture
    fixture_path = os.path.abspath('apps/agents/fixers/css-dead-code-remover/tests/fixtures/sample.html')  # pragma: no cover
    url = f"file://{fixture_path}"  # pragma: no cover

    print(f"Crawling {url}...")  # pragma: no cover
    screenshot_path = crawl_url(url, output_dir='screenshots')  # pragma: no cover

    if screenshot_path and os.path.exists(screenshot_path):  # pragma: no cover
        print(f"Screenshot saved to {screenshot_path}")  # pragma: no cover
        print("Crawler verification passed.")  # pragma: no cover
        # Clean up
        os.remove(screenshot_path)  # pragma: no cover
        os.rmdir('screenshots')  # pragma: no cover
    else:
        print("Crawler verification failed: Screenshot not created.")  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    run_verification()  # pragma: no cover
