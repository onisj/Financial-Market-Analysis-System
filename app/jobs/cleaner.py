from app.utils.tavily_client import fetch_stock_news, extract_news_content
from app.config.dependencies import get_db
from app.models.stock_data import StockNews
from datetime import datetime
from sqlalchemy.orm import Session
from datetime import timedelta

async def delete_old_news(db: Session):
    """
    Deletes news older than 24 hours.
    """
    expiry_time = datetime.utcnow() - timedelta(hours=24)
    db.query(StockNews).filter(StockNews.timestamp < expiry_time).delete()
    await db.commit()
