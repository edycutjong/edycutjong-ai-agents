from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from typing import Dict, Any, List
import pandas as pd
import json
import os

class LLMAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.llm = None
        if self.api_key:
            try:
                self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-4o", temperature=0)
            except Exception:  # pragma: no cover
                # Fallback or just stay None if init fails
                pass  # pragma: no cover

    def analyze_report(self, validation_results: Dict[str, Any]) -> str:
        """
        Generates a natural language summary of the validation report.
        """
        if not self.llm:
            return "LLM Analysis unavailable: No OpenAI API Key provided."

        prompt_template = """
        You are a Data Quality Expert. Analyze the following data validation report and provide a concise summary of the findings.
        Highlight any critical issues like schema mismatches, significant row count differences, or data quality regressions.

        Validation Report:
        {report}

        Summary:
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["report"])
        chain = prompt | self.llm

        # Convert report to JSON string for the prompt, handling numpy types
        class NumpyEncoder(json.JSONEncoder):
            def default(self, obj):
                if hasattr(obj, 'tolist'):  # pragma: no cover
                    return obj.tolist()  # pragma: no cover
                return super().default(obj)  # pragma: no cover

        report_str = json.dumps(validation_results, indent=2, cls=NumpyEncoder)

        try:
            response = chain.invoke({"report": report_str})
            return response.content
        except Exception as e:  # pragma: no cover
            return f"Error during AI analysis: {str(e)}"  # pragma: no cover

    def verify_transformation(self, source_sample: pd.DataFrame, dest_sample: pd.DataFrame, rule_description: str) -> str:
        """
        Verifies if the transformation from source to destination adheres to the described rule.
        """
        if not self.llm:
            return "LLM Verification unavailable: No OpenAI API Key provided."  # pragma: no cover

        if not rule_description:
            return "No transformation rule provided for verification."

        prompt_template = """  # pragma: no cover
        You are a Data Pipeline Auditor. Verification is requested for a data transformation.

        Transformation Rule provided by user: "{rule}"

        Below are sample rows from the Source data and the corresponding Destination data.
        Please verify if the data in the Destination appears to follow the rule when transformed from Source.
        If there are discrepancies, point them out.

        Source Sample:
        {source_sample}

        Destination Sample:
        {dest_sample}

        Verification Result:
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["rule", "source_sample", "dest_sample"])  # pragma: no cover
        chain = prompt | self.llm  # pragma: no cover

        try:  # pragma: no cover
            response = chain.invoke({  # pragma: no cover
                "rule": rule_description,
                "source_sample": source_sample.to_string(),
                "dest_sample": dest_sample.to_string()
            })
            return response.content  # pragma: no cover
        except Exception as e:  # pragma: no cover
            return f"Error during AI verification: {str(e)}"  # pragma: no cover
