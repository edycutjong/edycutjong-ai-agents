import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts.system_prompts import GRAFANA_GENERATOR_SYSTEM_PROMPT
from config import Config

class GrafanaGenerator:
    def __init__(self, api_key: str = None, model: str = Config.DEFAULT_MODEL):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model
        if self.api_key:
            self.llm = ChatOpenAI(api_key=self.api_key, model=self.model, temperature=0)
        else:
            self.llm = None

    def generate(self, metrics: List[Dict[str, Any]], service_name: str) -> str:
        if not metrics:
            return ""

        if not self.llm:
            return self._mock_generate(metrics, service_name)

        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", GRAFANA_GENERATOR_SYSTEM_PROMPT),
                ("user", "Metrics: {metrics}\nService: {service_name}")
            ])
            chain = prompt | self.llm
            response = chain.invoke({
                "metrics": json.dumps(metrics, indent=2),
                "service_name": service_name
            })

            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]

            return content
        except Exception as e:
            print(f"Error generating Grafana dashboard: {e}")
            return ""

    def _mock_generate(self, metrics: List[Dict[str, Any]], service_name: str) -> str:
        # Mock Grafana Dashboard JSON
        dashboard = {
            "title": f"{service_name} Dashboard",
            "panels": [
                {
                    "title": "Error Rate",
                    "type": "graph",
                    "targets": [{"expr": f"rate(log_error_count{{service=\"{service_name}\"}}[5m])"}]
                }
            ]
        }
        return json.dumps(dashboard, indent=2)
