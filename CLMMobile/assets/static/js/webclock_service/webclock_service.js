var socket = io("/webclockservice")
let digitalClock = document.getElementById("digital-clock")
let talkLbl = document.getElementById("talk-lbl")

// socket stuff
// socket connect
socket.on("connect", () => {
    console.log("connected")
})

socket.on("disconnect", () => {
    console.log("Server disconnected!")
})

socket.on("status", (data) => {
    talkLbl.innerText = `${data.current.name}   -   ${data.current.time}:00`
    digitalClock.innerText = `${data.current.time}:00`
    digitalClock.style.color = "white"
})

// getting timer data
socket.on("webclockdata", (data) => {
    console.log("test")
    const isOvertime = data.remaining <= 0
    const totalSeconds = isOvertime ? data.over_time : data.remaining

    const mins = Math.floor(totalSeconds / 60)
    const secs = totalSeconds - mins * 60

    digitalClock.innerText = `${mins}:${String(secs).padStart(2, "0")}`
    
    if (isOvertime) digitalClock.style.color = "red"
    else if (!isOvertime && mins === 0 && secs <= 20) digitalClock.style.color = "orange"
    else digitalClock.style.color = "lime"
})