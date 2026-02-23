from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import sys
import os

# Add parent directory to sys.path to allow importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import OPENAI_API_KEY
except ImportError:
    OPENAI_API_KEY = None

def analyze_failure(endpoint, status_code, response_time, error_message):
    """
    Analyzes a failure using an LLM to provide diagnostic context.
    """
    if not OPENAI_API_KEY:
        return "AI Diagnosis: OpenAI API Key not configured."

    try:
        # Initialize LLM with the API key
        llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o")

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a DevOps expert. Analyze the following uptime monitor failure and provide a concise diagnosis and potential troubleshooting steps."),
            ("user", "Endpoint: {endpoint}\nStatus Code: {status_code}\nResponse Time: {response_time}\nError: {error_message}")
        ])

        chain = prompt | llm

        response = chain.invoke({
            "endpoint": endpoint,
            "status_code": status_code,
            "response_time": response_time,
            "error_message": error_message
        })

        return response.content
    except Exception as e:
        return f"AI Diagnosis failed: {str(e)}"
