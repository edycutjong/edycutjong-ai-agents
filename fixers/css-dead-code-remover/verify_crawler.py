import os
import sys
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set logging
logging.basicConfig(level=logging.INFO)

from tools.crawler import crawl_url

def run_verification():
    # Use the existing fixture
    fixture_path = os.path.abspath('apps/agents/fixers/css-dead-code-remover/tests/fixtures/sample.html')
    url = f"file://{fixture_path}"

    print(f"Crawling {url}...")
    screenshot_path = crawl_url(url, output_dir='screenshots')

    if screenshot_path and os.path.exists(screenshot_path):
        print(f"Screenshot saved to {screenshot_path}")
        print("Crawler verification passed.")
        # Clean up
        os.remove(screenshot_path)
        os.rmdir('screenshots')
    else:
        print("Crawler verification failed: Screenshot not created.")

if __name__ == "__main__":
    run_verification()
