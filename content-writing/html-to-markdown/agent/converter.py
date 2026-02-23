"""HTML to Markdown converter — convert HTML content to clean markdown."""
from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass
class ConvertResult:
    html: str = ""; markdown: str = ""; is_valid: bool = True; error: str = ""
    def to_dict(self) -> dict: return {"html_len": len(self.html), "md_len": len(self.markdown), "is_valid": self.is_valid}

def html_to_markdown(html: str) -> ConvertResult:
    r = ConvertResult(html=html)
    try:
        md = html
        # Headers
        for i in range(6, 0, -1):
            md = re.sub(f'<h{i}[^>]*>(.*?)</h{i}>', lambda m: "#" * i + " " + m.group(1).strip(), md, flags=re.DOTALL)
        # Bold / italic
        md = re.sub(r'<(strong|b)>(.*?)</\1>', r'**\2**', md, flags=re.DOTALL)
        md = re.sub(r'<(em|i)>(.*?)</\1>', r'*\2*', md, flags=re.DOTALL)
        # Code
        md = re.sub(r'<code>(.*?)</code>', r'`\1`', md, flags=re.DOTALL)
        md = re.sub(r'<pre[^>]*>(.*?)</pre>', lambda m: f"```\n{m.group(1).strip()}\n```", md, flags=re.DOTALL)
        # Links and images
        md = re.sub(r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', md, flags=re.DOTALL)
        md = re.sub(r'<img\s+[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*/?\s*>', r'![\2](\1)', md)
        md = re.sub(r'<img\s+[^>]*src="([^"]*)"[^>]*/?\s*>', r'![](\1)', md)
        # Lists
        md = re.sub(r'<li[^>]*>(.*?)</li>', lambda m: f"- {m.group(1).strip()}", md, flags=re.DOTALL)
        md = re.sub(r'</?[uo]l[^>]*>', '', md)
        # Paragraphs and breaks
        md = re.sub(r'<p[^>]*>(.*?)</p>', lambda m: m.group(1).strip() + "\n\n", md, flags=re.DOTALL)
        md = re.sub(r'<br\s*/?>', '\n', md)
        md = re.sub(r'<hr\s*/?>', '---\n', md)
        # Blockquotes
        md = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: "> " + m.group(1).strip(), md, flags=re.DOTALL)
        # Strip remaining tags
        md = re.sub(r'<[^>]+>', '', md)
        # Clean up whitespace
        md = re.sub(r'\n{3,}', '\n\n', md).strip()
        r.markdown = md
    except Exception as e:
        r.is_valid = False; r.error = str(e)
    return r

def strip_tags(html: str) -> str:
    return re.sub(r'<[^>]+>', '', html).strip()

def extract_links(html: str) -> list[tuple[str, str]]:
    return re.findall(r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>', html, re.DOTALL)

def extract_images(html: str) -> list[str]:
    return re.findall(r'<img\s+[^>]*src="([^"]*)"', html)

def format_result_markdown(r: ConvertResult) -> str:
    if not r.is_valid: return f"## HTML→MD ❌\n**Error:** {r.error}"
    return f"## HTML→MD ✅\n**HTML:** {len(r.html)}B → **MD:** {len(r.markdown)}B\n\n{r.markdown[:200]}"
