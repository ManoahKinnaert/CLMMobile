const socket = io("/timer")
// buttons
const startStopBtn = document.getElementById("start-stop-btn")
const modeBtn = document.getElementById("mode-btn")
const forwardBtn = document.getElementById("next")
const backwardBtn = document.getElementById("prev")
// time label
const timeLbl = document.getElementById("time-lbl")
// dropdown
const dropdownContent = document.getElementById("dropdown-content")
const dropdown = document.getElementById("dropdown")
// other
let schedule = null
let currentBtn = null
let dropdownContentShown = false
let circuitOverseerMode = null
// button click events
startStopBtn.onclick = () => {
    socket.emit("toggle")
}
modeBtn.onclick = () => {
    socket.emit("set_circuitoverseer", { circuit_overseer: !circuitOverseerMode })
    location.reload()   // Only for updating the modeBtn text
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
    timeLbl.innerText = `${String(data.current.time).padStart(2, "0")}:00`
    timeLbl.style.color = "black"
    
    circuitOverseerMode = data.circuit_overseer
})
socket.on("schedule", (data) => {
    setupDropDown(data.schedule)
    selectCurrent(data.current)
})
socket.on("status", (data) => {
    if (data.timer_started === true) {
        startStopBtn.textContent = "Stop"
    } else {
        startStopBtn.textContent = "Start"
    }

    if (!data.timer_started) {
        timeLbl.innerText = `${String(data.current.time).padStart(2, "0")}:00`
        timeLbl.style.color = "black"
    }
    
    if (circuitOverseerMode != data.circuit_overseer) {
        circuitOverseerMode = data.circuit_overseer
    }    
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
    timeLbl.innerText = `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`
    if (isOvertime) timeLbl.style.color = "red"
})
// functions
function selectCurrent(current) {
    if (currentBtn !== null && currentBtn) currentBtn.style.color = "rgba(0, 0, 0, 0.5)"
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