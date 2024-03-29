const timerBlock = document.getElementById('timerBlock')
const sliderBlock = document.getElementById('sliderBlock')
const wordBlock = document.getElementById('wordBlock')
const colorElemBlock = document.getElementById('colorElemBlock')
const startBlock = document.getElementById('startBlock')
const scoreBlock = document.getElementById('scoreBlock')


const table = document.getElementById('table')
const recordsList = document.getElementById('recordsList')

const language = document.querySelector('[name=LANGUAGE_CODE]').value

let colorsNames = ['Yellow', 'Red', 'Green', 'Blue', 'Black']

if (language === 'ru') {
    colorsNames = ['Жёлтый', 'Красный', 'Зелёный', 'Синий', 'Чёрный']
}

const colorsTypes = [
    'rgba(250, 212, 15, 0.5)',
    'rgba(255, 0, 0, 0.5)',
    'rgba(66, 255, 0, 0.47)',
    'rgba(0, 133, 255, 0.5)',
    'rgba(0, 0, 0, 0.5)'
]

let sliderValue = 0
let totalCounter = 0
let correctCounter = 0
let incorrectCounter = 0
let prevColorName = undefined
let score = 0
let streak = 0
let timer = 0

window.addEventListener('keydown', (hotkey) => {
    const hotkeys = {
        'KeyQ': '1',
        'KeyW': '2',
        'KeyE': '3',
        'KeyR': '4',
        'KeyT': '5'
    };
    if (hotkey.code in hotkeys) {
        document.getElementById(hotkeys[hotkey.code]).click();
    }
})

function addingResultToLeaderboard(result) {
    let recordListLi = recordsList.getElementsByTagName('li')
    let new_result = document.createElement('li')
    new_result.innerHTML = result + '<b class="stroop_score">'+ score + '</b>'
    new_result.className = 'stroop_r record'
    new_result.id = 'record'
    recordsList.prepend(new_result)

    if (recordListLi.length > 20) {
        let last = recordListLi[recordListLi.length - 1]
        last.parentNode.removeChild(last)
    }
}

function sendData(data, score) {
    const csrftoken = document.querySelector(
        '[name=csrfmiddlewaretoken]'
    ).value

    let xhr = new XMLHttpRequest()
    let formData = new FormData()
    formData.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest')
    formData.append('csrfmiddlewaretoken', csrftoken)
    formData.append('record', data)
    formData.append('score', score)

    xhr.open("POST", "/games/stroop/")
    xhr.send(formData)

    addingResultToLeaderboard(data)
}

