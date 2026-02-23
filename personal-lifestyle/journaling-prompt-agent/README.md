# Journaling Prompt Agent

Your personal AI journaling companion. This application generates personalized journaling prompts based on your mood, energy level, and context, and helps you track your emotional well-being over time.

## Features

- **Personalized Prompts**: Generates prompts tailored to your current mood and energy.
- **Gratitude Journaling**: Helps you focus on the positive with guided gratitude exercises.
- **Daily Reflection**: Provides thoughtful questions for daily processing.
- **Themed Prompts**: Explore specific themes like "Nature", "Childhood", or "Dreams".
- **Mood Tracking**: Logs your mood and energy levels with every interaction.
- **Trends & Insights**: View your recent mood history directly in the CLI.
- **Markdown Export**: Export all your journal entries to a beautifully formatted Markdown file.
- **Premium CLI**: A rich, interactive terminal user interface with dark mode support.

## Tech Stack

- **Python 3.10+**
- **LangChain**: For LLM interactions and prompt management.
- **OpenAI GPT-4**: The intelligence behind the prompts.
- **Rich**: For the premium terminal UI.
- **Pydantic**: For data validation and modeling.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/journaling-prompt-agent.git
    cd journaling-prompt-agent
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory and add your OpenAI API Key:
    ```bash
    OPENAI_API_KEY=sk-your-api-key-here
    ```

## Usage

Run the application:

```bash
python main.py
```

Follow the on-screen instructions to:
1.  Check in with your mood and energy.
2.  Select a journaling activity from the main menu.
3.  Write your entry (optional) and save it.
4.  View your mood history or export your journal.

## Testing

Run the test suite to ensure everything is working correctly:

```bash
pytest tests/
```

## Structure

- `main.py`: The entry point for the CLI application.
- `agent/`: Contains the core logic (`generator.py`, `tracker.py`, `exporter.py`).
- `prompts/`: Stores the prompt templates used by the LLM.
- `data/`: Stores your local journal entries and mood history (JSON format).
- `exports/`: Destination for exported Markdown files.
- `tests/`: Unit tests for the application.
