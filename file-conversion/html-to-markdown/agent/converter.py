"""HTML to Markdown converter — convert HTML content to clean Markdown."""
from __future__ import annotations
import re
from dataclasses import dataclass

def html_to_markdown(html: str) -> str:
    """Convert HTML string to Markdown."""
    text = html
    # Remove scripts and styles
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.I)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.I)
    # Headers
    for i in range(6, 0, -1):
        text = re.sub(rf"<h{i}[^>]*>(.*?)</h{i}>", lambda m: f"\n{'#' * i} {m.group(1).strip()}\n", text, flags=re.DOTALL | re.I)
    # Bold and italic
    text = re.sub(r"<(strong|b)>(.*?)</\1>", r"**\2**", text, flags=re.DOTALL | re.I)
    text = re.sub(r"<(em|i)>(.*?)</\1>", r"*\2*", text, flags=re.DOTALL | re.I)
    # Code
    text = re.sub(r"<code>(.*?)</code>", r"`\1`", text, flags=re.DOTALL | re.I)
    text = re.sub(r"<pre[^>]*>(.*?)</pre>", lambda m: f"\n```\n{strip_tags(m.group(1)).strip()}\n```\n", text, flags=re.DOTALL | re.I)
    # Links
    text = re.sub(r'<a[^>]*href=["\']([^"\']*)["\'][^>]*>(.*?)</a>', r"[\2](\1)", text, flags=re.DOTALL | re.I)
    # Images
    text = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>',r"![\2](\1)", text, flags=re.I)
    text = re.sub(r'<img[^>]*src=["\']([^"\']*)["\'][^>]*/?>',r"![](\1)", text, flags=re.I)
    # Lists
    text = re.sub(r"<li[^>]*>(.*?)</li>", r"- \1", text, flags=re.DOTALL | re.I)
    text = re.sub(r"</?[ou]l[^>]*>", "\n", text, flags=re.I)
    # Paragraphs and breaks
    text = re.sub(r"<p[^>]*>(.*?)</p>", r"\n\1\n", text, flags=re.DOTALL | re.I)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<hr\s*/?>", "\n---\n", text, flags=re.I)
    # Blockquotes
    text = re.sub(r"<blockquote[^>]*>(.*?)</blockquote>", lambda m: "\n".join(f"> {line}" for line in m.group(1).strip().split("\n")), text, flags=re.DOTALL | re.I)
    # Tables (simplified)
    text = re.sub(r"<tr[^>]*>(.*?)</tr>", lambda m: "| " + " | ".join(re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", m.group(1), re.DOTALL | re.I)) + " |", text, flags=re.DOTALL | re.I)
    text = re.sub(r"</?table[^>]*>", "\n", text, flags=re.I)
    text = re.sub(r"</?thead[^>]*>", "", text, flags=re.I)
    text = re.sub(r"</?tbody[^>]*>", "", text, flags=re.I)
    # Strip remaining tags
    text = strip_tags(text)
    # HTML entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    # Clean up whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", "", text)

def convert_file(filepath: str) -> str:
    with open(filepath) as f: return html_to_markdown(f.read())

@dataclass
class ConversionStats:
    input_chars: int = 0
    output_chars: int = 0
    tags_removed: int = 0
    @property
    def reduction_pct(self) -> float:
        if self.input_chars == 0: return 0
        return round((1 - self.output_chars / self.input_chars) * 100, 1)

def convert_with_stats(html: str) -> tuple[str, ConversionStats]:
    tags = len(re.findall(r"<[^>]+>", html))
    md = html_to_markdown(html)
    return md, ConversionStats(input_chars=len(html), output_chars=len(md), tags_removed=tags)
