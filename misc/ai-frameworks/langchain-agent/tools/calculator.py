"""Calculator tool for mathematical operations."""

import ast
import operator
import math
from langchain_core.tools import Tool


def _evaluate_ast(node, allowed_names):
    """Recursively evaluate an AST node safely."""
    bin_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.BitXor: operator.xor,
        ast.BitOr: operator.or_,
        ast.BitAnd: operator.and_,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
    }

    un_ops = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
        ast.Not: operator.not_,
        ast.Invert: operator.invert,
    }

    if isinstance(node, ast.Expression):
        return _evaluate_ast(node.body, allowed_names)
    elif hasattr(ast, 'Constant') and isinstance(node, ast.Constant):
        return node.value
    elif isinstance(node, ast.Num):  # For Python < 3.8
        return node.n
    elif isinstance(node, ast.Str):  # For Python < 3.8
        return node.s
    elif isinstance(node, ast.Name):
        if node.id in allowed_names:
            return allowed_names[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")
    elif isinstance(node, ast.BinOp):
        left = _evaluate_ast(node.left, allowed_names)
        right = _evaluate_ast(node.right, allowed_names)
        op = type(node.op)
        if op not in bin_ops:
            raise ValueError(f"Unsupported binary operator: {op.__name__}")
        return bin_ops[op](left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _evaluate_ast(node.operand, allowed_names)
        op = type(node.op)
        if op not in un_ops:
            raise ValueError(f"Unsupported unary operator: {op.__name__}")
        return un_ops[op](operand)
    elif isinstance(node, ast.Call):
        func = _evaluate_ast(node.func, allowed_names)
        args = [_evaluate_ast(arg, allowed_names) for arg in node.args]
        if node.keywords:
            raise ValueError("Keyword arguments are not supported")
        return func(*args)
    elif isinstance(node, ast.List):
        return [_evaluate_ast(elt, allowed_names) for elt in node.elts]
    elif isinstance(node, ast.Tuple):
        return tuple(_evaluate_ast(elt, allowed_names) for elt in node.elts)
    elif isinstance(node, ast.Attribute):
        raise ValueError("Attribute access is explicitly blocked")
    else:
        raise ValueError(f"Unsupported AST node: {type(node).__name__}")


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
        tree = ast.parse(expression, mode='eval')
        result = _evaluate_ast(tree, allowed_names)
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
