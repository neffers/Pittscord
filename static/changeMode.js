// declaring lightMode variable and retreiving value from local storage
let lightMode = localStorage.getItem("lightMode")

function enableFromStart() {
    if (lightMode === "enabled") enableLight()
}

// no return, change the colors of the ui - from a darker color pallete, to a lighter color pallete (or reverse)
function changeMode() {
    console.log("changeMode()")
    lightMode = localStorage.getItem('lightMode')
    if (lightMode === 'enabled') {
        enableDark()
    } else {
        enableLight()
    }
}

// helper function for changeMode(), changing the colors to light ones and storing in local sorage
function enableLight() {
    document.body.classList.add('lightMode')
    localStorage.setItem('lightMode', 'enabled')
}

// helper function for changeMode(), changing the colors to dark ones and storing in local sorage
function enableDark() {
    document.body.classList.remove('lightMode')
    localStorage.setItem('lightMode', null)
}

function onLoginLoad() {
    document.getElementById('modeBtn').addEventListener('click', changeMode)
    enableFromStart()
}

addEventListener("DOMContentLoaded", onLoginLoad)