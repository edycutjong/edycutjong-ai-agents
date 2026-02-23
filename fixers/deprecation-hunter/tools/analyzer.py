import os
import ast
from dataclasses import dataclass
from typing import List, Optional, Dict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

@dataclass
class DeprecationFinding:
    filepath: str
    line_number: int
    code: str
    message: str
    suggestion: Optional[str] = None
    library: Optional[str] = None
    severity: str = "warning" # warning, error

class DeprecationAnalyzer:
    def __init__(self, use_llm: bool = True):
        self.use_llm = use_llm and bool(os.environ.get("OPENAI_API_KEY"))
        if self.use_llm:
            self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        else:
            self.llm = None

    def analyze_file(self, filepath: str, dependencies: Dict[str, str]) -> List[DeprecationFinding]:
        findings = []

        try:
            with open(filepath, "r") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return []

        # 1. AST Analysis (Heuristics)
        findings.extend(self._analyze_ast(filepath, content))

        # 2. LLM Analysis (if enabled)
        if self.use_llm:
            findings.extend(self._analyze_llm(filepath, content, dependencies))

        return findings

    def _analyze_ast(self, filepath: str, content: str) -> List[DeprecationFinding]:
        findings = []
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        for node in ast.walk(tree):
            # Check for datetime.utcnow()
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    # Check for datetime.utcnow()
                    if node.func.attr == 'utcnow':
                        # This is a weak check, ideally we check if the object is datetime
                        findings.append(DeprecationFinding(
                            filepath=filepath,
                            line_number=node.lineno,
                            code="datetime.utcnow()",
                            message="datetime.utcnow() is deprecated.",
                            suggestion="datetime.now(datetime.timezone.utc)",
                            library="datetime"
                        ))

                    # Check for pandas.append
                    if node.func.attr == 'append':
                        findings.append(DeprecationFinding(
                            filepath=filepath,
                            line_number=node.lineno,
                            code=".append()",
                            message="Pandas .append() is deprecated.",
                            suggestion="pandas.concat()",
                            library="pandas"
                        ))

                    # Check for numpy types
                    if node.func.attr in ['float', 'int', 'bool', 'object', 'str']:
                         # Very weak check again, but serves as a placeholder for detailed AST analysis
                        pass

        return findings

    def _analyze_llm(self, filepath: str, content: str, dependencies: Dict[str, str]) -> List[DeprecationFinding]:
        # To avoid token limits, we might want to split the file or only analyze parts.
        # For this implementation, we'll try to analyze the whole file if it's small,
        # or just skip if it's too large for a simple demo.
        if len(content) > 10000:
            return [] # Skip large files to save tokens/time in this demo

        prompt = ChatPromptTemplate.from_template(
            """
            Analyze the following Python code for deprecated library usage.
            Dependencies: {dependencies}

            Code:
            ```python
            {code}
            ```

            Return a JSON object with a list of findings. Each finding should have:
            - line_number: int
            - code: str (the deprecated code snippet)
            - message: str (why it is deprecated)
            - suggestion: str (how to fix it)
            - library: str (the library name)
            - severity: str (warning or error)

            If no deprecations are found, return an empty list in the JSON: {{ "findings": [] }}
            """
        )

        chain = prompt | self.llm | JsonOutputParser()

        try:
            result = chain.invoke({"code": content, "dependencies": ", ".join(dependencies.keys())})
            findings = []
            if "findings" in result:
                for f in result["findings"]:
                    findings.append(DeprecationFinding(
                        filepath=filepath,
                        line_number=f.get("line_number", 0),
                        code=f.get("code", ""),
                        message=f.get("message", ""),
                        suggestion=f.get("suggestion", ""),
                        library=f.get("library", ""),
                        severity=f.get("severity", "warning")
                    ))
            return findings
        except Exception as e:
            # print(f"LLM Analysis failed for {filepath}: {e}")
            return []
