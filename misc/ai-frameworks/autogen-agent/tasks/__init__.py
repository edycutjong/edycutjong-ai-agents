"""Example task definitions for the AutoGen agent system."""

TASKS = {
    "fibonacci": {
        "description": "Generate Fibonacci sequence",
        "prompt": "Write a Python function that generates the first N numbers in the Fibonacci sequence. Test it with N=20 and print the results.",
    },
    "data_analysis": {
        "description": "Analyze CSV data",
        "prompt": "Create a Python script that generates sample sales data (date, product, quantity, price) and performs basic analysis: total revenue, best-selling product, monthly trends. Use pandas and matplotlib to create a chart.",
    },
    "web_scraper": {
        "description": "Build a web scraper",
        "prompt": "Write a Python script using requests and BeautifulSoup that scrapes the top 10 stories from Hacker News (https://news.ycombinator.com) and prints them in a formatted table.",
    },
    "api_server": {
        "description": "Create a REST API",
        "prompt": "Build a simple FastAPI server with endpoints for a todo list: GET /todos, POST /todos, DELETE /todos/{id}. Include Pydantic models for validation.",
    },
    "math_solver": {
        "description": "Solve math problems",
        "prompt": "Solve this: Find all prime numbers between 1 and 1000 that are also happy numbers. A happy number is defined by the process of repeatedly replacing it with the sum of squares of its digits until it equals 1.",
    },
}


def get_task(name: str) -> dict:
    """Get a predefined task by name.

    Args:
        name: Task identifier.

    Returns:
        Task dict with description and prompt.

    Raises:
        KeyError: If task name not found.
    """
    if name not in TASKS:
        available = ", ".join(TASKS.keys())
        raise KeyError(f"Task '{name}' not found. Available: {available}")
    return TASKS[name]


def list_tasks() -> list[str]:
    """List all available task names."""
    return list(TASKS.keys())
