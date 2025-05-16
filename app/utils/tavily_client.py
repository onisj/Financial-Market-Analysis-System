from tavily import TavilyClient
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    logging.error("❌ TAVILY_API_KEY is missing! Make sure it's set in the .env file.")
else:
    logging.info("✅ Tavily API Key loaded successfully.")

# Initialize Tavily Client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def fetch_stock_news(symbol: str, max_results: int = 7):
    """
    Fetches the latest stock news using the Tavily Search API.
    """
    query = f"{symbol} stock news today"
    logging.info(f"🔍 Fetching news for {symbol} (max {max_results} results)...")

    try:
        response = tavily_client.search(
            query=query,
            topic="news",
            search_depth="advanced",
            max_results=max_results,
            include_domains=["finance.yahoo.com", "marketwatch.com", "https://www.cnbc.com"],
            time_range="day",
            include_answer=False,
            include_raw_content=True,
        )
        results = response.get("results", [])
        logging.info(f"✅ Found {len(results)} articles for {symbol}.")
        return results

    except Exception as e:
        logging.error(f"❌ Error fetching news for {symbol}: {e}", exc_info=True)
        return []

def extract_news_content(urls: list):
    """
    Extracts raw content from news articles using the Tavily Extract API.
    """
    if not urls:
        logging.warning("⚠️ No URLs provided for content extraction.")
        return []

    logging.info(f"📄 Extracting content from {len(urls)} URLs...")

    try:
        response = tavily_client.extract(urls=urls, include_images=False)
        extracted_results = response.get("results", [])
        logging.info(f"✅ Successfully extracted content from {len(extracted_results)} URLs.")
        return extracted_results

    except Exception as e:
        logging.error(f"❌ Error extracting content: {e}", exc_info=True)
        return []
