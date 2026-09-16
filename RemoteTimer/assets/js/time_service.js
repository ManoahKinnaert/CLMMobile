var socket = io("/timeservice")
let startStopBtn = document.getElementById("start-stop-btn")
let forwardBtn = document.getElementById("next")
let backwardBtn = document.getElementById("prev")
let timeLbl = document.getElementById("time-lbl")

let dropdownContent = document.getElementById("dropdown-content")
let dropdown = document.getElementById("dropdown")

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

startStopBtn.onclick = () => {
    socket.emit("toggle")
}

socket.on("status", (data) => {
    if (data.timer_started === true) {
        startStopBtn.textContent = "Stop"
    } else {
        startStopBtn.textContent = "Start"
    }

    timeLbl.innerText = `${data.current.time}:00`
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
    dropdown.innerText = current.talktype[1]
}

// Setup all the items in the dropdown
function setupDropDown(items) {
    let html = ""
    items.forEach(element => {  
        html += `<button>${element.talktype[1]}</button>`
    })
    dropdownContent.innerHTML = html 
}