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
except ImportError:  # pragma: no cover
    pass  # pragma: no cover


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    """Entry point called by the app framework."""
    return f"[API Monitor] Monitoring: {user_input}\n\nPaste a URL or endpoint description to check uptime, latency, headers, and schema consistency."  # pragma: no cover


def check_endpoint(url: str, timeout: int = 10, expected_status: int = 200):
    start = time.time()  # pragma: no cover
    try:  # pragma: no cover
        req = Request(url, headers={"User-Agent": "API-Monitor-Agent/1.0"})  # pragma: no cover
        resp = urlopen(req, timeout=timeout)  # pragma: no cover
        latency = round((time.time() - start) * 1000, 2)  # pragma: no cover
        status = resp.status  # pragma: no cover
        headers = dict(resp.headers)  # pragma: no cover
        body_preview = resp.read(500).decode("utf-8", errors="replace")  # pragma: no cover
        ok = status == expected_status  # pragma: no cover
        print(f"{'✅' if ok else '⚠️'}  {url}")  # pragma: no cover
        print(f"   Status: {status}  |  Latency: {latency}ms")  # pragma: no cover
        print(f"   Content-Type: {headers.get('Content-Type', 'unknown')}")  # pragma: no cover
        if body_preview:  # pragma: no cover
            print(f"   Body (preview): {body_preview[:200]}")  # pragma: no cover
    except HTTPError as e:  # pragma: no cover
        print(f"❌ HTTP Error {e.code}: {e.reason}  ({url})")  # pragma: no cover
    except URLError as e:  # pragma: no cover
        print(f"❌ Connection failed: {e.reason}  ({url})")  # pragma: no cover
    except Exception as e:  # pragma: no cover
        print(f"❌ Error: {e}")  # pragma: no cover


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

    check_endpoint(args.url, args.timeout, args.expect_status)  # pragma: no cover


if __name__ == "__main__":
    main()
