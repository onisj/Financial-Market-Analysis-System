from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class StockNewsSchema(BaseModel):
    id: str
    symbol: str
    headline: str
    url: HttpUrl
    raw_content: str
    summary: Optional[str]
    sentiment_score: Optional[float]
    relevance_score: Optional[float]
    published_date: Optional[datetime]
    timestamp: datetime

    class Config:
        orm_mode = True
