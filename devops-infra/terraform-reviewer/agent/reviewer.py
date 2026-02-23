import json
from typing import Dict, Any, Optional, List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .parser import TerraformParser
from .security import SecurityScanner
from .cost import CostEstimator
from .rules import RulesChecker
from .drift import DriftDetector
# Assuming prompts is reachable from the path where main.py runs
try:
    from prompts.system_prompts import REVIEW_SYSTEM_PROMPT
except ImportError:
    # Fallback for relative import if run differently
    from ..prompts.system_prompts import REVIEW_SYSTEM_PROMPT

class TerraformReviewer:
    def __init__(self, api_key: str, model_name: str = "gpt-4o"):
        self.parser = TerraformParser()
        self.security = SecurityScanner()
        self.cost = CostEstimator()
        self.rules = RulesChecker()
        self.drift = DriftDetector()

        self.llm = ChatOpenAI(
            openai_api_key=api_key,
            model=model_name,
            temperature=0.2
        )
        # Create a prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", REVIEW_SYSTEM_PROMPT),
            ("user", "{input_data}")
        ])
        # Create the chain
        self.chain = self.prompt | self.llm | StrOutputParser()

    def run_review(self, tf_content: str, tf_state_content: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Runs the full review process.
        """
        # 1. Parse
        hcl_data = self.parser.parse_hcl(tf_content)
        if not hcl_data:
            return {"error": "Failed to parse Terraform content."}

        # 2. Static Analysis
        security_findings = self.security.scan(hcl_data)
        cost_estimate = self.cost.estimate(hcl_data)
        rule_findings = self.rules.check_naming(hcl_data)
        secrets_findings = self.rules.check_hardcoded_secrets(hcl_data)

        # 3. Drift Detection
        drift_report = {}
        if tf_state_content:
            drift_report = self.drift.detect(hcl_data, tf_state_content)

        # 4. Prepare Context for LLM
        analysis_context = {
            "security_findings": security_findings,
            "cost_estimate": cost_estimate,
            "naming_issues": rule_findings,
            "secrets_issues": secrets_findings,
            "drift_report": drift_report,
            "raw_hcl_structure": json.dumps(hcl_data, default=str)[:10000] # Truncate to avoid context limits if huge
        }

        # 5. Generate AI Report
        try:
            ai_report = self.chain.invoke({"input_data": json.dumps(analysis_context, indent=2)})
        except Exception as e:
            ai_report = f"Error generating AI report: {str(e)}"

        return {
            "security": security_findings,
            "cost": cost_estimate,
            "rules": rule_findings + secrets_findings,
            "drift": drift_report,
            "ai_report": ai_report
        }
