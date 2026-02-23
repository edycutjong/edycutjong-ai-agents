import json
import os
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts.system_prompts import LOG_PARSER_SYSTEM_PROMPT
from config import Config

class LogParser:
    def __init__(self, api_key: str = None, model: str = Config.DEFAULT_MODEL):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model
        if self.api_key:
            self.llm = ChatOpenAI(api_key=self.api_key, model=self.model, temperature=0)
        else:
            self.llm = None

    def parse(self, raw_logs: str) -> List[Dict[str, Any]]:
        if not raw_logs or not raw_logs.strip():
            return []

        if not self.llm:
            # Fallback for demo/testing without key
            return self._mock_parse(raw_logs)

        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", LOG_PARSER_SYSTEM_PROMPT),
                ("user", "{raw_logs}")
            ])
            chain = prompt | self.llm
            response = chain.invoke({"raw_logs": raw_logs})

            content = response.content.strip()
            # Handle potential markdown code blocks
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]

            content = content.strip()
            return json.loads(content)
        except Exception as e:
            print(f"Error parsing logs: {e}")
            # Return a basic structure on failure
            return self._mock_parse(raw_logs)

    def _mock_parse(self, raw_logs: str) -> List[Dict[str, Any]]:
        # Simple mock parser for demonstration
        logs = []
        import datetime
        for i, line in enumerate(raw_logs.split('\n')):
            if not line.strip(): continue
            level = "INFO"
            if "ERROR" in line.upper(): level = "ERROR"
            elif "WARN" in line.upper(): level = "WARN"
            elif "DEBUG" in line.upper(): level = "DEBUG"

            logs.append({
                "timestamp": datetime.datetime.now().isoformat(),
                "level": level,
                "service": "demo-service",
                "message": line.strip(),
                "metadata": {"line_number": i+1, "mock_parsed": True}
            })
        return logs
