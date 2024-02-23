function setup() {
    document.getElementById("theButton").addEventListener("click", sendPost);
}

function sendPost() {
    fetch("/post", { method: "post" });
}

window.addEventListener("load", setup);