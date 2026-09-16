var socket = io("/timeservice")
let startStopBtn = document.getElementById("start-stop-btn")
let forwardBtn = document.getElementById("next")
let backwardBtn = document.getElementById("prev")
let timeLbl = document.getElementById("time-lbl")

let dropdownContent = document.getElementById("dropdown-content")
let dropdown = document.getElementById("dropdown")
var currentBtn = null

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

// Socket events
socket.on("connect", () => {
    socket.emit("connect_event")
})

socket.on("connect_event", (data) => {
    console.log("test")
    if (data.timer_started === true) {
        startStopBtn.textContent = "Stop"
    } else {
        startStopBtn.textContent = "Start"
    }
    timeLbl.innerText = `${data.current.time}:00`
    console.log(data.schedule)
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

socket.on("clockdata", (data) => {
    if (startStopBtn.textContent === "Start") startStopBtn.textContent = "Stop"
    const isOvertime = data.remaining <= 0
    const totalSeconds = isOvertime ? data.over_time : data.remaining

    const mins = Math.floor(totalSeconds / 60)
    const secs = totalSeconds - mins * 60

    timeLbl.innerText = `${mins}:${String(secs).padStart(2, "0")}`
    if (isOvertime) timeLbl.style.color = "red"
})

function selectCurrent(current) {
    if (currentBtn) currentBtn.style.color = "rgba(0, 0, 0, 0.5)"
    dropdown.innerText = current.name
    currentBtn = document.getElementById(current.name)
    currentBtn.style.color = "rgb(0, 0, 0)"
}

// Setup all the items in the dropdown
function setupDropDown(items) {
    let html = ""
    items.forEach(element => {  
        html += `<button id="${element.name}">${element.name}</button>`
    })
    dropdownContent.innerHTML = html 
}