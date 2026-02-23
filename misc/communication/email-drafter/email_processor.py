from langgraph.prebuilt import create_react_agent
from agent_config import get_llm, CalendarTool, SaveDraftTool

class EmailDrafter:
    def __init__(self):
        self.llm = get_llm()
        self.tools = [CalendarTool(), SaveDraftTool()]
        self.agent = self._create_agent()

    def _create_agent(self):
        system_message = (
            "You are a helpful email drafting assistant. "
            "You help users draft email responses. "
            "You can check the calendar for availability if the email asks for a meeting. "
            "If you check the calendar, mention the availability in your thought process but incorporate it into the final draft. "
            "You can save the draft to a file when the user asks or as a final step if appropriate. "
            "Always be polite and professional. "
            "The user will provide the incoming email thread."
        )
        return create_react_agent(self.llm, self.tools, prompt=system_message)

    def draft_email(self, email_content: str) -> str:
        response = self.agent.invoke({"messages": [("user", f"Draft a response to this email:\n\n{email_content}")]})
        return response["messages"][-1].content
