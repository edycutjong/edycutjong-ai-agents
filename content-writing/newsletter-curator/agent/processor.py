import json
import logging
from typing import List, Dict, Optional, Any
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from pydantic import BaseModel, Field

# Adjust import paths based on execution context
try:
    from config import MODEL_NAME_OPENAI, MODEL_NAME_GEMINI
    from prompts.templates import ANALYSIS_PROMPT
    from agent.fetcher import fetch_article_content
except ImportError:
    # Fallback for when running from a different root
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
    from config import MODEL_NAME_OPENAI, MODEL_NAME_GEMINI
    from prompts.templates import ANALYSIS_PROMPT
    from agent.fetcher import fetch_article_content

logger = logging.getLogger(__name__)

class ArticleAnalysis(BaseModel):
    relevant: bool = Field(description="Whether the article is relevant to the target topics")
    summary: str = Field(description="A concise summary of the article")
    category: str = Field(description="The most fitting category for the article")
    score: int = Field(description="Importance score from 1-10")

def get_llm(api_key: str, provider: str = "openai"):
    if provider == "openai":
        return ChatOpenAI(model=MODEL_NAME_OPENAI, api_key=api_key, temperature=0)
    elif provider == "google":
        return ChatGoogleGenerativeAI(model=MODEL_NAME_GEMINI, google_api_key=api_key, temperature=0)
    else:
        raise ValueError(f"Unknown provider: {provider}")

def process_articles(articles: List[Dict], topics: List[str], api_key: str, provider: str = "openai") -> List[Dict]:
    """
    Process a list of articles using an LLM to filter, summarize, and categorize them.
    """
    if not articles:
        return []

    try:
        llm = get_llm(api_key, provider)
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        return []

    # specific parser for robustness
    parser = JsonOutputParser(pydantic_object=ArticleAnalysis)
    chain = ANALYSIS_PROMPT | llm | parser

    processed_articles = []

    # Process each article
    # In a production app, this should be parallelized (e.g., asyncio)
    for article in articles:
        try:
            # Decide whether to fetch full content
            # If RSS summary is very short, fetch content
            content = article.get("summary", "")
            if len(content) < 200:
                 fetched_content = fetch_article_content(article["link"])
                 if fetched_content:
                     content = fetched_content[:2000] # Limit context window usage

            logger.info(f"Analyzing: {article['title']}")

            result = chain.invoke({
                "topics": ", ".join(topics),
                "title": article["title"],
                "content": content
            })

            if result.get("relevant"):
                # Merge result into article dict
                article.update(result)
                processed_articles.append(article)
            else:
                logger.info(f"Skipping irrelevant article: {article['title']}")

        except Exception as e:
            logger.error(f"Error processing article '{article['title']}': {e}")
            # Continue with other articles

    # Sort by score descending
    processed_articles.sort(key=lambda x: x.get("score", 0), reverse=True)

    return processed_articles
