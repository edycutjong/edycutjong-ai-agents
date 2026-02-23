"""Calculator tool for mathematical operations."""

import math
from langchain.tools import Tool


def _safe_eval(expression: str) -> str:
    """Safely evaluate a mathematical expression.

    Args:
        expression: Math expression to evaluate.

    Returns:
        String result of the evaluation.
    """
    allowed_names = {
        "abs": abs, "round": round, "min": min, "max": max,
        "sum": sum, "pow": pow, "len": len,
        "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "pi": math.pi, "e": math.e,
    }
    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


def create_calculator_tool() -> Tool:
    """Create a calculator tool for math operations.

    Returns:
        Configured calculator tool.
    """
    return Tool(
        name="Calculator",
        func=_safe_eval,
        description=(
            "Evaluate mathematical expressions. "
            "Input should be a valid math expression like '2 + 2', 'sqrt(144)', or '15 * 23.5'. "
            "Supports basic operations, powers, sqrt, log, trig functions."
        ),
    )
