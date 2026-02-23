import json
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts.system_prompts import METRIC_EXTRACTOR_SYSTEM_PROMPT
from config import Config

class MetricExtractor:
    def __init__(self, api_key: str = None, model: str = Config.DEFAULT_MODEL):
        self.api_key = api_key or Config.OPENAI_API_KEY
        self.model = model
        if self.api_key:
            self.llm = ChatOpenAI(api_key=self.api_key, model=self.model, temperature=0)
        else:
            self.llm = None

    def extract(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not logs:
            return []

        # Take a sample for analysis (e.g., first 10 logs)
        sample_logs = json.dumps(logs[:10], indent=2)

        if not self.llm:
            return self._mock_extract(logs)

        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", METRIC_EXTRACTOR_SYSTEM_PROMPT),
                ("user", "{logs}")
            ])
            chain = prompt | self.llm
            response = chain.invoke({"logs": sample_logs})

            content = response.content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]

            return json.loads(content)
        except Exception as e:
            print(f"Error extracting metrics: {e}")
            return []

    def _mock_extract(self, logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Mock metrics
        return [
            {
                "name": "http_request_duration_seconds",
                "type": "HISTOGRAM",
                "description": "Duration of HTTP requests",
                "labels": ["service", "level"],
                "source_field": "metadata.duration",
                "unit": "seconds"
            },
            {
                "name": "log_error_count",
                "type": "COUNTER",
                "description": "Count of error logs",
                "labels": ["service"],
                "source_field": "level",
                "unit": "count"
            }
        ]
