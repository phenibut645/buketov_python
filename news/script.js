
const submitButton = document.getElementById("submit-article")
const articleSource = document.getElementById("article-source")
const articleDate = document.getElementById("article-date")
const articleTitle = document.getElementById("article-title")

const newsContainer = document.getElementsByClassName("item-container")[0]

let lastId = -1;

async function getJSONData(path){
    const response = await fetch(path); 
    const json = await response.json();
    return json
}

function getLastId(){
    lastId++;
    return lastId;
}

async function importData(){
    const json = await getJSONData("./news.json");
    const keys = ["technology", "sport", "economy"]
    keys.forEach(key => {
        json[key].forEach(article =>{
            article["id"] = getLastId();
            article["source"] = key;
            news[key].push(article)
        })
    })
}
importData(); 

submitButton.addEventListener("click", (target) =>{
    news[articleSource.value].push({
        id: lastId,
        title: articleTitle.value,
        source: articleSource.value,
        date: articleDate.value
    })
    lastId++
})

function showNews(category) {
    newsContainer.innerHTML = ""
    news[category].forEach(element => {
        addArticle(element, category)
    });
}

function addArticle(element, category){
    const divContainer = document.createElement("div")
    const titleElement = document.createElement("p")
    const dateElement = document.createElement("p")
    const sourceElement = document.createElement("p")
    const buttonElement = document.createElement("button")
    titleElement.innerHTML = element.title
    dateElement.innerHTML = element.date
    sourceElement.innerHTML = element.source
    buttonElement.innerHTML = "Delete article"
    buttonElement.id = element.id

    buttonElement.addEventListener("click", (target) =>{
        let index = -1;
        news[category].forEach(element => {
            index++
            if (element.id.value === target.target.id.value) {
                return
            }
        })
        news[category].splice(index, 1);

        showNews(category)
    })

    divContainer.appendChild(titleElement)
    divContainer.appendChild(dateElement)
    divContainer.appendChild(sourceElement)
    divContainer.appendChild(buttonElement)
    newsContainer.appendChild(divContainer)
}

const news = {
    technology: [
    ],
    sport: [
    ],
    economy: [
    ]
}
