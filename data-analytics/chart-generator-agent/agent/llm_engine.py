import json
import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from config import Config
from prompts.system_prompts import SYSTEM_PROMPT

class LLMEngine:
    def __init__(self):
        self.llm = self._initialize_llm()
        self.parser = JsonOutputParser()

    def _initialize_llm(self):
        if Config.OPENAI_API_KEY:
            return ChatOpenAI(api_key=Config.OPENAI_API_KEY, model=Config.MODEL_NAME)
        elif Config.GOOGLE_API_KEY:
            return ChatGoogleGenerativeAI(google_api_key=Config.GOOGLE_API_KEY, model="gemini-pro")
        else:
            print("Warning: No API key found. Using mock LLM.")
            return None

    def process_request(self, columns: dict, user_request: str):
        if not self.llm:
            # Mock response for testing/demo without API keys
            # Basic logic: if "line" in request -> line chart, else bar chart
            # pick first two columns as x and y
            col_list = list(columns.keys())
            x = col_list[0] if len(col_list) > 0 else "x"
            y = col_list[1] if len(col_list) > 1 else "y"

            tool = "js" if "interactive" in user_request.lower() or "html" in user_request.lower() else "python"
            chart_type = "line" if "line" in user_request.lower() else "bar"

            return {
                "tool": tool,
                "chart_type": chart_type,
                "x_column": x,
                "y_column": y,
                "title": f"{chart_type.capitalize()} Chart of {y} vs {x}"
            }

        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("user", "Columns: {columns}\nRequest: {request}")
        ])

        chain = prompt | self.llm | self.parser

        try:
            response = chain.invoke({"columns": str(columns), "request": user_request})
            return response
        except Exception as e:
            print(f"Error invoking LLM: {e}")
            raise e
