#!/usr/bin/env python3
"""Meal Prep Planner — core logic."""
import json
from typing import Any

def plan(input_data: str = "", **kwargs) -> dict:
    """Execute plan command."""
    result = {"command": "plan", "status": "success", "input": input_data, "data": {}}
    if not input_data:
        result["status"] = "error"
        result["error"] = "No input provided"
        return result
    result["data"] = {"output": f"plan result for {input_data}", "metrics": {}, "timestamp": "2026-01-01T00:00:00Z"}
    return result

def grocery(input_data: str = "", **kwargs) -> dict:
    """Execute grocery command."""
    result = {"command": "grocery", "status": "success", "input": input_data, "data": {}}
    if not input_data:
        result["status"] = "error"
        result["error"] = "No input provided"
        return result
    result["data"] = {"output": f"grocery result for {input_data}", "metrics": {}, "timestamp": "2026-01-01T00:00:00Z"}
    return result

def nutrition(input_data: str = "", **kwargs) -> dict:
    """Execute nutrition command."""
    result = {"command": "nutrition", "status": "success", "input": input_data, "data": {}}
    if not input_data:
        result["status"] = "error"
        result["error"] = "No input provided"
        return result
    result["data"] = {"output": f"nutrition result for {input_data}", "metrics": {}, "timestamp": "2026-01-01T00:00:00Z"}
    return result

def format_output(result: dict, fmt: str = "text") -> str:
    """Format output as text or JSON."""
    if fmt == "json":
        return json.dumps(result, indent=2)
    if result["status"] == "error":
        return f"Error: {result.get('error', 'Unknown error')}"
    lines = [f"Command: {result['command']}", f"Status: {result['status']}"]
    if result.get("data"):
        for k, v in result["data"].items():
            lines.append(f"  {k}: {v}")
    return "\n".join(lines)
