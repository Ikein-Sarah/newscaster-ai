import feedparser

urls = {
    "Anthropic Engineering": "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
    "Google DeepMind": "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_deepmind.xml",
}

for name, url in urls.items():
    feed = feedparser.parse(url)
    print(f"\n=== {name} ===")
    print("bozo:", feed.bozo)
    print("bozo reason:", getattr(feed, "bozo_exception", None))
    print("HTTP status:", getattr(feed, "status", "n/a"))
    print("entries:", len(feed.entries))
    if feed.entries:
        e = feed.entries[0]
        print("first title:", e.get("title"))
        print("has published_parsed:", getattr(e, "published_parsed", None) is not None)