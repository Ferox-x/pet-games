const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const mainDiv = document.getElementById('mainDiv')
const timerDiv = document.getElementById('timer')
const startButton = document.getElementById('schulte_start')
const recordsList = document.getElementById('recordsList')
const table = document.getElementById('table')

let pTimer = document.createElement('p')

let xhr = new XMLHttpRequest()


let arrayNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']
let counter = 1
let time = 0
let format_time = ''


window.addEventListener('keydown', (hotKey) => {

    if (hotKey.code === 'KeyR') {
        reloadGame()
    }
})

function timer() {
    time++
    let minutes, seconds, milSec
    milSec = time % 100
    seconds = ~~(time / 100) % 60
    minutes = ~~(time / 6000)
    if (seconds < 10) {
        seconds = '0' + String(seconds)
    }
    if (minutes < 10) {
        minutes = '0' + String(minutes)
    }
    if (milSec < 10) {
        milSec = '0' + String(milSec)
    }
    format_time = String(minutes) + ':' + String(seconds) + ':' + String(milSec)
    pTimer.innerHTML = format_time
}

function clearBoard() {
    arrayNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'];
    for (let i = 1; i <= 25; i++) {
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

function addingResultToLeaderboard(result) {
    let tableOfRecordsLi = recordsList.getElementsByTagName('li')
    let new_result = document.createElement('li')
    new_result.innerHTML = result
    new_result.className = 'stroop_r record'
    recordsList.prepend(new_result)

    if (tableOfRecordsLi.length > 20) {
        let last = recordsList[tableOfRecordsLi.length - 1]
        last.parentNode.removeChild(last)
    }
}

function sendData() {
    let formData = new FormData()
    formData.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest')
    formData.append('csrfmiddlewaretoken', csrftoken)
    formData.append('time', format_time)
    xhr.open("POST", "/games/schulte/")
    xhr.send(formData)

    addingResultToLeaderboard(format_time)
}

function achievementsBlock() {
    table.onclick = showHide;

    function showHide() {
        if (recordsList.style.display !== 'block') {
            recordsList.style.display = 'block'
        } else {
            recordsList.style.display = 'none'
        }
    }
}

function correctClick(event) {
    let divId = event.target.id
    let flag = correctQuery(divId)
    let selectedDiv = document.getElementById(divId)

    selectedDiv.addEventListener('animationend', function () {
        selectedDiv.classList.remove('schulte_shake')
    });

    if (flag === true) {
        selectedDiv.style.backgroundColor = 'rgb(216, 213, 213)'
        selectedDiv.style.color = 'rgb(216, 213, 213)'
        selectedDiv.classList.remove('schulte_shake')
    } else {
        selectedDiv.className = 'schulte_main_div__button schulte_shake'
    }

    if (counter === 25) {
        clearInterval(document.timer)
        clearBoard()
        schulteManager()
        sendData()
        counter = 1
        time = 0
    }

    function correctQuery(id) {
        if (Number(id) === counter) {
            counter++
            return true
        }
    }
}

function draw(flag = false) {

    function randomId() {
        let divId
        let index

        divId = Math.floor(Math.random() * 24) + 1
        index = arrayNumbers.indexOf(String(divId))

        while (index === -1) {
            divId = Math.floor(Math.random() * 24) + 1
            index = arrayNumbers.indexOf(String(divId))
        }

        arrayNumbers.splice(index, 1)
        return String(divId)
    }

    for (let i = 1; i <= 25; i++) {
        let elementDiv = document.createElement('div')

        if (i === 13) {
            elementDiv.innerHTML = '·'
            elementDiv.style.fontSize = '50px'
            elementDiv.id = '25'
        } else {
            if (flag === true) {
                let elementId = randomId()
                elementDiv.id = elementId
                elementDiv.style.fontSize = 50 + 'px'
                elementDiv.innerHTML = elementId
                elementDiv.onclick = correctClick
            } else {
                elementDiv.id = randomId();
                elementDiv.style.fontSize = 50 + 'px'
                elementDiv.innerHTML = '·'
            }
        }
        elementDiv.className = 'schulte_main_div__button'
        mainDiv.insertBefore(elementDiv, null)
    }
}

function startGame() {
    clearInterval(document.timer)
    clearBoard()
    draw(true)
    document.timer = setInterval(timer, 10)
}

function schulteManager() {
    achievementsBlock()
    startButton.onclick = reloadGame
    startButton.style.userSelect = 'none'
    pTimer.className = 'schulte_ptimer'
    timerDiv.insertBefore(pTimer, null)
    draw()
}

schulteManager()
