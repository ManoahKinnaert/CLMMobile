var socket = io("/timeservice")
let startStopBtn = document.getElementById("start-stop-btn")
let forwardBtn = document.getElementById("next")
let backwardBtn = document.getElementById("prev")
let timeLbl = document.getElementById("time-lbl")

startStopBtn.onclick = () => {
    socket.emit("toggle")
    console.log("test")
}

socket.on("status", (data) => {
    if (data.timer_started === true) {
        startStopBtn.textContent = "Stop"
    } else {
        startStopBtn.textContent = "Start"
    }
})

socket.on("clockdata", (data) => {
    const isOvertime = data.remaining <= 0
    const totalSeconds = isOvertime ? data.over_time : data.remaining

    const mins = Math.floor(totalSeconds / 60)
    const secs = totalSeconds - mins * 60

    timeLbl.innerText = `${mins}:${String(secs).padStart(2, "0")}`
    if (isOvertime) timeLbl.style.color = "red"
})