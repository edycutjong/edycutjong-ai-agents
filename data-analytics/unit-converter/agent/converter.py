"""Unit converter — convert between common measurement units."""
from __future__ import annotations
from dataclasses import dataclass

CONVERSIONS = {
    "length": {"m": 1, "km": 1000, "cm": 0.01, "mm": 0.001, "mi": 1609.344, "yd": 0.9144, "ft": 0.3048, "in": 0.0254},
    "weight": {"kg": 1, "g": 0.001, "mg": 0.000001, "lb": 0.453592, "oz": 0.0283495, "t": 1000},
    "temperature": {},  # special handling
    "volume": {"l": 1, "ml": 0.001, "gal": 3.78541, "qt": 0.946353, "pt": 0.473176, "cup": 0.236588, "fl_oz": 0.0295735},
    "time": {"s": 1, "ms": 0.001, "min": 60, "h": 3600, "d": 86400, "wk": 604800},
    "data": {"b": 1, "kb": 1024, "mb": 1048576, "gb": 1073741824, "tb": 1099511627776},
}

@dataclass
class ConvertResult:
    value: float = 0; from_unit: str = ""; to_unit: str = ""; result: float = 0
    category: str = ""; is_valid: bool = True; error: str = ""
    def to_dict(self) -> dict: return {"value": self.value, "from": self.from_unit, "to": self.to_unit, "result": self.result}

def find_category(unit: str) -> str:
    u = unit.lower()
    for cat, units in CONVERSIONS.items():
        if u in units: return cat
    if u in ("c", "f", "k"): return "temperature"
    return ""

def convert(value: float, from_unit: str, to_unit: str) -> ConvertResult:
    r = ConvertResult(value=value, from_unit=from_unit.lower(), to_unit=to_unit.lower())
    cat = find_category(r.from_unit)
    if not cat: r.is_valid = False; r.error = f"Unknown unit: {r.from_unit}"; return r
    r.category = cat
    if cat == "temperature":
        r.result = convert_temperature(value, r.from_unit, r.to_unit)
    else:
        units = CONVERSIONS[cat]
        if r.to_unit not in units: r.is_valid = False; r.error = f"Unknown target: {r.to_unit}"; return r
        base = value * units[r.from_unit]
        r.result = base / units[r.to_unit]
    return r

def convert_temperature(value: float, from_u: str, to_u: str) -> float:
    if from_u == "c":
        if to_u == "f": return value * 9/5 + 32
        if to_u == "k": return value + 273.15
    elif from_u == "f":
        if to_u == "c": return (value - 32) * 5/9
        if to_u == "k": return (value - 32) * 5/9 + 273.15
    elif from_u == "k":
        if to_u == "c": return value - 273.15
        if to_u == "f": return (value - 273.15) * 9/5 + 32
    return value

def list_units(category: str = "") -> dict:
    if category: return {category: list(CONVERSIONS.get(category, {}).keys())}
    return {cat: list(units.keys()) for cat, units in CONVERSIONS.items() if units}

def format_result_markdown(r: ConvertResult) -> str:
    if not r.is_valid: return f"## Unit Converter ❌\n**Error:** {r.error}"
    return f"## Unit Converter ✅\n**{r.value} {r.from_unit}** = **{r.result:.6g} {r.to_unit}** ({r.category})"
