var socket = io("/timer")
// buttons
let startStopBtn = document.getElementById("start-stop-btn")
let forwardBtn = document.getElementById("next")
let backwardBtn = document.getElementById("prev")
// time label
let timeLbl = document.getElementById("time-lbl")
// dropdown
let dropdownContent = document.getElementById("dropdown-content")
let dropdown = document.getElementById("dropdown")
// other
let schedule = null
var currentBtn = null
var dropdownContentShown = false
// button click events
startStopBtn.onclick = () => {
    socket.emit("toggle")
}
forwardBtn.onclick = () => {
    socket.emit("next")
}
backwardBtn.onclick = () => {
    socket.emit("prev")
}
dropdown.onclick = () => {
    dropdownContentShown = !dropdownContentShown
    updateDropDownAppearance()
}
// socket events
socket.on("connect_event", (data) => {
    if (data.timer_started === true) {
        startStopBtn.textContent = "Stop"
    } else {
        startStopBtn.textContent = "Start"
    }
    timeLbl.innerText = `${data.current.time}:00`
    timeLbl.style.color = "black"
    setupDropDown(data.schedule)
    selectCurrent(data.current)
})
socket.on("status", (data) => {
    if (data.timer_started === true) {
        startStopBtn.textContent = "Stop"
    } else {
        startStopBtn.textContent = "Start"
    }

    timeLbl.innerText = `${data.current.time}:00`
    timeLbl.style.color = "black"
    selectCurrent(data.current)
})
socket.on("warning", (data) => {
    alert(data.message)
})
socket.on("clockdata", (data) => {
    if (startStopBtn.textContent === "Start") startStopBtn.textContent = "Stop"
    const isOvertime = data.remaining <= 0
    const totalSeconds = isOvertime ? data.over_time : data.remaining
    const mins = Math.floor(totalSeconds / 60)
    const secs = totalSeconds - mins * 60
    timeLbl.innerText = `${mins}:${String(secs).padStart(2, "0")}`
    if (isOvertime) timeLbl.style.color = "red"
})
// functions
function selectCurrent(current) {
    if (currentBtn) currentBtn.style.color = "rgba(0, 0, 0, 0.5)"
    dropdown.innerText = `${current.name} (${String(current.time).padStart(2, "0")}:00)`
    currentBtn = document.getElementById(current.name)
    currentBtn.style.color = "rgb(0, 0, 0)"
    dropdownContentShown = false 
    updateDropDownAppearance()
}
function setCurrent(item) {
    let index = 0
    schedule.forEach(element => {
        if (element === item) {
            index = schedule.indexOf(element)
        }
    })
    socket.emit("set_current", { "index": index })
}
function setupDropDown(items) {
    schedule = items 
    let html = ""
    items.forEach(element => {
        html += `<button id="${element.name}">${element.name} (${String(element.time).padStart(2, "0")}:00)</button>`
    })
    dropdownContent.innerHTML = html
    items.forEach(element => {
        let btn = document.getElementById(element.name)
        btn.onclick = () => { setCurrent(element) }
    })
}
function updateDropDownAppearance() {
    if (dropdownContentShown) {
        dropdownContent.style.display = "block"
    } else {
        dropdownContent.style.display = "none"
    }
}