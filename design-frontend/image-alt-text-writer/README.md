# Image Alt Text Writer

An AI-powered agent that scans HTML files for images missing alt text and generates descriptive alternatives using multimodal LLMs (OpenAI GPT-4o or Google Gemini).

## Features

- Scans HTML files for `<img>` tags missing `alt` attributes or with empty `alt` text.
- Generates descriptive alt text using AI based on the image content.
- Supports batch processing of directories.
- Generates reports in JSON and Markdown.
- Configurable to use different LLM providers.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_key
   # or
   GOOGLE_API_KEY=your_key
   ```

3. Run the scanner:
   ```bash
   python main.py path/to/your/html/files
   ```
