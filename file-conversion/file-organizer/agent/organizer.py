"""File organizer — categorize and organize files by type, size, and date."""
from __future__ import annotations
import os
from dataclasses import dataclass, field
from collections import Counter

CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".csv", ".ppt", ".pptx"},
    "code": {".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".go", ".rs", ".rb", ".php", ".swift", ".kt"},
    "data": {".json", ".yaml", ".yml", ".xml", ".toml", ".ini", ".cfg", ".env", ".sql"},
    "media": {".mp4", ".avi", ".mkv", ".mov", ".mp3", ".wav", ".flac", ".ogg", ".aac"},
    "archives": {".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz"},
    "web": {".html", ".htm", ".css", ".scss", ".less", ".wasm"},
}

@dataclass
class FileInfo:
    path: str; name: str; extension: str; category: str; size: int = 0

@dataclass
class OrganizeResult:
    total_files: int = 0; categories: dict = field(default_factory=dict)
    largest_files: list[FileInfo] = field(default_factory=list)
    extensions: dict = field(default_factory=dict); total_size: int = 0

def categorize_file(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts: return cat
    return "other"

def get_extension(filename: str) -> str:
    return os.path.splitext(filename)[1].lower()

def organize_file_list(files: list[dict]) -> OrganizeResult:
    r = OrganizeResult(total_files=len(files))
    cat_counter, ext_counter, infos = Counter(), Counter(), []
    for f in files:
        name, size = f.get("name", ""), f.get("size", 0)
        ext, cat = get_extension(name), categorize_file(name)
        cat_counter[cat] += 1
        if ext: ext_counter[ext] += 1
        r.total_size += size
        infos.append(FileInfo(path=f.get("path", name), name=name, extension=ext, category=cat, size=size))
    r.categories = dict(cat_counter.most_common())
    r.extensions = dict(ext_counter.most_common(10))
    r.largest_files = sorted(infos, key=lambda x: x.size, reverse=True)[:5]
    return r

def suggest_structure(result: OrganizeResult) -> list[str]:
    suggestions = []
    for cat, count in result.categories.items():
        if count >= 3: suggestions.append(f"Create a '{cat}/' folder for {count} files")
    if result.total_files > 20: suggestions.append("Consider adding a README for organization")
    return suggestions

def format_result_markdown(r: OrganizeResult) -> str:
    lines = ["## File Organization", f"**Total:** {r.total_files} files | **Size:** {r.total_size:,} bytes", ""]
    if r.categories:
        lines.append("### Categories")
        for cat, count in r.categories.items(): lines.append(f"- **{cat}:** {count} files")
    suggestions = suggest_structure(r)
    if suggestions:
        lines.append("\n### Suggestions")
        for s in suggestions: lines.append(f"- 💡 {s}")
    return "\n".join(lines)
