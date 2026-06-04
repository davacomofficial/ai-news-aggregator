import requests
from bs4 import BeautifulSoup


def scrape_ai_news():

    url = "https://techcrunch.com/category/artificial-intelligence/"

    response = requests.get(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    articles = []

    news_cards = soup.find_all("h3")[:5]

    for item in news_cards:

        title = item.get_text(strip=True)

        articles.append({
            "title": title
        })

    return {
        "status": True,
        "articles": articles
    }