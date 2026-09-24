let dropdown = document.getElementById("dropdown")
let dropdownContent = document.getElementById("dropdown-content")
var dropdownContentShown = false

dropdown.onclick = () => {
    dropdownContentShown = !dropdownContentShown
    updateDropDownContentAppearance()
}

function updateDropDownContentAppearance() {
    if (dropdownContentShown) dropdownContent.style.display = "block"
    else dropdownContent.style.display = "none"
}