import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

class SuggestionEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-4o")
        else:
            self.llm = None

    def get_suggestions(self, dependency_sizes: List[Dict[str, Any]], unused_deps: List[str]) -> List[str]:
        """
        Generates suggestions for reducing dependency bloat using LLM.
        """
        if not self.llm:
            return ["AI suggestions unavailable (OPENAI_API_KEY not found)."]

        # Filter for top heaviest dependencies to focus on
        sorted_deps = sorted(dependency_sizes, key=lambda x: x.get("size", 0), reverse=True)[:10]

        heavy_deps_list = "\n".join([f"- {d['name']}: {d.get('size', 0)/1024:.2f} KB" for d in sorted_deps])
        unused_list = ", ".join(unused_deps) if unused_deps else "None"

        prompt = ChatPromptTemplate.from_template(
            """
            You are an expert in JavaScript/TypeScript dependency optimization.
            Analyze the following dependency data and suggest specific actions to reduce bundle size.

            Heavy Dependencies:
            {heavy_deps}

            Unused Dependencies (detected by static analysis):
            {unused_deps}

            Provide a list of 3-5 concrete, actionable suggestions.
            Focus on:
            1. Lighter alternatives for heavy packages (e.g. date-fns instead of moment).
            2. Tree-shaking optimizations (e.g. import specific functions).
            3. Confirmation if unused packages can be safely removed.

            Format as a bulleted list.
            """
        )

        chain = prompt | self.llm | StrOutputParser()

        try:
            response = chain.invoke({
                "heavy_deps": heavy_deps_list,
                "unused_deps": unused_list
            })
            # Split by lines and clean up
            suggestions = [line.strip().lstrip("- ").lstrip("* ") for line in response.split("\n") if line.strip()]
            return suggestions
        except Exception as e:
            return [f"Error generating suggestions: {str(e)}"]

    def audit_tree_shaking(self, package_name: str) -> str:
        """
        Checks if a package supports tree-shaking (simulated via LLM knowledge).
        """
        if not self.llm:
            return "Tree-shaking audit unavailable."

        prompt = ChatPromptTemplate.from_template(
            "Does the npm package '{package}' support tree-shaking? Answer 'Yes' or 'No' followed by a brief explanation (1 sentence)."
        )
        chain = prompt | self.llm | StrOutputParser()
        try:
            return chain.invoke({"package": package_name})
        except Exception:
            return "Could not determine."
