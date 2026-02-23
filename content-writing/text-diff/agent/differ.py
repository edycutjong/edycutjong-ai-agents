"""Text diff — compare two texts and show additions, deletions, and changes."""
from __future__ import annotations
import difflib
from dataclasses import dataclass, field

@dataclass
class DiffLine:
    line_num: int = 0; content: str = ""; kind: str = "equal"  # added, removed, equal

@dataclass
class DiffResult:
    lines: list[DiffLine] = field(default_factory=list)
    added: int = 0; removed: int = 0; changed: int = 0
    similarity: float = 0.0
    def to_dict(self) -> dict: return {"added": self.added, "removed": self.removed, "similarity": self.similarity}

def diff_texts(text1: str, text2: str) -> DiffResult:
    r = DiffResult()
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)
    r.similarity = round(difflib.SequenceMatcher(None, text1, text2).ratio() * 100, 1)
    matcher = difflib.SequenceMatcher(None, lines1, lines2)
    line_num = 0
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for line in lines1[i1:i2]:
                line_num += 1; r.lines.append(DiffLine(line_num, line.rstrip(), "equal"))
        elif tag == "insert":
            for line in lines2[j1:j2]:
                line_num += 1; r.lines.append(DiffLine(line_num, line.rstrip(), "added")); r.added += 1
        elif tag == "delete":
            for line in lines1[i1:i2]:
                line_num += 1; r.lines.append(DiffLine(line_num, line.rstrip(), "removed")); r.removed += 1
        elif tag == "replace":
            for line in lines1[i1:i2]:
                line_num += 1; r.lines.append(DiffLine(line_num, line.rstrip(), "removed")); r.removed += 1
            for line in lines2[j1:j2]:
                line_num += 1; r.lines.append(DiffLine(line_num, line.rstrip(), "added")); r.added += 1
    r.changed = min(r.added, r.removed)
    return r

def unified_diff(text1: str, text2: str, from_file: str = "original", to_file: str = "modified") -> str:
    lines1 = text1.splitlines(keepends=True)
    lines2 = text2.splitlines(keepends=True)
    return "".join(difflib.unified_diff(lines1, lines2, fromfile=from_file, tofile=to_file))

def word_diff(text1: str, text2: str) -> list[tuple[str, str]]:
    words1 = text1.split(); words2 = text2.split()
    sm = difflib.SequenceMatcher(None, words1, words2)
    result = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal": result.extend(("equal", w) for w in words1[i1:i2])
        elif tag == "insert": result.extend(("added", w) for w in words2[j1:j2])
        elif tag == "delete": result.extend(("removed", w) for w in words1[i1:i2])
        elif tag == "replace":
            result.extend(("removed", w) for w in words1[i1:i2])
            result.extend(("added", w) for w in words2[j1:j2])
    return result

def format_result_markdown(r: DiffResult) -> str:
    lines = [f"## Text Diff 📝", f"**Added:** {r.added} | **Removed:** {r.removed} | **Similarity:** {r.similarity}%", ""]
    for dl in r.lines[:30]:
        prefix = "+" if dl.kind == "added" else "-" if dl.kind == "removed" else " "
        lines.append(f"`{prefix}` {dl.content}")
    return "\n".join(lines)
