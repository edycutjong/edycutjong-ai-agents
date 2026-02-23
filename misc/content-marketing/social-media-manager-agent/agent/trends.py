import feedparser
import random
import datetime

class TrendMonitor:
    def __init__(self, sources=None):
        self.sources = sources or [
            "https://feeds.feedburner.com/TechCrunch/",
            "http://rss.slashdot.org/Slashdot/slashdotMain",
            "https://www.theverge.com/rss/index.xml"
        ]
        self.mock_trends = [
            {"topic": "AI Agents", "volume": "1.2M", "sentiment": "Positive", "source": "Mock Data"},
            {"topic": "Quantum Computing", "volume": "850K", "sentiment": "Neutral", "source": "Mock Data"},
            {"topic": "SpaceX Launch", "volume": "2.1M", "sentiment": "Positive", "source": "Mock Data"},
            {"topic": "Cybersecurity Threats", "volume": "600K", "sentiment": "Negative", "source": "Mock Data"},
            {"topic": "Green Energy Tech", "volume": "450K", "sentiment": "Positive", "source": "Mock Data"},
        ]

    def get_trends(self):
        trends = []
        try:
            for url in self.sources:
                feed = feedparser.parse(url)
                if feed.entries:
                    for entry in feed.entries[:3]:  # Top 3 from each
                        trends.append({
                            "topic": entry.title,
                            "volume": f"{random.randint(10, 500)}K",  # Simulated volume
                            "sentiment": random.choice(["Positive", "Neutral", "Mixed"]), # Simulated sentiment
                            "source": feed.feed.title if 'title' in feed.feed else "RSS Feed",
                            "link": entry.link
                        })
        except Exception as e:
            print(f"Error fetching trends: {e}")

        # Fallback if no trends fetched or error
        if not trends:
            return self.mock_trends

        # Add some mock trends to fill if few real ones
        if len(trends) < 5:
            trends.extend(self.mock_trends[:5-len(trends)])

        return trends

    def get_trend_summary(self):
        trends = self.get_trends()
        summary = "Current Top Trends:\n"
        for i, trend in enumerate(trends[:5], 1):
            summary += f"{i}. {trend['topic']} ({trend['volume']}) - {trend['sentiment']}\n"
        return summary

if __name__ == "__main__":
    monitor = TrendMonitor()
    print(monitor.get_trend_summary())
