# Financial Advice System for Stock Trading (RAG-Based)

A **Retrieval-Augmented Generation (RAG)** system that provides AI-powered financial advice for stock trading. It collects and processes real-time news for NVIDIA (NVDA), Tesla (TSLA), and Alphabet (GOOG) every 6 hours, using a Large Language Model (LLM) to generate buy/sell/hold recommendations.

## Introduction

### Problem Statement
Stock trading without timely, accurate information is risky, often leading to uninformed decisions and financial losses. Traders need real-time market insights to optimize buy/sell/hold strategies.

### Solution
This project delivers a RAG-based system that:
- **Scrapes** stock news every 6 hours.
- **Stores** news temporarily in a database (24-hour expiry).
- **Embeds** news in a vector store for efficient retrieval.
- **Generates** LLM-powered financial advice based on user queries.

## System Architecture

### Components
| Component | Description |
|-----------|-------------|
| **Web Scraper** | Fetches stock news every 6 hours using Tavily API. |
| **Database** | Stores news in PostgreSQL/SQLite with 24-hour expiry. |
| **Vector Store** | Uses ChromaDB to embed news for fast similarity search. |
| **Query System** | LLM (GPT-4) generates advice from retrieved news. |

### Data Flow
1. Web scraper collects news every 6 hours.
2. News is stored in the database and embedded in ChromaDB.
3. User submits a query (e.g., "Should I buy NVDA?").
4. System retrieves relevant news from ChromaDB.
5. LLM analyzes news and provides advice.

## Implementation Details

### Web Scraper
- **Tool**: Tavily API searches for "\<Stock Symbol> stock news today".
- **Frequency**: Runs every 6 hours via APScheduler.
- **Features**:
  - Extracts headlines, URLs, and raw content.
  - Stores data in the `StockNews` table.
  - Removes duplicates and irrelevant items.

### Temporary Data Storage
- **Database**: PostgreSQL (preferred) or SQLite.
- **Schema**: `StockNews` table:
  | Field | Type | Description |
  |-------|------|-------------|
  | `id` | UUID | Unique identifier |
  | `symbol` | String | Stock ticker (NVDA, TSLA, GOOG) |
  | `headline` | String | News headline |
  | `url` | String | Source link |
  | `raw_content` | Text | Full news content |
  | `timestamp` | Datetime | Storage time |
- **Expiry**: News older than 24 hours is auto-deleted.

### Vector Store
- **Tool**: ChromaDB for vector embeddings.
- **Process**:
  1. Extracts text from `StockNews`.
  2. Converts text to embeddings.
  3. Stores embeddings for similarity search.
  4. Retrieves relevant news for user queries.

### Financial Advice Query System
- **Input**: User query (e.g., "Should I buy TSLA stock?").
- **Process**:
  1. Searches ChromaDB for top-5 relevant news articles.
  2. GPT-4 analyzes news and generates advice.
- **Example Endpoint**:
  ```python
  @router.get("/financial-advice")
  async def get_financial_advice(query: str):
      news = retrieve_relevant_news(query, top_k=5)
      if not news:
          return {"financial_advice": "No relevant stock news found."}
      advice = generate_financial_advice(query, news)
      return {"financial_advice": advice}
  ```

### Deployment
- **Framework**: FastAPI with CORS for frontend integration.
- **Database**: Supports SQLite or PostgreSQL.
- **Endpoint**: `/financial-advice?query=<stock question>` returns AI-generated advice.
- **Deployment**: Configured for Render (`render.yaml` included).

## Conclusion
This RAG-based system delivers real-time, AI-driven stock trading advice by:
- Collecting and processing news every 6 hours.
- Using ChromaDB for efficient news retrieval.
- Leveraging GPT-4 for accurate buy/sell/hold recommendations.

### Next Steps
- Expand to support all stock symbols.
- Integrate additional data sources for improved accuracy.
- Add live stock price trends for enhanced insights.

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/onisj/Financial-Market-Analysis-System.git
   cd Financial-Market-Analysis-System
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   - Update `alembic.ini` with your database URL (PostgreSQL/SQLite).
   - Set Tavily API key in environment variables.
4. **Apply Migrations**:
   ```bash
   alembic upgrade head
   ```
5. **Run the Application**:
   ```bash
   python main.py
   ```
6. **Access API**:
   - Query: `http://localhost:8000/financial-advice?query=Should I buy NVDA stock?`

## License
MIT