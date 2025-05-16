from app.utils.tavily_client import fetch_stock_news, extract_news_content
from app.config.dependencies import get_db
from app.models.stock_data import StockNews
from datetime import datetime
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.utils.vector_store import store_news_embeddings, cleanup_old_news

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def scrape_and_store_news():
    """
    Scrapes stock news, stores in the database, and updates vector DB.
    """
    stock_symbols = ["NVDA","GOOG","TSLA"]

    async for db in get_db():
        for symbol in stock_symbols:
            try:
                logging.info(f"🔍 Scraping news for {symbol}...")

                news_results = fetch_stock_news(symbol)
                if not news_results:
                    logging.warning(f"⚠️ No news found for {symbol}")
                    continue

                logging.info(f"✅ Found {len(news_results)} articles for {symbol}")

                urls = [news["url"] for news in news_results]
                extracted_articles = extract_news_content(urls)

                logging.info(f"📰 Extracted {len(extracted_articles)} full articles for {symbol}")

                await store_scraped_news(symbol, extracted_articles, db)

                store_news_embeddings(symbol, extracted_articles)

                logging.info(f"💾 Stored {len(extracted_articles)} articles in database & vector DB for {symbol}")

            except Exception as e:
                logging.error(f"❌ Error during scraping for {symbol}: {e}", exc_info=True)

async def store_scraped_news(symbol: str, articles: list, db: Session):
    """
    Saves scraped news articles to the database.
    """
    try:
        for article in articles:
            db_news = StockNews(
                symbol=symbol,
                headline=article["raw_content"][:150],
                url=article["url"],
                raw_content=article["raw_content"],
                summary=article["raw_content"][:400],
                sentiment_score=None,  # Placeholder
                relevance_score=0.0,  # Placeholder
                published_date=datetime.utcnow(),
                timestamp=datetime.utcnow()
            )
            db.add(db_news)
        
        await db.commit()
        logging.info(f"✅ Successfully committed {len(articles)} articles for {symbol}")

    except SQLAlchemyError as db_error:
        logging.error(f"❌ Database error while storing {symbol} articles: {db_error}", exc_info=True)
        await db.rollback()

    except Exception as e:
        logging.error(f"❌ Unexpected error in `store_scraped_news()`: {e}", exc_info=True)
