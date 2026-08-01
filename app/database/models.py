from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String, DateTime, Text, UniqueConstraint
from datetime import datetime, timezone




class Base(DeclarativeBase):
    pass


class ArticleRow(Base):
    __tablename__ = "articles"


    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(2000))
    title: Mapped[str] = mapped_column(String(500))
    source: Mapped[str] = mapped_column(String(100))
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    description: Mapped[str] = mapped_column(Text, default= "")
    content: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="fetched")
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    summary: Mapped[str] = mapped_column(Text, server_default="")
    key_insight: Mapped[str] = mapped_column(Text, server_default="")
    angle: Mapped[str] = mapped_column(Text, server_default="")
    story_type: Mapped[str] = mapped_column(String(50), server_default="")
    specific_detail: Mapped[str] = mapped_column(Text, server_default="")
    

    __table_args__ = (UniqueConstraint("url", name="uq_articles_url"),)


