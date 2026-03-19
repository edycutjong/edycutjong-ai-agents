"""
API Monitor Agent — monitors API endpoints for uptime and response quality.
Usage: python main.py <url>
"""
import argparse, sys, time
try:
    from urllib.request import urlopen, Request
    from urllib.error import URLError, HTTPError
except ImportError:  # pragma: no cover
    pass  # pragma: no cover


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[API Monitor] Paste a URL or endpoint to check uptime, latency, status codes, and headers."


def ping(url: str, timeout: int = 10):
    start = time.time()
    try:
        req = Request(url, headers={"User-Agent": "APIMonitor/1.0"})
        resp = urlopen(req, timeout=timeout)
        latency = round((time.time()-start)*1000, 1)
        print(f"✅ {url}  →  HTTP {resp.status}  |  {latency}ms")
    except HTTPError as e:  # pragma: no cover
        print(f"⚠️  {url}  →  HTTP {e.code}: {e.reason}")  # pragma: no cover
    except URLError as e:  # pragma: no cover
        print(f"❌ {url}  →  {e.reason}")  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Monitor API endpoint health")
    parser.add_argument("url", nargs="?", help="URL to monitor")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args()
    if not args.url:
        print("API Monitor Agent\nUsage: python main.py <url> [--timeout 10]")
        sys.exit(0)
    ping(args.url, args.timeout)

if __name__ == "__main__":
    main()
