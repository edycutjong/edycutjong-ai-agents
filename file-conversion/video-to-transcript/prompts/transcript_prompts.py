SUMMARY_TEMPLATE = """You are an expert content analyzer. Given the following transcript, please provide a comprehensive summary of the key points, main arguments, and conclusions.

Transcript:
{transcript}

Summary:
"""

CHAPTERS_TEMPLATE = """You are an expert video editor assistant. Given the following transcript, please identify the major topic shifts and create a list of chapter markers.
Each chapter should have a Title and a Brief Description.

Transcript:
{transcript}

Please format the output as a list of chapters.
Example:
1. Introduction - Overview of the topic
2. Main Argument - Detailed explanation of the core concept
3. Conclusion - Final thoughts and summary

Chapters:
"""
