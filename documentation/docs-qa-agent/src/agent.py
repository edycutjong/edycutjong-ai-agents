"""Docs QA Agent — core Gemini logic."""
import json
import os
import google.generativeai as genai
from config import Config

QA_PROMPT = """\
You are a documentation expert. Given the following documentation content, answer the user's question accurately.

Produce a JSON object with these fields:
- answer: the answer to the question
- sources: list of relevant sections or file names that support the answer
- confidence: float 0.0-1.0 indicating confidence in the answer
- follow_up_questions: list of 2-3 suggested follow-up questions
- tasks: list of any actionable tasks extracted from the answer

Documentation:
{docs}

Question: {question}

Respond ONLY with valid JSON.
"""


class DocsQAAgent:
    """Answer questions about documentation using Gemini."""

    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.MODEL)

    def ingest_docs(self, path: str) -> str:
        """Read documentation files from a directory or single file."""
        content_parts = []
        if os.path.isfile(path):
            with open(path, "r") as f:
                content_parts.append(f"--- {os.path.basename(path)} ---\n{f.read()}")
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for fname in sorted(files):
                    if fname.endswith((".md", ".txt", ".rst")):
                        fpath = os.path.join(root, fname)
                        with open(fpath, "r") as f:
                            rel = os.path.relpath(fpath, path)
                            content_parts.append(f"--- {rel} ---\n{f.read()}")
        return "\n\n".join(content_parts)

    def ask(self, docs_content: str, question: str) -> dict:
        """Ask a question about the documentation."""
        prompt = QA_PROMPT.format(docs=docs_content, question=question)
        response = self.model.generate_content(prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0].strip()
        return json.loads(text)
