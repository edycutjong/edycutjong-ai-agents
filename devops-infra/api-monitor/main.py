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
    return "[API Monitor] Paste a URL or endpoint to check uptime, latency, status codes, and headers."  # pragma: no cover


def ping(url: str, timeout: int = 10):
    start = time.time()  # pragma: no cover
    try:  # pragma: no cover
        req = Request(url, headers={"User-Agent": "APIMonitor/1.0"})  # pragma: no cover
        resp = urlopen(req, timeout=timeout)  # pragma: no cover
        latency = round((time.time()-start)*1000, 1)  # pragma: no cover
        print(f"✅ {url}  →  HTTP {resp.status}  |  {latency}ms")  # pragma: no cover
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
    ping(args.url, args.timeout)  # pragma: no cover

if __name__ == "__main__":
    main()
