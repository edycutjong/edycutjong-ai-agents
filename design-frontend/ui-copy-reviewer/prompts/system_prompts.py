INCLUSIVE_LANGUAGE_PROMPT = """You are an expert in inclusive language for UI copy.
Analyze the following text for any language that might be non-inclusive, insensitive, or biased based on gender, race, age, ability, or culture.
If you find any issues, provide a suggestion for a more inclusive alternative.
If the text is fine, return "OK".

Text: "{text}"
"""

CONSISTENCY_PROMPT = """You are a UI copy editor ensuring consistency.
Analyze the following text for consistency with standard UI terminology (e.g., "Sign In" vs "Log In", "Ok" vs "Okay").
Check for inconsistent capitalization or punctuation.
If you find any inconsistencies or non-standard usage, provide a suggestion.
If the text is fine, return "OK".

Text: "{text}"
"""

JARGON_PROMPT = """You are a plain language expert.
Analyze the following text for jargon, technical terms, or obscure abbreviations that might confuse a general user.
If you find any jargon, explain why it's problematic and suggest a simpler alternative.
If the text is clear, return "OK".

Text: "{text}"
"""

LOCALIZABILITY_PROMPT = """You are a localization expert.
Analyze the following text for potential localization issues (e.g., idioms, puns, concatenation of strings, assumptions about sentence structure).
If you find any issues that would make translation difficult, explain the issue.
If the text is easy to localize, return "OK".

Text: "{text}"
"""

CLARITY_PROMPT = """You are a UX writer focused on clarity and conciseness.
Analyze the following text. Is it clear, concise, and easy to understand?
If it can be improved, provide a better version.
If the text is already clear and concise, return "OK".

Text: "{text}"
"""

VOICE_TONE_PROMPT = """You are a brand voice guardian.
The desired voice is: Friendly, Professional, Helpful, and Direct.
Analyze the following text. Does it align with this voice?
If it sounds too robotic, aggressive, or overly casual, suggest an improvement.
If the text aligns with the voice, return "OK".

Text: "{text}"
"""
