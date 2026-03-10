"""Calculator tool for mathematical operations."""

import ast
import operator
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

    # Operators mapping
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval_expr(node):
        if isinstance(node, ast.Constant):  # python 3.8+
            return node.value
        elif isinstance(node, (ast.Num, ast.Str, ast.Bytes)):  # python < 3.8
            return node.n if isinstance(node, ast.Num) else node.s
        elif isinstance(node, ast.BinOp):
            op = type(node.op)
            if op not in operators:
                raise ValueError(f"Unsupported binary operation: {op}")
            return operators[op](_eval_expr(node.left), _eval_expr(node.right))
        elif isinstance(node, ast.UnaryOp):
            op = type(node.op)
            if op not in operators:
                raise ValueError(f"Unsupported unary operation: {op}")
            return operators[op](_eval_expr(node.operand))
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only direct function calls allowed")
            if node.func.id not in allowed_names:
                raise ValueError(f"Function '{node.func.id}' not allowed")
            args = [_eval_expr(arg) for arg in node.args]
            return allowed_names[node.func.id](*args)
        elif isinstance(node, ast.Name):
            if node.id in allowed_names:
                return allowed_names[node.id]
            raise ValueError(f"Name '{node.id}' not allowed")
        elif isinstance(node, (ast.List, ast.Tuple)):
            return [_eval_expr(elt) for elt in node.elts]
        else:
            raise ValueError(f"Unsupported expression type: {type(node)}")

    try:
        expression = expression.strip()
        if not expression:
            return ""
        # Parse into AST
        tree = ast.parse(expression, mode='eval')
        # Evaluate
        result = _eval_expr(tree.body)
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
