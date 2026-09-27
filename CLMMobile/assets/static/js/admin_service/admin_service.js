let dropdown = document.getElementById("dropdown")
let passwordsContainer = document.getElementById("passwords-container")
let revealPasswordsFormBtn = document.getElementById("change-passwords-btn")
let dropdownContent = document.getElementById("dropdown-content")
var dropdownContentShown = false
var passwordsFormsShown = false

dropdown.onclick = () => {
    dropdownContentShown = !dropdownContentShown
    updateDropDownContentAppearance()
}

revealPasswordsFormBtn.onclick = () => {
    passwordsFormsShown = !passwordsFormsShown
    updatePasswordsFormAppearance()
}

function updateDropDownContentAppearance() {
    if (dropdownContentShown) dropdownContent.style.display = "block"
    else dropdownContent.style.display = "none"
}

function updatePasswordsFormAppearance() {
    if (passwordsFormsShown) passwordsContainer.style.display = "block"
    else passwordsContainer.style.display = "none"
}