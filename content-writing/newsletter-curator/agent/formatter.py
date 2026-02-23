from datetime import datetime
from collections import defaultdict
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def format_newsletter_markdown(articles: List[Dict], title: str = "Tech Newsletter", date: str = None) -> str:
    """
    Format the processed articles into a Markdown newsletter.

    Args:
        articles (List[Dict]): List of processed articles.
        title (str): Title of the newsletter.
        date (str): Date string (optional).

    Returns:
        str: Markdown string.
    """
    if date is None:
        date = datetime.now().strftime("%B %d, %Y")

    md = f"# {title}\n"
    md += f"**{date}**\n\n"
    md += "---\n\n"

    if not articles:
        md += "*No articles found matching your criteria.*\n"
        return md

    # Group by category
    categories = defaultdict(list)
    for article in articles:
        cat = article.get("category", "Uncategorized")
        categories[cat].append(article)

    # Sort categories alphabetically or by importance? Alphabetical for now.
    sorted_categories = sorted(categories.keys())

    for cat in sorted_categories:
        items = categories[cat]
        # Sort items by score descending within category
        items.sort(key=lambda x: x.get("score", 0), reverse=True)

        md += f"## {cat}\n\n"
        for item in items:
            score = item.get("score", 0)
            # visual score indicator
            score_str = f"score: {score}/10"

            md += f"### [{item['title']}]({item['link']})\n"
            md += f"**{score_str}**\n\n"
            md += f"{item['summary']}\n\n"

    md += "---\n*Curated by Newsletter Curator Agent*\n"
    return md

def format_newsletter_html(articles: List[Dict], title: str = "Tech Newsletter", date: str = None) -> str:
    """
    Format the processed articles into a simple HTML newsletter.
    """
    if date is None:
        date = datetime.now().strftime("%B %d, %Y")

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: sans-serif; line-height: 1.6; color: #333; max_width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            h2 {{ color: #e67e22; margin-top: 30px; border-bottom: 1px solid #eee; }}
            h3 {{ margin-bottom: 5px; }}
            a {{ color: #3498db; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
            .meta {{ font-size: 0.9em; color: #7f8c8d; margin-bottom: 10px; }}
            .summary {{ margin-bottom: 20px; }}
            .footer {{ margin-top: 50px; font-size: 0.8em; color: #95a5a6; text-align: center; border-top: 1px solid #eee; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <div class="meta">{date}</div>
    """

    if not articles:
        html += "<p><em>No articles found matching your criteria.</em></p>"
    else:
        categories = defaultdict(list)
        for article in articles:
            cat = article.get("category", "Uncategorized")
            categories[cat].append(article)

        sorted_categories = sorted(categories.keys())

        for cat in sorted_categories:
            items = categories[cat]
            items.sort(key=lambda x: x.get("score", 0), reverse=True)

            html += f"<h2>{cat}</h2>"
            for item in items:
                score = item.get("score", 0)
                html += f"""
                <div class="article">
                    <h3><a href="{item['link']}">{item['title']}</a></h3>
                    <div class="meta">Importance Score: {score}/10</div>
                    <div class="summary">{item['summary']}</div>
                </div>
                """

    html += """
        <div class="footer">Curated by Newsletter Curator Agent</div>
    </body>
    </html>
    """
    return html
