console.log('idleTimeout.js')
var idle;
function idleTimeout() {
    window.onload = resetTimer;
    window.onmousemove = resetTimer;
    window.onmousedown = resetTimer;
    window.ontouchstart = resetTimer;
    window.ontouchmove = resetTimer;
    window.onclick = resetTimer;
    window.onkeydown = resetTimer;
    window.addEventListener('scroll', resetTimer, true);
}

function redirect() {
    window.location.href = "http://localhost:8000/advertising";
}

function resetTimer() {
    clearTimeout(idle);
    idle = setTimeout(redirect, (60 * 10 * 1000));
}
idleTimeout();