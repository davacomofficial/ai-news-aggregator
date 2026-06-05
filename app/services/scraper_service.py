import requests

from bs4 import BeautifulSoup

from app.services.ai_service import summarize_article

from app.models.news_model import (
    SessionLocal,
    News
)

from app.services.trend_service import (
    extract_trending_topics
)


def scrape_ai_news():

    url = "https://techcrunch.com/category/artificial-intelligence/"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    articles = []

    db = SessionLocal()

    posts = soup.find_all("div", class_="loop-card")[:5]

    for post in posts:

        try:

            title_tag = post.find("h3")

            link_tag = post.find("a")

            image_tag = post.find("img")

            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)

            article_url = link_tag["href"] if link_tag else ""

            thumbnail = ""

            if image_tag and image_tag.get("src"):
                thumbnail = image_tag["src"]

            summary = summarize_article(title)

            news_data = {

                "title": title,

                "summary": summary,

                "thumbnail": thumbnail,

                "article_url": article_url
            }

            articles.append(news_data)

            existing_news = db.query(News).filter(
                News.title == title
            ).first()

            if not existing_news:

                new_news = News(

                    title=title,

                    summary=summary,

                    thumbnail=thumbnail,

                    article_url=article_url
                )

                db.add(new_news)

                db.commit()

        except Exception as e:

            print("SCRAPER ERROR:", e)

    db.close()

    trending_topics = extract_trending_topics(
    articles
    )

    return {

        "status": True,

        "articles": articles,

        "trending_topics": trending_topics
    }