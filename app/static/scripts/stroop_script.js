const timerBlock = document.getElementById('timerBlock');
const sliderBlock = document.getElementById('sliderBlock');
const wordBlock = document.getElementById('wordBlock');
const colorElemBlock = document.getElementById('colorElemBlock');
const startBlock = document.getElementById('startBlock');
const scoreBlock = document.getElementById('scoreBlock');

const table = document.getElementById('table')
const recordsList = document.getElementById('recordsList')

const colorsNames = ['Yellow', 'Red', 'Green', 'Blue', 'Black'];
const colorsTypes = [
    'rgba(250, 212, 15, 0.5)',
    'rgba(255, 0, 0, 0.5)',
    'rgba(66, 255, 0, 0.47)',
    'rgba(0, 133, 255, 0.5)',
    'rgba(0, 0, 0, 0.5)'
];

let sliderValue = 0;
let totalCounter = 0;
let correctCounter = 0;
let incorrectCounter = 0;
let prevColorName = undefined;

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
});

function sendData(data) {
    const csrftoken = document.querySelector(
        '[name=csrfmiddlewaretoken]'
    ).value;

    let xhr = new XMLHttpRequest();
    let formData = new FormData();
    formData.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
    formData.append('csrfmiddlewaretoken', csrftoken);
    formData.append('record', data);

    xhr.open("POST", "/games/stroop/");
    xhr.send(formData);

    let new_result = document.createElement('li')
    new_result.innerHTML = data
    new_result.className = 'stroop_r record'
    recordsList.prepend(new_result)

    if (recordsList.getElementsByTagName('li').length > 20) {
        document.getElementById('record').remove()
    }
}

function saveResult(total, correct, incorrect) {
    let formatRecord = total + ' - ' + correct + ' - ' + incorrect;
    sendData(formatRecord);
}

function achievementsBlock() {
    table.onclick = showHide;

    function showHide() {
        if (recordsList.style.display !== 'block') {
            recordsList.style.display = 'block';
        } else {
            recordsList.style.display = 'none';
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
        return array[Math.floor(Math.random() * array.length)];
    }

    let colorName = randomElement(colorsNames);
    let colorType = randomElement(colorsTypes);

    do {
        colorName = randomElement(colorsNames)
    } while (colorName === prevColorName);
    return [colorType, colorName];
}

function wordColorGenerator(colorType, colorName) {
    let wordColor = document.createElement('p');
    wordColor.innerHTML = colorName;
    wordColor.style.color = colorType;
    wordColor.className = 'stroop_word-color';
    wordColor.id = 'wordColor';
    wordBlock.appendChild(wordColor);
    prevColorName = colorName;
}

function clickColorBlock(event) {
    const colorTypeName = {
        'rgba(250, 212, 15, 0.5)': 'Yellow',
        'rgba(255, 0, 0, 0.5)': 'Red',
        'rgba(66, 255, 0, 0.47)': 'Green',
        'rgba(0, 133, 255, 0.5)': 'Blue',
        'rgba(0, 0, 0, 0.5)': 'Black',
    };

    let colorNameText = document.getElementById('wordColor').textContent;
    let selectedBlockElem = document.getElementById(event.target.id);
    let colorBlockElem = colorTypeName[selectedBlockElem.style.backgroundColor];

    if (colorBlockElem === colorNameText) {
        correctCounter++
    } else {
        incorrectCounter++
    }

    totalCounter++

    document.getElementById('counter').innerHTML = spanColor(totalCounter, correctCounter, incorrectCounter)
    document.getElementById('wordColor').remove();
    wordColorGenerator(colorsGenerator()[0], colorsGenerator()[1]);
}

function timerSetting() {
    let value = document.getElementById('slider').value;
    let timer = document.getElementById('timer');
    timer.innerHTML = String(value) + ' seconds';
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

    if (sliderValue === 60) {
        saveResult(totalCounter, correctCounter, incorrectCounter)
    }

    incorrectCounter = 0
    correctCounter = 0
    totalCounter = 0

    wordBlock.style.display = 'none'
    scoreBlock.style.display = 'none'

    let timer = document.createElement('p');
    timer.id = 'timer';
    timer.className = 'stroop_timer';
    timer.style.userSelect = 'none';
    timer.innerHTML = '60 seconds';
    timerBlock.appendChild(timer);

    let slider = document.createElement('input');
    slider.id = 'slider';
    slider.className = 'stroop_slider';
    slider.type = 'range';
    slider.min = '10';
    slider.max = '120';
    slider.step = '10';
    slider.value = '60';
    slider.oninput = timerSetting;
    sliderBlock.appendChild(slider);

    for (let j = 1; j <= 5; j++) {
        let colorBlock = document.createElement('div');
        colorBlock.id = String(j);
        colorBlock.className = 'stroop_color_block';
        colorBlock.style.backgroundColor = colorsTypes[j - 1];
        colorElemBlock.appendChild(colorBlock);
    }

    let startGame = document.createElement('a');
    startGame.id = 'startGame';
    startGame.className = 'stroop_start_game';
    startGame.innerHTML = 'START';
    startGame.style.userSelect = 'none';
    startBlock.appendChild(startGame);
    startGame.onclick = mainGame;
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
        document.getElementById(String(j)).onclick = clickColorBlock;
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
