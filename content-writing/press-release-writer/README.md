# Press Release Writer

This is an AI-powered Press Release Writer agent.

## Features
- Generates AP-style press releases.
- Adapts tone and content for different audiences.
- Includes boilerplate and media contact info.
- Exports to PDF and Markdown.
- Premium UI with dark mode support.

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python main.py
   ```
   Or directly with Streamlit:
   ```bash
   streamlit run app.py
   ```

## Configuration
Create a `.env` file with your API keys:
```
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...
```

## Testing
Run tests with:
```bash
pytest tests/
```
