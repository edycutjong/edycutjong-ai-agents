import os
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage

from prompts.analysis_prompt import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from config import Config

class FinOpsAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.api_key = Config.OPENAI_API_KEY
        self.model_name = model_name
        self.is_mock = not bool(self.api_key)

    def generate_report(self,
                        total_cost: float,
                        currency: str,
                        top_services: pd.DataFrame,
                        waste_df: pd.DataFrame,
                        right_sizing_df: pd.DataFrame,
                        potential_savings: float) -> str:

        # Prepare data strings
        top_services_str = top_services.head(5).to_markdown(index=False)

        if waste_df.empty:
            waste_str = "No significant waste identified."
        else:
            # Summarize waste by reason
            waste_summary = waste_df.groupby('Reason')['Cost'].sum().reset_index()
            waste_str = waste_summary.to_markdown(index=False)

        if right_sizing_df.empty:
            right_sizing_str = "No right-sizing opportunities identified."
        else:
            right_sizing_str = right_sizing_df.to_markdown(index=False)

        user_content = USER_PROMPT_TEMPLATE.format(
            currency=currency,
            total_cost=total_cost,
            top_services=top_services_str,
            waste_summary=waste_str,
            right_sizing_summary=right_sizing_str,
            potential_savings=potential_savings
        )

        if self.is_mock:
            return self._mock_response(user_content)

        try:
            llm = ChatOpenAI(model=self.model_name, temperature=0.7, api_key=self.api_key)
            prompt = ChatPromptTemplate.from_messages([
                ("system", SYSTEM_PROMPT),
                ("user", "{input}")
            ])
            chain = prompt | llm | StrOutputParser()
            return chain.invoke({"input": user_content})
        except Exception as e:
            return f"Error generating report: {str(e)}\n\n(Falling back to mock mode...)\n\n" + self._mock_response(user_content)

    def _mock_response(self, context: str) -> str:
        return f"""
# Cost Optimization Report (Mock)

## Executive Summary
This is a simulated AI analysis because no OpenAI API Key was detected.
Based on the data provided:

{context}

## Recommendations
1. **Remove Unused Resources:** Please review the identified waste (e.g., unattached IPs or old snapshots).
2. **Right-Size Instances:** Consider downsizing underutilized instances.
3. **Monitor Trends:** Keep an eye on the daily cost trends to spot anomalies early.

*To enable real AI analysis, please set your OPENAI_API_KEY in the .env file.*
"""
