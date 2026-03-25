#!/usr/bin/env python3
"""LLM Prompt Tester — core logic."""
import json
from typing import Any

def test(input_data: str = "", **kwargs) -> dict:
    """Execute test command."""
    result = {"command": "test", "status": "success", "input": input_data, "data": {}}
    if not input_data:
        result["status"] = "error"
        result["error"] = "No input provided"
        return result
    result["data"] = {"output": f"test result for {input_data}", "metrics": {}, "timestamp": "2026-01-01T00:00:00Z"}
    return result

def compare(input_data: str = "", **kwargs) -> dict:
    """Execute compare command."""
    result = {"command": "compare", "status": "success", "input": input_data, "data": {}}
    if not input_data:
        result["status"] = "error"
        result["error"] = "No input provided"
        return result
    result["data"] = {"output": f"compare result for {input_data}", "metrics": {}, "timestamp": "2026-01-01T00:00:00Z"}
    return result

def best(input_data: str = "", **kwargs) -> dict:
    """Execute best command."""
    result = {"command": "best", "status": "success", "input": input_data, "data": {}}
    if not input_data:
        result["status"] = "error"
        result["error"] = "No input provided"
        return result
    result["data"] = {"output": f"best result for {input_data}", "metrics": {}, "timestamp": "2026-01-01T00:00:00Z"}
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
