from agent.formatter import format_newsletter_markdown, format_newsletter_html

def test_format_markdown_with_articles():
    articles = [
        {
            "title": "AI Breakthrough",
            "link": "http://ai.com",
            "summary": "AI is now sentient.",
            "category": "Artificial Intelligence",
            "score": 10,
            "relevant": True
        },
        {
            "title": "New iPhone",
            "link": "http://apple.com",
            "summary": "It's faster.",
            "category": "Gadgets",
            "score": 8,
            "relevant": True
        }
    ]

    md = format_newsletter_markdown(articles, title="Tech Weekly")

    assert "# Tech Weekly" in md
    assert "## Artificial Intelligence" in md
    assert "## Gadgets" in md
    assert "[AI Breakthrough](http://ai.com)" in md
    assert "score: 10/10" in md
    assert "AI is now sentient." in md

def test_format_markdown_empty():
    md = format_newsletter_markdown([], title="Empty Newsletter")
    assert "No articles found" in md

def test_format_html_with_articles():
    articles = [
        {
            "title": "AI Breakthrough",
            "link": "http://ai.com",
            "summary": "AI is now sentient.",
            "category": "Artificial Intelligence",
            "score": 10
        }
    ]

    html = format_newsletter_html(articles, title="Tech Weekly")

    assert "<h1>Tech Weekly</h1>" in html
    assert "<h2>Artificial Intelligence</h2>" in html
    assert '<a href="http://ai.com">AI Breakthrough</a>' in html
    assert "Importance Score: 10/10" in html
