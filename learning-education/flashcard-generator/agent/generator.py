"""Flashcard generator — create study cards from text, terms, or topics."""
from __future__ import annotations
import json, random, re, uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Flashcard:
    front: str
    back: str
    id: str = ""
    tags: list[str] = field(default_factory=list)
    difficulty: int = 1  # 1-5
    times_reviewed: int = 0
    times_correct: int = 0
    def __post_init__(self):
        if not self.id: self.id = uuid.uuid4().hex[:8]
    @property
    def accuracy(self) -> float:
        return round(self.times_correct / max(self.times_reviewed, 1) * 100, 1)
    def to_dict(self) -> dict:
        return {"id": self.id, "front": self.front, "back": self.back, "tags": self.tags, "difficulty": self.difficulty, "accuracy": self.accuracy}

@dataclass
class Deck:
    name: str
    cards: list[Flashcard] = field(default_factory=list)
    created_at: str = ""
    def __post_init__(self):
        if not self.created_at: self.created_at = datetime.now().isoformat()
    def add(self, card: Flashcard): self.cards.append(card)
    @property
    def size(self) -> int: return len(self.cards)
    def to_dict(self) -> dict:
        return {"name": self.name, "cards": [c.to_dict() for c in self.cards], "size": self.size}

TOPIC_CARDS = {
    "python": [
        Flashcard(front="What is a list comprehension?", back="A concise way to create lists: [x for x in range(10)]"),
        Flashcard(front="What is a decorator?", back="A function that wraps another function to extend its behavior using @syntax"),
        Flashcard(front="What is __init__?", back="The constructor method called when creating an instance of a class"),
        Flashcard(front="Difference between list and tuple?", back="Lists are mutable, tuples are immutable"),
        Flashcard(front="What is a generator?", back="A function using yield to return values lazily, one at a time"),
    ],
    "javascript": [
        Flashcard(front="What is a closure?", back="A function that retains access to its outer scope variables"),
        Flashcard(front="Difference: == vs ===?", back="== coerces types, === checks strict equality (type + value)"),
        Flashcard(front="What is the event loop?", back="Mechanism that handles async callbacks in a single-threaded runtime"),
        Flashcard(front="What is 'this'?", back="Refers to the execution context; varies based on how a function is called"),
    ],
    "git": [
        Flashcard(front="git rebase vs merge?", back="Rebase replays commits linearly, merge creates a merge commit"),
        Flashcard(front="What is git stash?", back="Temporarily shelves changes so you can work on something else"),
        Flashcard(front="What is HEAD?", back="A pointer to the current commit/branch you're on"),
    ],
}

def generate_from_topic(topic: str, count: int = 10) -> Deck:
    bank = TOPIC_CARDS.get(topic.lower(), [])
    if not bank:
        all_cards = [c for cs in TOPIC_CARDS.values() for c in cs]
        bank = all_cards
    selected = random.sample(bank, min(count, len(bank)))
    return Deck(name=f"{topic.title()} Flashcards", cards=selected)

def generate_from_terms(terms: dict[str, str], deck_name: str = "Custom") -> Deck:
    cards = [Flashcard(front=term, back=defn) for term, defn in terms.items()]
    return Deck(name=deck_name, cards=cards)

def generate_from_text(text: str, deck_name: str = "Study") -> Deck:
    """Extract key terms from text (sentences containing ':' or '-')."""
    cards = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line: continue
        for sep in [":", " - ", " — "]:
            if sep in line:
                parts = line.split(sep, 1)
                if len(parts) == 2 and len(parts[0].strip()) > 2:
                    cards.append(Flashcard(front=parts[0].strip().lstrip("- "), back=parts[1].strip()))
                    break
    return Deck(name=deck_name, cards=cards)

def review_session(deck: Deck, shuffle: bool = True) -> list[dict]:
    """Create a review session order."""
    cards = list(deck.cards)
    if shuffle: random.shuffle(cards)
    return [{"index": i, "front": c.front, "id": c.id} for i, c in enumerate(cards)]

def export_anki(deck: Deck) -> str:
    """Export deck in Anki-compatible TSV format."""
    lines = []
    for c in deck.cards:
        front = c.front.replace("\t", " ").replace("\n", " ")
        back = c.back.replace("\t", " ").replace("\n", " ")
        tags = " ".join(c.tags) if c.tags else ""
        lines.append(f"{front}\t{back}\t{tags}")
    return "\n".join(lines)

def format_deck_markdown(deck: Deck) -> str:
    lines = [f"# {deck.name}", f"**Cards:** {deck.size}", ""]
    for i, c in enumerate(deck.cards, 1):
        lines.append(f"### Card {i}")
        lines.append(f"**Q:** {c.front}")
        lines.append(f"**A:** {c.back}")
        lines.append("")
    return "\n".join(lines)
