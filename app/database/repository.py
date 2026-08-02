from sqlalchemy.dialects.postgresql import insert
from app.database.database import SessionLocal
from app.database.models import ArticleRow
from datetime import datetime, timedelta, timezone

def save_articles(articles) -> int:
    saved = 0
    
    with SessionLocal() as session:
        for a in articles:
            stmt = (
                insert(ArticleRow)
                .values(
                    url=a.url,
                    title=a.title,
                    source=a.source,
                    published_at=a.published_at,
                    description=a.description,
                )
                .on_conflict_do_nothing(index_elements=["url"])
            )
            result = session.execute(stmt)
            saved += result.rowcount
    
        session.commit()
    
    return saved

def get_articles_by_status(status: str):
    with SessionLocal() as session:
        return session.query(ArticleRow).filter(ArticleRow.status == status).all()

def update_content(article_id: int, content: str):
    with SessionLocal() as session:
        article = session.query(ArticleRow).filter(ArticleRow.id == article_id).first()
        if article:
            article.content = content
            article.status = "content_fetched"
            session.commit()

def save_analysis(article_id: int, analysis: dict):
    required = ["story_type", "specific_detail", "angle", "key_insight", "summary"]
    missing = [f for f in required if not analysis.get(f)]
    if missing:
        print(f"  incomplete analysis for {article_id}, missing: {missing}")
        return

    with SessionLocal() as session:
        article = session.query(ArticleRow).filter(ArticleRow.id == article_id).first()
        if not article:
            print(f"  no article with id {article_id}")
            return

        article.story_type = analysis["story_type"]
        article.specific_detail = analysis["specific_detail"]
        article.angle = analysis["angle"]
        article.key_insight = analysis["key_insight"]
        article.summary = analysis["summary"]
        article.status = "analyzed"
        session.commit()


def get_analyzed_articles(hours: int = 24):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    with SessionLocal() as session:
        return (
            session.query(ArticleRow)
            .filter(ArticleRow.status == "analyzed", ArticleRow.fetched_at >= cutoff)
            .all()
        )


def mark_emailed(article_ids: list[int]):
    with SessionLocal() as session:
        session.query(ArticleRow).filter(ArticleRow.id.in_(article_ids)).update(
            {ArticleRow.status: "emailed"}, synchronize_session=False
        )
        session.commit()