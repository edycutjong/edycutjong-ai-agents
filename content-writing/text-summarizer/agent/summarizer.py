"""Text summarizer — extractive summarization of text content."""
from __future__ import annotations
import re, math
from dataclasses import dataclass, field
from collections import Counter

@dataclass
class SummaryResult:
    original_length: int = 0
    summary_length: int = 0
    compression_ratio: float = 0.0
    sentence_count: int = 0
    summary_sentences: int = 0
    summary: str = ""
    keywords: list[str] = field(default_factory=list)
    def to_dict(self) -> dict:
        return {"original_length": self.original_length, "summary_length": self.summary_length, "compression_ratio": round(self.compression_ratio, 2), "keywords": self.keywords[:5]}

STOP_WORDS = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "shall", "can", "need", "dare", "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by", "from", "as", "into", "through", "during", "before", "after", "above", "below", "between", "out", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "and", "but", "or", "if", "while", "that", "this", "it", "its", "i", "me", "my", "we", "our", "you", "your", "he", "him", "his", "she", "her", "they", "them", "their", "what", "which", "who", "whom"}

def split_sentences(text: str) -> list[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if len(s.strip()) > 10]

def extract_keywords(text: str, top_n: int = 10) -> list[str]:
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    words = [w for w in words if w not in STOP_WORDS]
    counter = Counter(words)
    return [word for word, _ in counter.most_common(top_n)]

def score_sentence(sentence: str, keywords: list[str], position: int, total: int) -> float:
    words = re.findall(r'\b[a-z]+\b', sentence.lower())
    if not words: return 0
    keyword_score = sum(1 for w in words if w in keywords) / len(words)
    position_score = 1.0 if position < 2 else (0.5 if position == total - 1 else 0.2)
    length_score = min(len(words) / 20, 1.0)
    return keyword_score * 0.5 + position_score * 0.3 + length_score * 0.2

def summarize(text: str, ratio: float = 0.3, max_sentences: int = 5) -> SummaryResult:
    r = SummaryResult(original_length=len(text))
    sentences = split_sentences(text)
    r.sentence_count = len(sentences)
    if not sentences:
        r.summary = text[:200]
        r.summary_length = len(r.summary)
        return r
    r.keywords = extract_keywords(text)
    target = max(1, min(max_sentences, int(len(sentences) * ratio)))
    scores = [(i, score_sentence(s, r.keywords, i, len(sentences))) for i, s in enumerate(sentences)]
    scores.sort(key=lambda x: x[1], reverse=True)
    selected = sorted([idx for idx, _ in scores[:target]])
    r.summary = " ".join(sentences[i] for i in selected)
    r.summary_length = len(r.summary)
    r.summary_sentences = len(selected)
    r.compression_ratio = r.summary_length / max(r.original_length, 1)
    return r

def format_result_markdown(r: SummaryResult) -> str:
    lines = ["## Summary", r.summary, "", f"**Original:** {r.original_length} chars ({r.sentence_count} sentences)", f"**Summary:** {r.summary_length} chars ({r.summary_sentences} sentences)", f"**Compression:** {r.compression_ratio:.0%}"]
    if r.keywords:
        lines.append(f"\n**Keywords:** {', '.join(r.keywords[:5])}")
    return "\n".join(lines)
