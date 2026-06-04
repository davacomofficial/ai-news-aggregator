async function loadNews() {

    const response = await fetch("/api/news")

    const data = await response.json()

    const newsList = document.getElementById("newsList")

    newsList.innerHTML = ""

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