let dropdown = document.getElementById("dropdown")
let dropdownContent = document.getElementById("dropdown-content")
let userPassForm = document.getElementById("user-pass-form")
let adminPassForm = document.getElementById("admin-pass-form")
let changePassBtn = document.getElementById("change-passwords-btn")
var dropdownContentShown = false
var passFormShown = false

dropdown.onclick = () => {
    dropdownContentShown = !dropdownContentShown
    updateDropdownContent()
}

changePassBtn.onclick = () => {
    passFormShown = !passFormShown
    if (passFormShown) {
        userPassForm.style.display = "flex"
        adminPassForm.style.display = "flex"
    } else {
        userPassForm.style.display = "none"
        adminPassForm.style.display = "none"
    }
}


function updateDropdownContent() {
    if (dropdownContentShown) dropdownContent.style.display = "block"
    else dropdownContent.style.display = "none"
}