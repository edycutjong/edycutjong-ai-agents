from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
import sys

# Add parent directory to path if running directly (for testing)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from prompts.polish_prompt import POLISH_SYSTEM_PROMPT
except ImportError:
    # Fallback if running as package or different context
    POLISH_SYSTEM_PROMPT = "You are a helpful assistant. Polish this markdown."

class AIEditor:
    """
    AI-powered editor to polish Markdown content using OpenAI.
    """
    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        """
        Initialize the AI Editor.

        Args:
            api_key (str, optional): OpenAI API Key. Defaults to env var OPENAI_API_KEY.
            model (str, optional): The model to use. Defaults to "gpt-4o".
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.llm = None

        if self.api_key:
            try:
                self.llm = ChatOpenAI(openai_api_key=self.api_key, model=self.model, temperature=0.3)
            except Exception as e:
                print(f"Failed to initialize ChatOpenAI: {e}")

    def polish_content(self, content: str) -> str:
        """
        Polishes the given Markdown content.

        Args:
            content (str): The raw markdown content.

        Returns:
            str: The polished markdown content.
        """
        if not self.llm:
            print("[yellow]Warning: OpenAI API Key not configured. Skipping AI polish step.[/yellow]")
            return content

        if not content.strip():
            return content

        try:
            print("  [cyan]AI is polishing the content...[/cyan]")
            messages = [
                SystemMessage(content=POLISH_SYSTEM_PROMPT),
                HumanMessage(content=content)
            ]
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            print(f"[red]Error during AI polish: {e}[/red]")
            return content
