"""Quiz generator — create quizzes from topics or text content."""
from __future__ import annotations
import json, random, re, hashlib
from dataclasses import dataclass, field

@dataclass
class Question:
    text: str
    options: list[str] = field(default_factory=list)
    correct: int = 0  # index of correct option
    explanation: str = ""
    difficulty: str = "medium"  # easy, medium, hard
    category: str = ""
    def to_dict(self) -> dict:
        return self.__dict__.copy()
    @property
    def correct_answer(self) -> str:
        return self.options[self.correct] if self.options and self.correct < len(self.options) else ""

@dataclass
class Quiz:
    title: str
    questions: list[Question] = field(default_factory=list)
    passing_score: float = 70.0
    def to_dict(self) -> dict:
        return {"title": self.title, "questions": [q.to_dict() for q in self.questions], "passing_score": self.passing_score, "total": len(self.questions)}

@dataclass
class QuizResult:
    total: int = 0
    correct: int = 0
    wrong: int = 0
    score: float = 0
    passed: bool = False
    answers: list[dict] = field(default_factory=list)

QUESTION_BANK = {
    "python": [
        Question(text="What is the output of `len([1, 2, 3])`?", options=["2", "3", "4", "Error"], correct=1, explanation="len() returns the number of items.", category="python"),
        Question(text="Which keyword is used to define a function?", options=["func", "define", "def", "function"], correct=2, explanation="Python uses 'def' keyword.", category="python"),
        Question(text="What type is `True` in Python?", options=["int", "bool", "str", "bit"], correct=1, explanation="True and False are booleans.", category="python"),
        Question(text="What does `//` do in Python?", options=["Comment", "Division", "Floor division", "Modulo"], correct=2, explanation="// performs integer/floor division.", category="python"),
        Question(text="Which is mutable?", options=["str", "tuple", "list", "frozenset"], correct=2, explanation="Lists are mutable in Python.", category="python"),
    ],
    "javascript": [
        Question(text="What is `typeof null`?", options=["null", "undefined", "object", "boolean"], correct=2, explanation="typeof null returns 'object' — a known JS bug.", category="javascript"),
        Question(text="Which method adds to the end of an array?", options=["push()", "pop()", "shift()", "unshift()"], correct=0, explanation="push() adds elements to the end.", category="javascript"),
        Question(text="What is `NaN === NaN`?", options=["true", "false", "undefined", "Error"], correct=1, explanation="NaN is not equal to anything, including itself.", category="javascript"),
        Question(text="Which declares a constant?", options=["var", "let", "const", "fixed"], correct=2, explanation="const declares a constant variable.", category="javascript"),
    ],
    "general-cs": [
        Question(text="What is O(1)?", options=["Linear time", "Constant time", "Quadratic time", "Log time"], correct=1, explanation="O(1) means constant time complexity.", category="general-cs"),
        Question(text="What does SQL stand for?", options=["Structured Query Language", "Simple Query Language", "Standard Query Logic", "Sequential Query Language"], correct=0, category="general-cs"),
        Question(text="What is a stack?", options=["FIFO", "LIFO", "Random access", "Tree"], correct=1, explanation="Stack is Last In, First Out.", category="general-cs"),
    ],
}

def generate_quiz(topic: str, count: int = 5, difficulty: str | None = None) -> Quiz:
    """Generate a quiz from the question bank."""
    bank = QUESTION_BANK.get(topic.lower(), [])
    if not bank:
        all_qs = [q for qs in QUESTION_BANK.values() for q in qs]
        bank = all_qs
    if difficulty:
        filtered = [q for q in bank if q.difficulty == difficulty]
        if filtered: bank = filtered
    selected = random.sample(bank, min(count, len(bank)))
    return Quiz(title=f"{topic.title()} Quiz", questions=selected)

def grade_quiz(quiz: Quiz, answers: list[int]) -> QuizResult:
    """Grade a quiz given user answers (indexes)."""
    result = QuizResult(total=len(quiz.questions))
    for i, q in enumerate(quiz.questions):
        user_ans = answers[i] if i < len(answers) else -1
        is_correct = user_ans == q.correct
        if is_correct: result.correct += 1
        else: result.wrong += 1
        result.answers.append({"question": q.text, "user_answer": user_ans, "correct_answer": q.correct, "is_correct": is_correct})
    result.score = round(result.correct / max(result.total, 1) * 100, 1)
    result.passed = result.score >= quiz.passing_score
    return result

def format_quiz_markdown(quiz: Quiz) -> str:
    lines = [f"# {quiz.title}", f"**Questions:** {len(quiz.questions)} | **Passing:** {quiz.passing_score}%", ""]
    for i, q in enumerate(quiz.questions, 1):
        lines.append(f"### Q{i}. {q.text}")
        for j, opt in enumerate(q.options):
            lines.append(f"  {'ABCD'[j]}. {opt}")
        lines.append("")
    return "\n".join(lines)

def format_results_markdown(result: QuizResult) -> str:
    emoji = "✅" if result.passed else "❌"
    lines = [f"# Quiz Results {emoji}", f"**Score:** {result.score}% ({result.correct}/{result.total})", f"**Status:** {'PASSED' if result.passed else 'FAILED'}", ""]
    for a in result.answers:
        e = "✅" if a["is_correct"] else "❌"
        lines.append(f"- {e} {a['question']}")
    return "\n".join(lines)
