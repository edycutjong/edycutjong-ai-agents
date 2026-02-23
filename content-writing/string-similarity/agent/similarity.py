"""String similarity — compare strings using various distance algorithms."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class SimilarityResult:
    text1: str = ""; text2: str = ""; ratio: float = 0.0; distance: int = 0; algorithm: str = ""
    def to_dict(self) -> dict: return {"ratio": self.ratio, "distance": self.distance, "algorithm": self.algorithm}

def levenshtein(s1: str, s2: str) -> int:
    if len(s1) < len(s2): return levenshtein(s2, s1)
    if not s2: return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            curr.append(min(prev[j + 1] + 1, curr[j] + 1, prev[j] + (c1 != c2)))
        prev = curr
    return prev[-1]

def jaro_winkler(s1: str, s2: str) -> float:
    if s1 == s2: return 1.0
    l1, l2 = len(s1), len(s2)
    if not l1 or not l2: return 0.0
    window = max(l1, l2) // 2 - 1
    m1 = [False] * l1; m2 = [False] * l2; matches = 0; transpositions = 0
    for i in range(l1):
        lo, hi = max(0, i - window), min(l2, i + window + 1)
        for j in range(lo, hi):
            if m2[j] or s1[i] != s2[j]: continue
            m1[i] = m2[j] = True; matches += 1; break
    if not matches: return 0.0
    k = 0
    for i in range(l1):
        if not m1[i]: continue
        while not m2[k]: k += 1
        if s1[i] != s2[k]: transpositions += 1
        k += 1
    jaro = (matches / l1 + matches / l2 + (matches - transpositions / 2) / matches) / 3
    prefix = sum(1 for i in range(min(4, min(l1, l2))) if s1[i] == s2[i])
    return round(jaro + prefix * 0.1 * (1 - jaro), 4)

def similarity_ratio(s1: str, s2: str) -> float:
    dist = levenshtein(s1, s2)
    return round(1 - dist / max(len(s1), len(s2), 1), 4)

def compare(s1: str, s2: str, algorithm: str = "levenshtein") -> SimilarityResult:
    r = SimilarityResult(text1=s1, text2=s2, algorithm=algorithm)
    if algorithm == "jaro_winkler":
        r.ratio = jaro_winkler(s1, s2)
    else:
        r.distance = levenshtein(s1, s2); r.ratio = similarity_ratio(s1, s2)
    return r

def closest_match(target: str, candidates: list[str]) -> str:
    if not candidates: return ""
    return min(candidates, key=lambda c: levenshtein(target, c))

def format_result_markdown(r: SimilarityResult) -> str:
    return f"## String Similarity 🔤\n**Ratio:** {r.ratio:.1%} | **Distance:** {r.distance} | **Algorithm:** {r.algorithm}"
