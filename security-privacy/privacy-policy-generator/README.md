# Privacy Policy Generator Agent

A security and privacy agent that scans your codebase for data collection patterns and generates GDPR/CCPA-compliant privacy policies using AI.

## Features

- **Code Scanning**: Automatically identifies PII (email, location, IP, etc.) and third-party services (Stripe, Google Analytics, etc.).
- **Policy Generation**: Uses LLMs (OpenAI/Gemini) to draft comprehensive privacy policies.
- **Multiple Standards**: Supports GDPR and CCPA.
- **Premium UI**: Modern Streamlit interface for easy interaction.
- **CLI Support**: Command-line interface for automation.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root of the project with your API keys:
    ```
    OPENAI_API_KEY=your_openai_api_key
    # or
    GEMINI_API_KEY=your_gemini_api_key
    ```

## Usage

### CLI

To scan a directory and generate a policy:

```bash
python main.py scan <path_to_directory>
python main.py generate <path_to_directory> --type gdpr
```

Run `python main.py --help` for all commands.

### User Interface (Streamlit)

To launch the web interface:

```bash
streamlit run app.py
```

## Testing

Run the test suite:

```bash
pytest
```
