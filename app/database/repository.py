from sqlalchemy.dialects.postgresql import insert
from app.database.database import SessionLocal
from app.database.models import ArticleRow

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


