from langchain_core.prompts import PromptTemplate

TRIAGE_PROMPT_TEMPLATE = """
You are an intelligent email triage assistant. Your goal is to analyze the following email and provide a structured assessment.

Email Subject: {subject}
Sender: {sender}
Body:
{body}

Analyze the email and provide the following:
1. Category: Choose one from [Urgent, Work, Personal, Newsletter, Spam, Other].
2. Urgency Score: A number from 1 to 10 (10 being most urgent).
3. Summary: A brief summary of the email (max 2 sentences).
4. Action Items: A list of specific actions required.
5. Suggested Actions: Suggested next steps (e.g., "Reply confirming attendance", "Archive", "Forward to X").

{format_instructions}
"""

DRAFT_REPLY_PROMPT_TEMPLATE = """
You are an expert email drafter. Draft a reply to the following email.

Original Email Subject: {subject}
Original Email Sender: {sender}
Original Email Body:
{body}

Your Instructions:
- Tone: {tone} (e.g., professional, casual, direct)
- Context: The user wants to reply to this email.
- If specific instructions are provided, follow them: {instructions}

Draft the reply. Return ONLY the body of the reply.
"""

BRIEFING_PROMPT_TEMPLATE = """
You are an executive assistant. Create a daily briefing based on the following high-priority emails.

Emails:
{emails_text}

Provide a summary of the key items requiring attention today. Group them logically.
"""
