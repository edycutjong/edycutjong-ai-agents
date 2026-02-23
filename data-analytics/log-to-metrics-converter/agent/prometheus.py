import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts.system_prompts import PROMETHEUS_GENERATOR_SYSTEM_PROMPT
from config import Config

class PrometheusGenerator:
    def __init__(self, api_key: str = None, model: str = Config.DEFAULT_MODEL):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model
        if self.api_key:
            self.llm = ChatOpenAI(api_key=self.api_key, model=self.model, temperature=0)
        else:
            self.llm = None

    def generate(self, metrics: List[Dict[str, Any]]) -> str:
        if not metrics:
            return ""

        if not self.llm:
            return self._mock_generate(metrics)

        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", PROMETHEUS_GENERATOR_SYSTEM_PROMPT),
                ("user", "{metrics}")
            ])
            chain = prompt | self.llm
            response = chain.invoke({"metrics": json.dumps(metrics, indent=2)})

            return response.content.strip()
        except Exception as e:
            print(f"Error generating Prometheus config: {e}")
            return ""

    def _mock_generate(self, metrics: List[Dict[str, Any]]) -> str:
        # Mock Prometheus config
        return """
---CONFIG---
scrape_configs:
  - job_name: 'log_metrics'
    static_configs:
      - targets: ['localhost:9090']

---RULES---
groups:
  - name: log_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(log_error_count[5m]) > 0.1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
"""
