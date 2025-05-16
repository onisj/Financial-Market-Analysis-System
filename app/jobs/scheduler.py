from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
from app.jobs.scraper import scrape_and_store_news
from app.jobs.cleaner import delete_old_news
import logging
from datetime import timedelta

scheduler = BackgroundScheduler()

@scheduler.scheduled_job("interval", hours=6)
def scheduled_scraping():
    """
    Runs scraping every 6 hours.
    """
    logging.info("🔄 Running scheduled scraping job...")
    asyncio.run(scrape_and_store_news())

@scheduler.scheduled_job("interval", hours=24)
def cleanup_old_news():
    """
    Runs every 24 hours to delete old news.
    """
    logging.info("🗑️ Deleting old stock news...")
    asyncio.run(delete_old_news())


def start_scheduler():
    scheduler.start()

