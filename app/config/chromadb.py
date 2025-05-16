import chromadb

chroma_client = chromadb.PersistentClient(path="./vector_db")

stock_news_collection = chroma_client.get_or_create_collection(name="stock_news")

def get_vector_store():
    """Returns the ChromaDB collection for stock news storage."""
    return stock_news_collection

def close_chromadb():
    chroma_client._client.stop()