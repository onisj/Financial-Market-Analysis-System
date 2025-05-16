from fastapi import APIRouter
from app.utils.vector_store import retrieve_relevant_news, analyze_sentiment
from app.utils.llm import generate_financial_advice
import logging

router = APIRouter()

@router.get("/financial-advice")
async def get_financial_advice(query: str):
    """
    API endpoint to provide financial advice based on stock news.
    """
    logging.info(f"🔍 Processing user query: {query}")

    # Retrieve relevant news
    retrieved_news = retrieve_relevant_news(query, top_k=5)

    if retrieved_news == "No relevant stock news found.":
        return {"financial_advice": "No recent stock news available for your query."}

    # Sentiment analysis on retrieved news
    sentiment_scores = [analyze_sentiment(news) for news in retrieved_news.split("\n")]

    # Count occurrences
    sentiment_count = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for sentiment in sentiment_scores:
        sentiment_count[sentiment] += 1

    logging.info(f"📊 Sentiment Analysis: {sentiment_count}")

    # Determine market sentiment
    dominant_sentiment = max(sentiment_count, key=sentiment_count.get)

    # Get LLM-based financial advice
    llm_response = generate_financial_advice(query, retrieved_news)

    # Construct final response
    return {
        "market_sentiment": dominant_sentiment,
        "financial_advice": llm_response
    }
