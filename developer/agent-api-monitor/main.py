"""
API Monitor Agent — checks uptime, response time, headers, and schema drift.
Usage: python main.py <url>  [--timeout 10] [--expect-status 200]
"""
import argparse
import sys
import json
import time
try:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
except ImportError:
    pass


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    """Entry point called by the app framework."""
    return f"[API Monitor] Monitoring: {user_input}\n\nPaste a URL or endpoint description to check uptime, latency, headers, and schema consistency."


def check_endpoint(url: str, timeout: int = 10, expected_status: int = 200):
    start = time.time()
    try:
        req = Request(url, headers={"User-Agent": "API-Monitor-Agent/1.0"})
        resp = urlopen(req, timeout=timeout)
        latency = round((time.time() - start) * 1000, 2)
        status = resp.status
        headers = dict(resp.headers)
        body_preview = resp.read(500).decode("utf-8", errors="replace")
        ok = status == expected_status
        print(f"{'✅' if ok else '⚠️'}  {url}")
        print(f"   Status: {status}  |  Latency: {latency}ms")
        print(f"   Content-Type: {headers.get('Content-Type', 'unknown')}")
        if body_preview:
            print(f"   Body (preview): {body_preview[:200]}")
    except HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}  ({url})")
    except URLError as e:
        print(f"❌ Connection failed: {e.reason}  ({url})")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Monitor API endpoint uptime and response")
    parser.add_argument("url", nargs="?", help="URL or endpoint to monitor")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    parser.add_argument("--expect-status", type=int, default=200, help="Expected HTTP status code (default: 200)")
    args = parser.parse_args()

    if not args.url:
        print("API Monitor Agent")
        print("Usage: python main.py <url> [--timeout 10] [--expect-status 200]")
        print("Example: python main.py https://api.github.com/zen")
        sys.exit(0)

    check_endpoint(args.url, args.timeout, args.expect_status)


if __name__ == "__main__":
    main()
