from fastapi import FastAPI
from app.config.db import async_engine
from app.models.base import Base
from fastapi.middleware.cors import CORSMiddleware
from app.jobs.scheduler import start_scheduler
from app.jobs.scraper import scrape_and_store_news
from app.routes import query
from app.config.chromadb import close_chromadb
import asyncio

app = FastAPI(title="Financial Advice System")

# Create a startup event handler
@app.on_event("startup")
async def startup():
    # Create tables in the database
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    
    start_scheduler()

    asyncio.create_task(scrape_and_store_news())

# @app.on_event("shutdown")
# def shutdown_event():
#     close_chromadb()

# CORS Middleware (Allows Frontend to Connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://marketmind-ai.vercel.app", "http://localhost:8080"],  # Allow all origins (Frontend React App can connect)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(query.router, prefix="/api", tags=["Financial Advice"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Financial Advice API!"}
