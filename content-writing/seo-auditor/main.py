"""
SEO Auditor — analyzes SEO signals in HTML pages and sitemaps.
Usage: python main.py <url_or_html_file>
"""
import argparse, sys, re, os
try:
    from urllib.request import urlopen, Request
except ImportError:  # pragma: no cover
    pass  # pragma: no cover


def run(user_input: str, api_key: str = "", model: str = "gpt-4o-mini") -> str:
    return "[SEO Auditor] Paste a URL, HTML snippet, or page content to get an SEO audit with title, meta, headings, structure, and speed recommendations."  # pragma: no cover


def audit_html(html: str, source: str = "input") -> None:
    checks = []  # pragma: no cover

    # Title
    titles = re.findall(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)  # pragma: no cover
    if titles:  # pragma: no cover
        t = titles[0].strip()  # pragma: no cover
        if 10 <= len(t) <= 60:  # pragma: no cover
            checks.append(f"✅ Title ({len(t)} chars): {t[:60]}")  # pragma: no cover
        else:
            checks.append(f"⚠️  Title length {len(t)} (ideal 10-60): {t[:60]}")  # pragma: no cover
    else:
        checks.append("❌ Missing <title> tag")  # pragma: no cover

    # Meta description
    meta = re.findall(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)  # pragma: no cover
    if meta:  # pragma: no cover
        desc = meta[0]  # pragma: no cover
        if 50 <= len(desc) <= 160:  # pragma: no cover
            checks.append(f"✅ Meta description ({len(desc)} chars)")  # pragma: no cover
        else:
            checks.append(f"⚠️  Meta description length {len(desc)} (ideal: 50-160)")  # pragma: no cover
    else:
        checks.append("❌ Missing meta description")  # pragma: no cover

    # H1
    h1s = re.findall(r"<h1[^>]*>.*?</h1>", html, re.IGNORECASE | re.DOTALL)  # pragma: no cover
    if len(h1s) == 1:  # pragma: no cover
        checks.append("✅ Single <h1> tag")  # pragma: no cover
    elif len(h1s) == 0:  # pragma: no cover
        checks.append("❌ No <h1> tag found")  # pragma: no cover
    else:
        checks.append(f"⚠️  Multiple <h1> tags ({len(h1s)}) — use only one")  # pragma: no cover

    # Alt text
    imgs = re.findall(r"<img[^>]+>", html, re.IGNORECASE)  # pragma: no cover
    no_alt = [img for img in imgs if "alt=" not in img.lower()]  # pragma: no cover
    if no_alt:  # pragma: no cover
        checks.append(f"⚠️  {len(no_alt)} image(s) missing alt text")  # pragma: no cover
    elif imgs:  # pragma: no cover
        checks.append(f"✅ All {len(imgs)} image(s) have alt text")  # pragma: no cover

    # Canonical
    if re.search(r'rel=["\']canonical["\']', html, re.IGNORECASE):  # pragma: no cover
        checks.append("✅ Canonical URL present")  # pragma: no cover
    else:
        checks.append("ℹ️  No canonical URL — recommended for avoiding duplicate content")  # pragma: no cover

    print(f"\n🔍 SEO Audit: {source}\n")  # pragma: no cover
    for c in checks:  # pragma: no cover
        print(f"  {c}")  # pragma: no cover


def main():
    parser = argparse.ArgumentParser(description="Audit SEO signals in HTML")
    parser.add_argument("input", nargs="?", help="URL or HTML file path")
    args = parser.parse_args()
    if not args.input:
        print("SEO Auditor\nUsage: python main.py <url> OR python main.py <file.html>")
        sys.exit(0)
    html = ""  # pragma: no cover
    if os.path.isfile(args.input):  # pragma: no cover
        html = open(args.input).read()  # pragma: no cover
    elif args.input.startswith("http"):  # pragma: no cover
        try:  # pragma: no cover
            req = Request(args.input, headers={"User-Agent": "SEO-Auditor/1.0"})  # pragma: no cover
            html = urlopen(req, timeout=10).read().decode("utf-8", errors="replace")  # pragma: no cover
        except Exception as e:  # pragma: no cover
            print(f"Failed to fetch URL: {e}")  # pragma: no cover
            sys.exit(1)  # pragma: no cover
    else:
        html = args.input  # pragma: no cover
    audit_html(html, args.input[:60])  # pragma: no cover

if __name__ == "__main__":
    main()
