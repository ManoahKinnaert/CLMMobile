var socket = io("/webclock")
let clock = document.getElementById("clock")
let talkLbl = document.getElementById("talk-lbl")
// socket events
socket.on("status", (data) => {
    talkLbl.innerText = `${data.current.name}   -   ${String(data.current.time).padStart(2, "0")}:00`
})
socket.on("webclockdata", (data) => {
    const isOvertime = data.remaining <= 0
    const totalSeconds = isOvertime ? data.over_time : data.remaining
    const mins = Math.floor(totalSeconds / 60)
    const secs = totalSeconds - mins * 60
    
    clock.innerText = `${mins}:${String(secs).padStart(2, "0")}`

    if (isOvertime) clock.style.color = "red"
    else if (!isOvertime && mins === 0 && secs <= 20) clock.style.color = "orange"
    else clock.style.color = "lime"
})