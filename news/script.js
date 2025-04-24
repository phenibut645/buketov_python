
const submitButton = document.getElementById("submit-article")
const articleSource = document.getElementById("article-source")
const articleDate = document.getElementById("article-date")
const articleTitle = document.getElementById("article-title")

const newsContainer = document.getElementsByClassName("item-container")[0]

submitButton.addEventListener("click", (target) =>{
    console.log(123)
    news[articleSource.value].push({
        title: articleTitle.value,
        source: articleSource.value,
        date: articleDate.value
    })
})

function showNews(category) {
    news[category].forEach(element => {
        addArticle(element.title, element.source, element.date)
    });
}

function addArticle(title, source, date){
    const divContainer = document.createElement("div")
    const titleElement = document.createElement("p")
    const dateElement = document.createElement("p")
    const sourceElement = document.createElement("p")
    titleElement.innerHTML = title
    dateElement.innerHTML = date
    sourceElement.innerHTML = source
    divContainer.appendChild(titleElement)
    divContainer.appendChild(dateElement)
    divContainer.appendChild(sourceElement)
    newsContainer.appendChild(divContainer)
}

const news = {
    technology: [
        {
            title: "",
            source: "",
            date: ""
        }
    ],
    sport: [
        {}
    ],
    economy: [
        {}
    ]
}