function formatResult(total, correct, incorrect) {
    return total + '-' + correct + '-' + incorrect
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

function spanColor(total, correct, incorrect) {
    return (
        '<span style="color: rgba(0, 0, 0, 0.7)">' + String(total) + '</span>' +
        '<span style="opacity: 0.5">' + ' - ' + '</span>' +
        '<span style="color: rgba(66, 255, 0, 0.7)">' + String(correct) + '</span>' +
        '<span style="opacity: 0.5">' + ' - ' + '</span>' +
        '<span style="color: rgba(255, 0, 0, 0.7)">' + String(incorrect) + '</span>'
    )
}

function colorsGenerator() {
    function randomElement(array) {
        return array[Math.floor(Math.random() * array.length)]
    }

    let colorName = randomElement(colorsNames)
    let colorType = randomElement(colorsTypes)

    do {
        colorName = randomElement(colorsNames)
    } while (colorName === prevColorName)
    return [colorType, colorName]
}

function wordColorGenerator(colorType, colorName) {
    let wordColor = document.createElement('p')
    wordColor.innerHTML = colorName
    wordColor.style.color = colorType
    wordColor.className = 'stroop_word-color'
    wordColor.id = 'wordColor'
    wordBlock.appendChild(wordColor)
    prevColorName = colorName
    document.recordTimer = setInterval(scoreTimer, 10)

}

function scoreTimer(){
    timer++
}

function clickColorBlock(event) {
    const colorTypeName = {
        'rgba(250, 212, 15, 0.5)': colorsNames[0],
        'rgba(255, 0, 0, 0.5)': colorsNames[1],
        'rgba(66, 255, 0, 0.47)': colorsNames[2],
        'rgba(0, 133, 255, 0.5)': colorsNames[3],
        'rgba(0, 0, 0, 0.5)': colorsNames[4],
    }

    let colorNameText = document.getElementById(
        'wordColor'
    ).textContent
    let selectedBlockElem = document.getElementById(event.target.id)

    let colorBlockElem = colorTypeName[selectedBlockElem.style.backgroundColor]

    clearInterval(document.recordTimer)
    if (colorBlockElem === colorNameText) {
        correctCounter++
        streak++
        timer = timer/100
        let between_coef = correctCounter / (incorrectCounter * 5)
        if (between_coef === Infinity) {
            between_coef = correctCounter / (5)
        }
        if (timer < 5) {
            score = score + 5 * (5 - timer) * streak * between_coef
        }
        timer = 0
    } else {
        incorrectCounter++
        streak = 0
    }

    totalCounter++

    document.getElementById('counter').innerHTML = spanColor(
        totalCounter,
        correctCounter,
        incorrectCounter
    )
    document.getElementById('wordColor').remove()
    wordColorGenerator(colorsGenerator()[0], colorsGenerator()[1])
}

function timerSetting() {
    let value = document.getElementById('slider').value
    let timer = document.getElementById('timer')
    timer.innerHTML = String(value) + ' seconds'
}

function timerDisplay() {
    let time = document.getElementById('time')

    if (time.innerHTML > 0) {
        time.innerHTML--
    } else {
        time.remove()
        document.getElementById('timerCircle').remove()
        timerBlock.className = 'stroop_timer-block'
        startBlock.style.display = 'flex'
        sliderBlock.style.display = 'flex'
        for (let j = 1; j <= 5; j++) {
            let colorBlock = document.getElementById(String(j))
            colorBlock.remove()
        }

        document.getElementById('wordColor').remove()
        counter.remove()
        clearInterval(document.interval)
        mainMenu()
    }
}

function mainMenu() {
    achievementsBlock()
    score = Math.floor(score)

    if (sliderValue === 60) {
        let result = formatResult(
            totalCounter,
            correctCounter,
            incorrectCounter
        )
        sendData(result, score)
    } else if (incorrectCounter + correctCounter + totalCounter !== 0) {
        let result = formatResult(
            totalCounter,
            correctCounter,
            incorrectCounter
        )
        addingResultToLeaderboard(result)
    }

    score = 0
    incorrectCounter = 0
    correctCounter = 0
    totalCounter = 0

    wordBlock.style.display = 'none'
    scoreBlock.style.display = 'none'

    let timer = document.createElement('p')
    timer.id = 'timer'
    timer.className = 'stroop_timer'
    timer.style.userSelect = 'none'
    timer.innerHTML = '60 seconds'
    timerBlock.appendChild(timer)

    let slider = document.createElement('input')
    slider.id = 'slider'
    slider.className = 'stroop_slider'
    slider.type = 'range'
    slider.min = '10'
    slider.max = '120'
    slider.step = '10'
    slider.value = '60'
    slider.oninput = timerSetting
    sliderBlock.appendChild(slider)

    for (let j = 1; j <= 5; j++) {
        let colorBlock = document.createElement('div')
        colorBlock.id = String(j)
        colorBlock.className = 'stroop_color_block'
        colorBlock.style.backgroundColor = colorsTypes[j - 1]
        colorElemBlock.appendChild(colorBlock)
    }

    let startGame = document.createElement('a')
    startGame.id = 'startGame'
    startGame.className = 'stroop_start_game btn_animation'
    startGame.innerHTML = 'START'
    startGame.style.userSelect = 'none'
    startBlock.appendChild(startGame)
    startGame.onclick = mainGame
}

function mainGame() {

    let timerCircle = document.createElement('div')
    timerCircle.id = 'timerCircle'
    timerCircle.className = 'stroop_timer-circle'
    timerBlock.appendChild(timerCircle)
    timerBlock.className = 'stroop_timer-block-game'

    let counter = document.createElement('counter')
    counter.id = 'counter'
    counter.className = 'stroop_counter'
    counter.innerHTML = spanColor(totalCounter, correctCounter, incorrectCounter)
    scoreBlock.appendChild(counter)


    let time = document.createElement('p')
    time.id = 'time'
    time.className = 'stroop_timer-game'
    time.innerHTML = document.getElementById('slider').value
    timerCircle.appendChild(time)

    wordColorGenerator(colorsGenerator()[0], colorsGenerator()[1])
    for (let j = 1; j <= 5; j++) {
        document.getElementById(String(j)).onclick = clickColorBlock
    }

    sliderValue = Number(document.getElementById('slider').value)
    document.interval = setInterval(timerDisplay, 1000)

    document.getElementById('timer').remove()
    document.getElementById('slider').remove()
    document.getElementById('startGame').remove()

    startBlock.style.display = 'none'
    sliderBlock.style.display = 'none'
    wordBlock.style.display = 'flex'
    scoreBlock.style.display = 'flex'

}

mainMenu()
