# Documentation Quiz

Agent that reads project documentation and generates interactive quizzes to test understanding of APIs, architecture, and best practices.

## Features
- Parse README/docs into Q&A pairs
- Multiple choice & free-form questions
- Difficulty calibration
- Explanation for correct answers
- Score tracking & progress reports
- Topic-specific quiz generation
- Export as flashcards
- API reference quiz mode

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
