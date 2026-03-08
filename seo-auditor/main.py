"""
SEO Auditor — analyzes SEO signals in HTML pages and sitemaps.
Usage: python main.py <url_or_html_file>
"""
import argparse, sys, re, os
try:
    from urllib.request import urlopen, Request
except ImportError:
    pass


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[SEO Auditor] Paste a URL, HTML snippet, or page content to get an SEO audit with title, meta, headings, structure, and speed recommendations."


def audit_html(html: str, source: str = "input") -> None:
    checks = []

    # Title
    titles = re.findall(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if titles:
        t = titles[0].strip()
        if 10 <= len(t) <= 60:
            checks.append(f"✅ Title ({len(t)} chars): {t[:60]}")
        else:
            checks.append(f"⚠️  Title length {len(t)} (ideal 10-60): {t[:60]}")
    else:
        checks.append("❌ Missing <title> tag")

    # Meta description
    meta = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    if meta:
        desc = meta[0]
        if 50 <= len(desc) <= 160:
            checks.append(f"✅ Meta description ({len(desc)} chars)")
        else:
            checks.append(f"⚠️  Meta description length {len(desc)} (ideal: 50-160)")
    else:
        checks.append("❌ Missing meta description")

    # H1
    h1s = re.findall(r"<h1[^>]*>.*?</h1>", html, re.IGNORECASE | re.DOTALL)
    if len(h1s) == 1:
        checks.append("✅ Single <h1> tag")
    elif len(h1s) == 0:
        checks.append("❌ No <h1> tag found")
    else:
        checks.append(f"⚠️  Multiple <h1> tags ({len(h1s)}) — use only one")

    # Alt text
    imgs = re.findall(r"<img[^>]+>", html, re.IGNORECASE)
    no_alt = [img for img in imgs if "alt=" not in img.lower()]
    if no_alt:
        checks.append(f"⚠️  {len(no_alt)} image(s) missing alt text")
    elif imgs:
        checks.append(f"✅ All {len(imgs)} image(s) have alt text")

    # Canonical
    if re.search(r'rel=["\']canonical["\']', html, re.IGNORECASE):
        checks.append("✅ Canonical URL present")
    else:
        checks.append("ℹ️  No canonical URL — recommended for avoiding duplicate content")

    print(f"\n🔍 SEO Audit: {source}\n")
    for c in checks:
        print(f"  {c}")


def main():
    parser = argparse.ArgumentParser(description="Audit SEO signals in HTML")
    parser.add_argument("input", nargs="?", help="URL or HTML file path")
    args = parser.parse_args()
    if not args.input:
        print("SEO Auditor\nUsage: python main.py <url> OR python main.py <file.html>")
        sys.exit(0)
    html = ""
    if os.path.isfile(args.input):
        html = open(args.input).read()
    elif args.input.startswith("http"):
        try:
            req = Request(args.input, headers={"User-Agent": "SEO-Auditor/1.0"})
            html = urlopen(req, timeout=10).read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"Failed to fetch URL: {e}")
            sys.exit(1)
    else:
        html = args.input
    audit_html(html, args.input[:60])

if __name__ == "__main__":
    main()
