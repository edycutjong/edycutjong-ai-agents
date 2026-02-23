# Interview Prep Agent

An AI-powered interview preparation agent that generates technical interview questions based on job descriptions and tech stacks.

## Features

- **Job Description Parsing**: Extracts skills and requirements from job descriptions.
- **Question Generation**: Generates Coding, System Design, and Behavioral questions.
- **Grading & Feedback**: Provides scores and constructive feedback on your answers.
- **Progress Tracking**: Tracks your performance over time.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

## Usage

Run the agent:
```bash
python main.py
```

## Testing

Run tests:
```bash
pytest tests/
```
