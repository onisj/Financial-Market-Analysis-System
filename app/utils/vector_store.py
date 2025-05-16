from sentence_transformers import SentenceTransformer
from app.config.chromadb import get_vector_store
import logging
import uuid
import datetime
from datetime import timedelta

embedding_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

def chunk_text(text, chunk_size=256, overlap=50):
    """
    Splits text into overlapping chunks to preserve context.
    """
    chunks = []
    words = text.split()
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# Ensure VADER lexicon is downloaded
nltk.download("vader_lexicon")

# Initialize Sentiment Analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyzes sentiment of the news text.
    Returns: Positive, Neutral, or Negative.
    """
    score = sentiment_analyzer.polarity_scores(text)["compound"]
    
    if score > 0.05:
        return "Positive"
    elif score < -0.05:
        return "Negative"
    else:
        return "Neutral"

def store_news_embeddings(stock_symbol, articles):
    """
    Converts news articles into embeddings and stores them in ChromaDB.
    """
    vector_store = get_vector_store()

    for article in articles:
        news_id = str(uuid.uuid4())  # Unique ID
        text_chunks = chunk_text(article["raw_content"])

        for chunk in text_chunks:
            embedding = embedding_model.encode(chunk).tolist()
            vector_store.add(
                ids=[news_id], 
                metadatas=[{"symbol": stock_symbol, "headline": (f'{article["raw_content"][:150]}'), "url": article["url"]}],
                embeddings=[embedding]
            )
    
    logging.info(f"✅ Stored {len(articles)} news articles for {stock_symbol} in ChromaDB")

def retrieve_relevant_news(query, top_k=3):
    """
    Retrieves the most relevant news chunks for a given user query.
    """
    vector_store = get_vector_store()
    query_embedding = embedding_model.encode(query).tolist()

    results = vector_store.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    if not results["ids"]:
        return "No relevant stock news found."

    retrieved_news = []
    for i, news_id in enumerate(results["ids"][0]):
        metadata = results["metadatas"][0][i]
        retrieved_news.append(
            f"{metadata['headline']} ({metadata['url']})"
        )

    return "\n".join(retrieved_news)


def cleanup_old_news():
    """
    Deletes news articles older than 24 hours from ChromaDB.
    """
    vector_store = get_vector_store()
    cutoff_time = datetime.utcnow() - timedelta(hours=24)

    all_data = vector_store.get()

    if not all_data["ids"]:
        logging.info("✅ No old news to clean up.")
        return

    old_ids = []
    for i, metadata in enumerate(all_data["metadatas"]):
        stored_time = datetime.strptime(metadata.get("timestamp", ""), "%Y-%m-%d %H:%M:%S")
        if stored_time < cutoff_time:
            old_ids.append(all_data["ids"][i])

    if old_ids:
        vector_store.delete(ids=old_ids)
        logging.info(f"🗑️ Deleted {len(old_ids)} old news articles from ChromaDB.")
    else:
        logging.info("✅ No old news found for cleanup.")
