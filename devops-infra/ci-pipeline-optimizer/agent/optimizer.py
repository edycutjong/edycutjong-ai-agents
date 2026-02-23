import json
from langchain_core.output_parsers import StrOutputParser

try:
    from prompts.prompts import optimization_prompt
except ImportError:
    # Fallback for when running tests or from a different context where the path is different
    import sys
    import os
    # Add the project root to sys.path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from prompts.prompts import optimization_prompt

class CIOptimizer:
    def __init__(self, llm):
        self.llm = llm
        if self.llm:
            self.optimization_chain = optimization_prompt | self.llm | StrOutputParser()
        else:
            self.optimization_chain = None

    def optimize(self, config_content: str, analysis_result: dict) -> str:
        """
        Generates an optimized CI/CD configuration based on the analysis.
        """
        if not self.optimization_chain:
             return "# Optimization failed: LLM not initialized."

        try:
            # Check if analysis_result is a dict or string, handle accordingly
            if isinstance(analysis_result, dict):
                analysis_str = json.dumps(analysis_result, indent=2)
            else:
                analysis_str = str(analysis_result)

            optimized_yaml = self.optimization_chain.invoke({
                "config_content": config_content,
                "analysis": analysis_str
            })

            # Clean up potential markdown formatting if the LLM adds it
            optimized_yaml = str(optimized_yaml).strip()
            if optimized_yaml.startswith("```yaml"):
                optimized_yaml = optimized_yaml[7:]
            elif optimized_yaml.startswith("```"):
                 optimized_yaml = optimized_yaml[3:]

            if optimized_yaml.endswith("```"):
                optimized_yaml = optimized_yaml[:-3]

            return optimized_yaml.strip()
        except Exception as e:
            return f"# Optimization failed: {e}"
