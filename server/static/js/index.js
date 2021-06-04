let label = document.querySelector("label")
let ol = document.querySelector("ol")
let buttonChangeSite = document.querySelector("button")

const url = "http://127.0.0.1:8080/data"
const headers = { "Content-Type": "application/json" }

let arrayNumbers

/*
Сбор данных с сервера
*/
async function newData() {
    const response = await fetch(url, { method: "get", headers: headers })
    const data = await response.json()
    arrayNumbers = data["GET"]["numbers"]
    return data["GET"]
}

/*
Создание списка из
пришедших данных
*/
async function createNewTagLi() {
    let data = await newData()
    let numbers = data["numbers"]
    let name = data["name"]
    let phone = data["phone"]
    label.textContent = `${name} ${phone}`
    for (let num of numbers) {
        let new_child = document.createElement("li")
        new_child.textContent = num
        ol.appendChild(new_child)
    }
}

buttonChangeSite.onclick = () => {
    location["href"] = "second"
}

createNewTagLi()
setInterval(() => location.reload(), 5000)
