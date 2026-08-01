from app.scrapers.blogs import RSSScraper, FEEDS
from app.scrapers.extractor import extract_content
from app.database.repository import save_articles, get_articles_by_status, update_content


def run():
    scraper = RSSScraper(FEEDS)
    articles = scraper.get_articles(hours=24)
    print(f"Scraped {len(articles)} articles")

    saved =  save_articles(articles)
    print(f"Saved {saved} articles")


    pending = get_articles_by_status("fetched")
    print(f"Fetching content for {len(pending)} articles")


    for article in pending:
        text = extract_content(article.url)
        if text:
            update_content(article.id, text)
            print(f"  ok: {article.title[:60]}")
        else:
            print(f"  failed: {article.title[:60]}")



if __name__ == "__main__":
    run()
    