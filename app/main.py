from app.scrapers.blogs import RSSScraper, FEEDS
from app.services.analyzer import analyze_article
from app.scrapers.extractor import extract_content
from app.database.repository import (
    save_articles,
    get_articles_by_status,
    update_content,
    save_analysis,
    get_analyzed_articles,
    mark_emailed
)
from app.services.emailer import send_email
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def run():
    scraper = RSSScraper(FEEDS)
    articles = scraper.get_articles(hours=24)
    logger.info(f"Scraped {len(articles)} articles")

    saved = save_articles(articles)
    logger.info(f"Saved {saved} new articles")

    pending = get_articles_by_status("fetched")
    logger.info(f"Fetching content for {len(pending)} articles")
    for article in pending:
        text = extract_content(article.url)
        if text:
            update_content(article.id, text)

    to_analyze = get_articles_by_status("content_fetched")
    logger.info(f"Analyzing {len(to_analyze)} articles")
    for article in to_analyze:
        result = analyze_article(article.title, article.source, article.content)
        if result:
            save_analysis(article.id, result)
            print(f"  {result.get('story_type'):12} {article.title[:50]}")
    

    to_send = get_analyzed_articles(hours=24)
    if to_send:
        send_email(to_send)
        mark_emailed([a.id for a in to_send])
        logger.info(f"Emailed {len(to_send)} articles")
    else:
        logger.info("Nothing to email")


if __name__ == "__main__":
    try:
        run()
    except Exception:
        logger.exception("Pipeline failed")
        sys.exit(1)
    