async function loadNews() {

    const response = await fetch("/api/news")

    const data = await response.json()

    const newsList = document.getElementById("newsList")

    const trendingContainer = document.getElementById(
        "trendingTopics"
    )

    newsList.innerHTML = ""

    trendingContainer.innerHTML = ""

    data.trending_topics.forEach(topic => {

        trendingContainer.innerHTML += `

            <div class="topic-tag">

                #${topic[0]}

                <span>
                    ${topic[1]}
                </span>

            </div>

        `
    })

    data.articles.forEach(article => {

        newsList.innerHTML += `

            <div class="card">

                <img
                    src="${article.thumbnail}"
                    class="thumbnail"
                >

                <div class="content">

                    <h3>${article.title}</h3>

                    <p>${article.summary}</p>

                    <a
                        href="${article.article_url}"
                        target="_blank"
                    >
                        Read Full Article
                    </a>

                </div>

            </div>

        `
    })
}