from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from pydantic import BaseModel, Field
from simpleeval import simple_eval

try:
    search_run = DuckDuckGoSearchRun()
except Exception:
    search_run = None

class SearchInput(BaseModel):
    query: str = Field(description="The search query to find information.")

@tool("research_tool", args_schema=SearchInput)
def research_tool(query: str) -> str:
    """Use this tool to research attractions, local culture, and general travel information."""
    if search_run:
        try:
            return search_run.invoke(query)
        except Exception as e:
            return f"Error performing search: {e}"
    return "Search tool is not available in this environment. Please rely on your internal knowledge."

@tool("calculator_tool")
def calculator_tool(expression: str) -> str:
    """Useful for making calculations. Input should be a mathematical expression string like '200 * 5'."""
    try:
        # Use simple_eval for safe mathematical evaluation
        return str(simple_eval(expression))
    except Exception as e:
        return f"Error calculating: {e}"

@tool("accommodation_tool", args_schema=SearchInput)
def accommodation_tool(query: str) -> str:
    """Use this tool to find hotels, hostels, and other accommodation options."""
    if search_run:
        try:
            return search_run.invoke(f"accommodation hotels {query}")
        except Exception as e:
            return f"Error searching for accommodation: {e}"
    return "Accommodation search is not available. Suggest generic options based on destination."

@tool("dining_tool", args_schema=SearchInput)
def dining_tool(query: str) -> str:
    """Use this tool to find restaurants, cafes, and dining experiences."""
    if search_run:
        try:
            return search_run.invoke(f"restaurants dining {query}")
        except Exception as e:
            return f"Error searching for dining: {e}"
    return "Dining search is not available. Suggest popular local cuisines."
