# Html To Markdown Converter

Scrapes and converts HTML pages to clean, well-formatted Markdown documentation.

## Features
- Parse HTML with tag hierarchy
- Convert to clean Markdown
- Preserve headings and lists
- Handle tables and code blocks
- Extract and download images
- Clean up boilerplate/nav/footer
- Support batch URL processing
- Maintain internal link structure

## Usage
```bash
python main.py
```

## Testing
```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```
