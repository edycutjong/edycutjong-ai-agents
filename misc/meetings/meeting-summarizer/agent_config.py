import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """Returns a configured ChatOpenAI instance."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return ChatOpenAI(temperature=0, model="gpt-4o-mini", api_key=api_key)

def get_summary_chain():
    """Returns a chain for summarizing key decisions."""
    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert meeting summarizer.
        Analyze the following transcript and provide a concise summary of the key decisions made.
        Format the output as a bulleted list of decisions.

        Transcript:
        {transcript}

        Key Decisions:
        """
    )
    return prompt | get_llm() | StrOutputParser()

def get_action_items_chain():
    """Returns a chain for extracting action items."""
    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert project manager.
        Analyze the following transcript and extract all action items.
        For each action item, specify the assignee (if mentioned) and the task.
        Format the output as a markdown table with columns: Assignee, Task.
        If no assignee is clear, use 'Unknown'.

        Transcript:
        {transcript}

        Action Items:
        """
    )
    return prompt | get_llm() | StrOutputParser()

def get_email_chain():
    """Returns a chain for drafting a follow-up email."""
    prompt = ChatPromptTemplate.from_template(
        """
        You are a professional assistant.
        Based on the following transcript, draft a follow-up email to the participants.
        The email should include a brief summary of the meeting and the action items.
        Keep the tone professional and courteous.

        Transcript:
        {transcript}

        Draft Email:
        """
    )
    return prompt | get_llm() | StrOutputParser()

def get_sentiment_chain():
    """Returns a chain for analyzing sentiment."""
    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert in sentiment analysis.
        Analyze the overall sentiment of the following meeting transcript.
        Provide a brief analysis of the mood, tone, and any potential conflicts or positive highlights.

        Transcript:
        {transcript}

        Sentiment Analysis:
        """
    )
    return prompt | get_llm() | StrOutputParser()
