# AI Workout Planner

An intelligent CLI tool that generates personalized workout plans based on your fitness goals, level, and available equipment.

## Features

- **Personalized Plans**: Generates 4-week workout schedules tailored to you.
- **Detailed Sessions**: Includes warm-ups, exercises (sets/reps), cool-downs, and calorie estimates.
- **Flexible Inputs**: Supports various fitness goals, equipment (or lack thereof), and schedule constraints.
- **Premium CLI**: Interactive and visually appealing terminal interface using `rich`.
- **Export Options**: Save your plan as Markdown or PDF.

## Setup

1.  **Navigate to the project directory**:
    ```bash
    cd apps/agents/personal-lifestyle/workout-planner
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment**:
    Create a `.env` file in this directory with your OpenAI API key:
    ```
    OPENAI_API_KEY=your_api_key_here
    ```

## Usage

Run the application:

```bash
python main.py
```

Follow the on-screen prompts to input your details. The AI will generate a plan, display a preview, and offer to save it.

## Testing

Run the tests using `pytest`:

```bash
pytest tests/
```
