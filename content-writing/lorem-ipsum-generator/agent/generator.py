"""Lorem ipsum generator — generate placeholder text with options."""
from __future__ import annotations
import random
from dataclasses import dataclass

WORDS = "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua ut enim ad minim veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt in culpa qui officia deserunt mollit anim id est laborum".split()

@dataclass
class LoremResult:
    text: str = ""; word_count: int = 0; paragraph_count: int = 0; sentence_count: int = 0; char_count: int = 0
    def to_dict(self) -> dict: return {"words": self.word_count, "paragraphs": self.paragraph_count, "chars": self.char_count}

def generate_words(count: int, start_with_lorem: bool = True) -> str:
    if count <= 0: return ""
    words = []
    if start_with_lorem:
        words.extend(WORDS[:min(count, len(WORDS))])
        count -= len(words)
    while count > 0:
        batch = min(count, len(WORDS))
        words.extend(random.sample(WORDS, batch))
        count -= batch
    return " ".join(words)

def generate_sentences(count: int, words_per_sentence: tuple = (5, 15)) -> str:
    sents = []
    for i in range(count):
        n = random.randint(*words_per_sentence)
        s = generate_words(n, start_with_lorem=(i == 0))
        sents.append(s[0].upper() + s[1:] + ".")
    return " ".join(sents)

def generate_paragraphs(count: int, sentences_per_para: tuple = (3, 7)) -> str:
    paras = []
    for i in range(count):
        n = random.randint(*sentences_per_para)
        paras.append(generate_sentences(n))
    return "\n\n".join(paras)

def generate(words: int = 0, sentences: int = 0, paragraphs: int = 0) -> LoremResult:
    r = LoremResult()
    if paragraphs > 0:
        r.text = generate_paragraphs(paragraphs); r.paragraph_count = paragraphs
    elif sentences > 0:
        r.text = generate_sentences(sentences); r.sentence_count = sentences
    elif words > 0:
        r.text = generate_words(words); r.word_count = words
    else:
        r.text = generate_paragraphs(3); r.paragraph_count = 3
    r.char_count = len(r.text)
    r.word_count = len(r.text.split())
    return r

def format_result_markdown(r: LoremResult) -> str:
    return f"## Lorem Ipsum 📝\n**Words:** {r.word_count} | **Chars:** {r.char_count}\n\n{r.text[:200]}..."
