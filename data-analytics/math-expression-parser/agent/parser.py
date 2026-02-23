"""Math expression parser — safely evaluate math expressions with variables."""
from __future__ import annotations
import re, math, operator
from dataclasses import dataclass

SAFE_NAMES = {
    "abs": abs, "round": round, "min": min, "max": max,
    "sqrt": math.sqrt, "log": math.log, "log2": math.log2, "log10": math.log10,
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan, "atan2": math.atan2,
    "floor": math.floor, "ceil": math.ceil,
    "pi": math.pi, "e": math.e, "tau": math.tau, "inf": math.inf,
    "pow": math.pow, "factorial": math.factorial,
}

@dataclass
class MathResult:
    expression: str = ""; result: float = 0; is_valid: bool = True
    error: str = ""; steps: list[str] = None
    def __post_init__(self):
        if self.steps is None: self.steps = []
    def to_dict(self) -> dict: return {"expression": self.expression, "result": self.result, "is_valid": self.is_valid}

def _safe_eval(expr: str, variables: dict = None) -> float:
    allowed = dict(SAFE_NAMES)
    if variables: allowed.update(variables)
    # Block anything unsafe
    if re.search(r'__|\bimport\b|\bexec\b|\beval\b|\bopen\b|\bos\b|\bsys\b', expr):
        raise ValueError("Unsafe expression")
    return eval(expr, {"__builtins__": {}}, allowed)  # noqa: S307

def evaluate(expression: str, variables: dict = None) -> MathResult:
    r = MathResult(expression=expression)
    try:
        expr = expression.strip().replace("^", "**")
        r.result = float(_safe_eval(expr, variables))
    except ZeroDivisionError: r.is_valid = False; r.error = "Division by zero"
    except Exception as e: r.is_valid = False; r.error = str(e)
    return r

def evaluate_batch(expressions: list[str], variables: dict = None) -> list[MathResult]:
    return [evaluate(e, variables) for e in expressions]

def simplify_fraction(numerator: int, denominator: int) -> tuple[int, int]:
    g = math.gcd(abs(numerator), abs(denominator))
    return numerator // g, denominator // g

def format_result_markdown(r: MathResult) -> str:
    if not r.is_valid: return f"## Math Parser ❌\n`{r.expression}` → **Error:** {r.error}"
    res = int(r.result) if r.result == int(r.result) else r.result
    return f"## Math Parser ✅\n`{r.expression}` = **{res}**"
