var i = 0;
var text = '🤬 Twitter Hate Speech Detector 📊'
var speed = 50;

function typeWriter() {
    if (i < text.length) {
        document.getElementById("effectText").innerHTML += text.charAt(i);
        i++;
        setTimeout(typeWriter, speed);
    }
}