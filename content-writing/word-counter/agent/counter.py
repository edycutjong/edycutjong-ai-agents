"""Word counter — count words, characters, sentences, and reading time."""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from collections import Counter

@dataclass
class WordCountResult:
    words: int = 0; characters: int = 0; characters_no_spaces: int = 0
    sentences: int = 0; paragraphs: int = 0; lines: int = 0
    reading_time_min: float = 0; top_words: list = field(default_factory=list)
    unique_words: int = 0; avg_word_length: float = 0
    def to_dict(self) -> dict: return {"words": self.words, "characters": self.characters, "sentences": self.sentences, "reading_time_min": self.reading_time_min}

STOP_WORDS = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "is", "was", "it", "this", "that", "be", "are", "were", "i", "you", "we", "they"}

def count_words(text: str, wpm: int = 200) -> WordCountResult:
    r = WordCountResult()
    r.characters = len(text)
    r.characters_no_spaces = len(text.replace(" ", ""))
    r.lines = text.count("\n") + 1 if text else 0
    r.paragraphs = len([p for p in text.split("\n\n") if p.strip()])
    words = re.findall(r'\b\w+\b', text.lower())
    r.words = len(words)
    r.sentences = len(re.findall(r'[.!?]+', text))
    r.reading_time_min = round(r.words / wpm, 1)
    r.unique_words = len(set(words))
    r.avg_word_length = round(sum(len(w) for w in words) / max(len(words), 1), 1)
    content_words = [w for w in words if w not in STOP_WORDS]
    counter = Counter(content_words)
    r.top_words = [(w, c) for w, c in counter.most_common(10)]
    return r

def keyword_density(text: str, keyword: str) -> float:
    r = count_words(text)
    kw_count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text.lower()))
    return round(kw_count / max(r.words, 1) * 100, 2)

def flesch_reading_ease(text: str) -> float:
    words = re.findall(r'\b\w+\b', text)
    sentences = max(len(re.findall(r'[.!?]+', text)), 1)
    syllables = sum(_count_syllables(w) for w in words)
    if not words: return 0
    return round(206.835 - 1.015 * (len(words) / sentences) - 84.6 * (syllables / len(words)), 1)

def _count_syllables(word: str) -> int:
    word = word.lower().rstrip("e")
    return max(1, len(re.findall(r'[aeiou]', word)))

def compare_texts(text1: str, text2: str) -> dict:
    r1, r2 = count_words(text1), count_words(text2)
    return {"words_diff": r2.words - r1.words, "reading_time_diff": r2.reading_time_min - r1.reading_time_min}

def format_result_markdown(r: WordCountResult) -> str:
    lines = [f"## Word Count 📊", f"**Words:** {r.words} | **Chars:** {r.characters} | **Sentences:** {r.sentences}", f"**Reading time:** ~{r.reading_time_min} min | **Unique words:** {r.unique_words}", ""]
    if r.top_words:
        lines.append("### Top Words")
        lines.append(", ".join(f"`{w}` ({c})" for w, c in r.top_words[:5]))
    return "\n".join(lines)
