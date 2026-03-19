"""Prompts for test generation."""

SYSTEM_PROMPT = """You are an expert test engineer.  # pragma: no cover
Given source code, generate comprehensive, well-structured test suites.
Follow best practices for the target framework (pytest, Jest, unittest).
Include descriptive test names, docstrings, and edge cases."""

GENERATE_PROMPT = """Generate {framework} tests for the following code:  # pragma: no cover

```
{source_code}
```

Requirements:
- Test all public functions and methods
- Include at least one positive and one negative test per function
- Use descriptive test names
- Add docstrings to each test
{edge_case_instruction}
{mock_instruction}

Output only the test code, ready to run."""

EDGE_CASE_INSTRUCTION = "- Include edge case tests (empty input, None, boundary values, large input)"  # pragma: no cover
MOCK_INSTRUCTION = "- Generate mock/stub code for external dependencies"  # pragma: no cover
