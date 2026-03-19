import pandas as pd
import random
import datetime

class Analytics:
    def __init__(self):
        self.platforms = ["Twitter", "LinkedIn", "Instagram"]  # pragma: no cover

    def get_growth_stats(self):
        """Returns mock growth statistics over the last 30 days."""
        dates = pd.date_range(end=datetime.datetime.today(), periods=30)  # pragma: no cover
        data = {  # pragma: no cover
            "Date": dates,
            "Followers": [random.randint(1000, 5000) + (i * random.randint(10, 50)) for i in range(30)],
            "Engagement": [random.randint(50, 500) for _ in range(30)],
            "Impressions": [random.randint(1000, 10000) for _ in range(30)]
        }
        return pd.DataFrame(data)  # pragma: no cover

    def get_recent_performance(self):
        """Returns mock performance of recent posts."""
        posts = [  # pragma: no cover
            {"Topic": "AI Trends", "Platform": "Twitter", "Likes": 120, "Shares": 45, "Comments": 12},
            {"Topic": "Remote Work", "Platform": "LinkedIn", "Likes": 350, "Shares": 80, "Comments": 40},
            {"Topic": "Product Launch", "Platform": "Instagram", "Likes": 800, "Shares": 20, "Comments": 150},
            {"Topic": "Coding Tips", "Platform": "Twitter", "Likes": 90, "Shares": 30, "Comments": 5},
            {"Topic": "Company Culture", "Platform": "LinkedIn", "Likes": 210, "Shares": 15, "Comments": 25},
        ]
        return pd.DataFrame(posts)  # pragma: no cover

    def get_platform_breakdown(self):
        """Returns mock breakdown of audience per platform."""
        return {  # pragma: no cover
            "Twitter": 45,
            "LinkedIn": 30,
            "Instagram": 25
        }
