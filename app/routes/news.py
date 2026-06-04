from fastapi import APIRouter
from app.services.scraper_service import scrape_ai_news

router = APIRouter(
    prefix="/api",
    tags=["News"]
)


@router.get("/news")
def get_news():

    return scrape_ai_news()