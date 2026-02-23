import os
import sys

# Add parent directory to path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

class LLMEngine:
    def __init__(self):
        self.use_mock = config.USE_MOCK_LLM
        self.api_key = config.OPENAI_API_KEY

        if not self.use_mock and not self.api_key:
            # Fallback to mock if no API key is present
            print("Warning: No OpenAI API Key found. Switching to Mock LLM.")
            self.use_mock = True

        if not self.use_mock:
            self.llm = ChatOpenAI(api_key=self.api_key, model="gpt-4o")
        else:
            self.llm = MockLLM()

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if self.use_mock:
            return self.llm.invoke(system_prompt, user_prompt)

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        try:
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error calling LLM: {e}")
            return f"Error: {str(e)}"

class MockLLM:
    def invoke(self, system_prompt, user_prompt):
        # Return a dummy response based on the prompt content keywords to simulate behavior
        sp = system_prompt.lower()
        up = user_prompt.lower()

        if "mongo" in sp or "mongo" in up:
            return """
            {
                "collection": "users",
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["username", "email"],
                        "properties": {
                            "username": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            },
                            "email": {
                                "bsonType": "string",
                                "description": "must be a string and is required"
                            }
                        }
                    }
                }
            }
            """
        elif "dynamo" in sp or "dynamo" in up:
             return """
            {
                "TableName": "Users",
                "KeySchema": [
                    {"AttributeName": "UserId", "KeyType": "HASH"}
                ],
                "AttributeDefinitions": [
                    {"AttributeName": "UserId", "AttributeType": "S"}
                ],
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 5,
                    "WriteCapacityUnits": 5
                }
            }
            """
        elif "strategy" in sp:
            return "RECOMMENDATION: EMBED\nReason: The data is often accessed together."

        else:
            return "Mock response for testing."
