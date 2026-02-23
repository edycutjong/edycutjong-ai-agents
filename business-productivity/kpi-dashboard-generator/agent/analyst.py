from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os

class KPIAnalyst:
    def __init__(self, api_key=None, model="gpt-4o"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.llm = ChatOpenAI(temperature=0.7, model_name=model, openai_api_key=self.api_key)
        else:
            self.llm = None

    def analyze_dashboard(self, kpi_data_summary):
        """
        Generates an executive summary based on the KPI data summary.
        kpi_data_summary: A dictionary or string description of current KPIs and their status.
        """
        if not self.llm:
            return "AI Analyst not configured (missing OpenAI API Key)."

        system_prompt = """
        You are an expert Business Intelligence Analyst.
        Your task is to review the provided KPI data summary and generate a concise executive summary.
        Highlight key successes (metrics meeting targets) and areas for concern (metrics missing targets).
        Provide actionable insights if possible based on the trends.
        Keep the tone professional and data-driven.
        """

        user_prompt = f"""
        Here is the current KPI Dashboard status:
        {kpi_data_summary}

        Please provide an executive summary.
        """

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"Error generating analysis: {e}"
