let dropdown = document.getElementById("dropdown")
let dropdownContent = document.getElementById("dropdown-content")
var dropdownContentShown = false

dropdown.onclick = () => {
    dropdownContentShown = !dropdownContentShown
    updateDropdownContent()
}

function updateDropdownContent() {
    if (dropdownContentShown) dropdownContent.style.display = "block"
    else dropdownContent.style.display = "none"
}