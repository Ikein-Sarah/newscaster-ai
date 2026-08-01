from app.scrapers.blogs import RSSScraper, FEEDS
from app.services.analyzer import analyze_article
from app.scrapers.extractor import extract_content
from app.database.repository import (
    save_articles,
    get_articles_by_status,
    update_content,
    save_analysis,
)



def run():
    scraper = RSSScraper(FEEDS)
    articles = scraper.get_articles(hours=24)
    print(f"Scraped {len(articles)} articles")

    saved = save_articles(articles)
    print(f"Saved {saved} new articles")

    pending = get_articles_by_status("fetched")
    print(f"Fetching content for {len(pending)} articles")
    for article in pending:
        text = extract_content(article.url)
        if text:
            update_content(article.id, text)

    to_analyze = get_articles_by_status("content_fetched")
    print(f"Analyzing {len(to_analyze)} articles")
    for article in to_analyze:
        result = analyze_article(article.title, article.source, article.content)
        if result:
            save_analysis(article.id, result)
            print(f"  {result.get('story_type'):12} {article.title[:50]}")


if __name__ == "__main__":
    run()
    