console.log("file found")
// declaring lightMode variable and retreiving value from local storage
export let lightMode = localStorage.getItem("lightMode")
console.log("lightmode gotten")

export function enableFromStart() {
    if (lightMode === "enabled") enableLight()
}

// no return, change the colors of the ui - from a darker color pallete, to a lighter color pallete (or reverse)
export function changeMode() {
    console.log("changeMode()")
    lightMode = localStorage.getItem('lightMode')
    if (lightMode === 'enabled') {
        enableDark()
    } else {
        enableLight()
    }
}

// helper function for changeMode(), changing the colors to light ones and storing in local sorage
export function enableLight() {
    document.body.classList.add('lightMode')
    localStorage.setItem('lightMode', 'enabled')
}

// helper function for changeMode(), changing the colors to dark ones and storing in local sorage
export function enableDark() {
    document.body.classList.remove('lightMode')
    localStorage.setItem('lightMode', null)
}

export function onLoginLoad() {
    document.getElementById('modeBtn').addEventListener('click', changeMode)
    enableFromStart()
}

addEventListener("DOMContentLoaded", onLoginLoad)

//export {lightMode, onLoginLoad, enableFromStart, changeMode, enableLight, enableDark};