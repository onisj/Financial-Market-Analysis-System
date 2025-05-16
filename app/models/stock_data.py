import uuid
from sqlalchemy import Column, String, Text, Float, DateTime
from datetime import datetime
from app.models.base import Base
from sqlalchemy.dialects.postgresql import UUID

class StockNews(Base):
    __tablename__ = "stock_news"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    symbol = Column(String, index=True)
    headline = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    raw_content = Column(Text, nullable=False)
    summary = Column(Text, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    relevance_score = Column(Float, nullable=True)
    published_date = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
