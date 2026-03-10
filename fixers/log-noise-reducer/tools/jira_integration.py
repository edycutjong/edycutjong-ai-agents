import random
import time

def create_jira_ticket(title: str, description: str, project_key: str = "LOG") -> str:
    """
    Mock function to create a Jira ticket.
    Returns a ticket ID.
    """
    # Simulate network delay
    time.sleep(0.5)

    ticket_id = f"{project_key}-{random.randint(1000, 9999)}"
    # In a real app, this would verify credentials and call the Jira API
    return ticket_id
