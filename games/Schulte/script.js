const mainDiv = document.getElementById('mainDiv')
const timerDiv = document.getElementById('timer')
const  startButton = document.getElementById('schulte_start')
let pTimer = document.createElement('p')

let arrayNumbers =  ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'];
let counter = 1
let time = 0

window.addEventListener('keydown', (hotKey) => {
    console.log(hotKey.code)
    if (hotKey.code === 'KeyR') {
        reloadGame()
    }
})

function timer() {
    time++
    let minutes, seconds, milSec = 0
    milSec = time % 100
    seconds = ~~(time/100) % 60
    minutes = ~~(time/6000)
    if (seconds < 10) {
        seconds = '0' + String(seconds)
    }
    if (minutes < 10) {
        minutes = '0' + String(minutes)
    }
    if (milSec < 10) {
        milSec = '0' + String(milSec)
    }
    pTimer.innerHTML = String(minutes) + ':' + String(seconds) + ':' +String(milSec)

}

function scaleGame(){
    let size = document.getElementById('slider').value;
    mainDiv.style.width = size + 'px';
    mainDiv.style.height = size + 'px';
    mainDiv.style.marginLeft = String((1350 - size) / 2) + 'px'
    for (let j = 1; j <= 25; j++) {
        if (j === 25) {
            document.getElementById(String(j)).style.fontSize = size * 0.1 + 'px';
        }
        else {
            document.getElementById(String(j)).style.fontSize = size * 0.075 + 'px';
        }
    }
}


function clearBoard() {
    arrayNumbers = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'];
    for (let i = 1; i <=25; i++) {
        let child = document.getElementById(String(i))
        child.remove()
    }
}

function reloadGame() {
    clearInterval(document.timer)
    startGame()
    counter = 1
    time = 0
}

function sendData() {
    let formData = new FormData()
    formData.append('time', time)
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/games/schulte");
    xhr.send(formData);
}

function correctClick (event) {
    let divId = event.target.id
    let flag = correctQuery(divId)
    let selectedDiv = document.getElementById(divId);
    selectedDiv.addEventListener('animationend', function () {
        selectedDiv.classList.remove('shake')
    });

    if (flag === true) {
        selectedDiv.style.backgroundColor = '#ffc76c';
    }
    else {
        selectedDiv.className = 'main_div__button shake';
    }

    if (counter === 25) {
        clearInterval(document.timer)
        clearBoard()
        schulteManager()
        sendData()
    }

    function correctQuery (id) {
        if (Number(id) === counter ) {
            counter++
            return true
        }
    }
}

function draw(flag=false) {

    function randomId() {
        let divId;
        let index;

        divId = Math.floor(Math.random() * 24) + 1;
        index = arrayNumbers.indexOf(String(divId));

        while (index === -1) {
            divId = Math.floor(Math.random() * 24) + 1;
            index = arrayNumbers.indexOf(String(divId));
        }

        arrayNumbers.splice(index, 1);
        return String(divId);
    }
    let size = document.getElementById('slider').value;

    for (let i = 1; i <= 25; i++) {
        let elementDiv = document.createElement('div');

        if (i === 13) {
            elementDiv.innerHTML = '·';
            elementDiv.style.fontSize = '50px';
            elementDiv.id = '25';
        }
        else {
            if (flag === true) {
                let elementId = randomId()
                elementDiv.id = elementId;
                elementDiv.style.fontSize = size * 0.075 + 'px';
                elementDiv.innerHTML = elementId;
                elementDiv.onclick = correctClick;
            }
            else {
                elementDiv.id = randomId();
                elementDiv.style.fontSize = size * 0.075 + 'px';
                elementDiv.innerHTML = '·';
            }
        }
        elementDiv.className = 'main_div__button'
        mainDiv.insertBefore(elementDiv, null)
    }
}

function startGame () {
    clearInterval(document.timer)
    clearBoard()
    draw(true)
    document.timer = setInterval(timer, 10)
}

function schulteManager () {

    startButton.onclick = startGame
    startButton.style.userSelect = 'none'
    pTimer.className = 'ptimer'
    timerDiv.insertBefore(pTimer, null)
    draw()
}

schulteManager()