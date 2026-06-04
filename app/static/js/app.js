async function loadNews() {

    const response = await fetch("/api/news")

    const data = await response.json()

    const newsList = document.getElementById("newsList")

    newsList.innerHTML = ""

    data.articles.forEach(article => {

        newsList.innerHTML += `

            <div class="card">

                <h3>${article.title}</h3>

                <p>${article.summary}</p>

            </div>

        `
    })
}