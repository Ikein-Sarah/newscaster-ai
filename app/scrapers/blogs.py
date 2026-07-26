import feedparser
from pydantic import BaseModel
from datetime import datetime, timezone, timedelta


class Article(BaseModel):
    title: str
    url: str
    source: str
    published_at: datetime
    description: str = ""

class RSSScraper:
    def __init__(self, feeds: dict[str,str]):
        self.feeds = feeds
    
    def get_articles(self, hours : int = 24) -> list[Article]:
        cutoff = datetime.now(timezone.utc) - timedelta(hours = hours)
        articles = []
        seen_urls = set()


        for source, url in self.feeds.items():
            feed = feedparser.parse(url)

            for entry in feed.entries:
                published_parsed =  getattr(entry, "published_parsed", None)
                if not published_parsed:
                    continue

                published_at = datetime(*published_parsed[:6], tzinfo = timezone.utc )
                if published_at < cutoff:
                    continue

                link = entry.get("link", "")
                if link in seen_urls:
                    continue
                seen_urls.add(link)

                articles.append(Article(
                    title = entry.get("title", ""),
                    url = link,
                    source = source,
                    published_at = published_at,
                    description = entry.get("summary", "")
                ))

        return articles



if __name__ == "__main__":
    FEEDS = {
        "Simon Willison": "https://simonwillison.net/atom/everything/",
        "Anthropic Engineering": "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
        "Hugging Face": "https://huggingface.co/blog/feed.xml",
        "OpenAI": "https://openai.com/news/rss.xml",
        "Hacker News": "https://hnrss.org/frontpage?points=100",
    }

    scraper = RSSScraper(FEEDS)
    articles = scraper.get_articles(hours=72)

    print(f"Found {len(articles)} articles\n")
    for a in articles:
        print(f"[{a.source}] {a.title}")