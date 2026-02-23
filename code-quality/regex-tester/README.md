# Regex Tester 🔍

Test, validate, explain, and explore regex patterns. Includes a library of 25 common patterns.

## Features

- **Test Patterns** — Match regex against text with full match details
- **Validate** — Check if a pattern is valid without testing
- **Explain** — Break down regex into human-readable components
- **Pattern Library** — 25 pre-built patterns (email, URL, IPv4, UUID, etc.)
- **Extract** — Use named patterns to extract data from text
- **Batch Testing** — Test multiple patterns at once
- **Flags** — Support for i (ignorecase), m (multiline), s (dotall), x (verbose)

## Quick Start

```bash
pip install -r requirements.txt

# Test a pattern
python main.py test "\d+" "abc 123 def 456"
python main.py test "(\w+)@(\w+\.\w+)" "user@example.com" --json

# Validate
python main.py validate "(?P<name>\w+)"

# Explain
python main.py explain "\d{3}-\d{4}"

# Browse pattern library
python main.py library
python main.py library email

# Extract using common patterns
python main.py extract email "Contact user@example.com"
python main.py extract url --file webpage.txt
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
regex-tester/
├── main.py              # CLI with 5 subcommands
├── config.py
├── requirements.txt
├── agent/
│   └── tester.py        # Regex engine + 25 common patterns
└── tests/
    └── test_tester.py   # 25 tests
```
