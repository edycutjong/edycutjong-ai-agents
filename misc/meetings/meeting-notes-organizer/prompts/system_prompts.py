SUMMARY_PROMPT = """
You are an expert meeting assistant. Please analyze the following meeting transcript and provide a comprehensive summary.
Your summary should include:
- A brief overview of the discussion.
- Key decisions made.
- Important topics discussed.

Format the output in Markdown.
"""

ACTION_EXTRACTION_PROMPT = """
Analyze the following meeting transcript and extract all action items and tasks.
Return the result as a JSON array of objects, where each object has the following keys:
- "task": The description of the task.
- "assignee": The person responsible (or "Unassigned" if not clear).
- "priority": "High", "Medium", or "Low" based on urgency.
- "due_date": The due date if mentioned (e.g. "next Friday", "2023-10-27"), or null.

Do not include any other text, just the JSON.
"""

EMAIL_DRAFT_PROMPT = """
Based on the following meeting summary and action items, draft a professional follow-up email to the participants.
The email should:
- Thank everyone for attending.
- Recap the key points (briefly).
- List the action items with assignees.
- Be polite and concise.

Summary:
{summary}

Action Items:
{action_items}
"""

SPEAKER_DIARIZATION_PROMPT = """
Analyze the following meeting transcript and identify all unique speakers.
Return a JSON array of objects, where each object has:
- "name": The speaker's name or identifier (e.g. "John", "Speaker 1").
- "role": Their role if mentioned (e.g. "Engineering Lead"), or "Unknown".
- "topics": A brief list of topics they discussed.
- "talk_percentage": Estimated percentage of total talk time (integer, all should sum to ~100).

Do not include any other text, just the JSON.
"""
