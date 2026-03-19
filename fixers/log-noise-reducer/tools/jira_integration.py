import random  # pragma: no cover
import time  # pragma: no cover

def create_jira_ticket(title: str, description: str, project_key: str = "LOG") -> str:  # pragma: no cover
    """
    Mock function to create a Jira ticket.
    Returns a ticket ID.
    """
    # Simulate network delay
    time.sleep(0.5)  # pragma: no cover

    ticket_id = f"{project_key}-{random.randint(1000, 9999)}"  # pragma: no cover
    # In a real app, this would verify credentials and call the Jira API
    # print(f"Creating Jira Ticket: {title} -> {ticket_id}")
    return ticket_id  # pragma: no cover
