from collections import Counter
import re


def extract_trending_topics(articles):

    text = " ".join([
        article["title"]
        for article in articles
    ])

    words = re.findall(r"\b[a-zA-Z]{4,}\b", text)

    blacklist = {

        "about",
        "their",
        "would",
        "there",
        "these",
        "those",
        "which",
        "techcrunch",
        "google",
        "cloud",
        "using"
    }

    filtered_words = [

        word.lower()

        for word in words

        if word.lower() not in blacklist
    ]

    counter = Counter(filtered_words)

    topics = counter.most_common(10)

    return topics