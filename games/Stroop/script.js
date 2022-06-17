const headerBlock = document.getElementById('headerBlock');
const mainBlock = document.getElementById('mainBlock');
const mainBlockWord = document.getElementById('mainBlockWord');
const mainBlockGame = document.getElementById('mainBlockGame');
const mainBlockTwo = document.getElementById('mainBlockTwo');
const footerBlock = document.getElementById('footerBlock');

const arrayColorsName = ['Blue', 'Black', 'Green', 'Red', 'Yellow'];
const arrayColors = ['blue', 'black', 'green', 'red', 'yellow'];

let prevColorName = undefined
let correctCounter = 0
let incorrectCounter = 0
let totalCounter = 0

function randomColor(array) {
    let colorName =  Math.floor(Math.random() * array.length)
    return arrayColorsName[colorName]
}

function correctClick(event) {
    const colorDict = {
        'blue': 'Blue',
        'black': 'Black',
        'green': 'Green',
        'red': 'Red',
        'yellow': 'Yellow'
    }
    let colorNameP = document.getElementById('block__p')
    let colorNameText = colorNameP.textContent
    let divId = event.target.id
    let selectedDiv = document.getElementById(divId);
    let color = selectedDiv.style.backgroundColor
    let result = colorDict[color]
    if (result === colorNameText) {
        correctCounter++
    } else {
        incorrectCounter++
    }
    colorNameP.remove()
    let listColor = generateColors()
    createElementP(listColor[0], listColor[1])
    totalCounter++

    counter = document.getElementById('counter')
    counter.innerHTML = String(totalCounter) +
                        ' : ' + String(correctCounter) +
                        ' : ' + String(incorrectCounter)
}

function generateColors() {
    let currentColorName = randomColor(arrayColorsName)
    let currentColor = randomColor(arrayColors)

    do {
        currentColorName = randomColor(arrayColorsName)
    } while (currentColorName === prevColorName)
    return [currentColor, currentColorName]
}

function createElementP(currentColor, currentColorName) {
    let colorNameP = document.createElement('p')
    colorNameP.innerHTML = currentColorName
    colorNameP.style.color = currentColor
    colorNameP.className = 'world-block__p'
    colorNameP.id = 'block__p'
    mainBlockWord.appendChild(colorNameP)
    prevColorName = currentColorName
}

function draw() {
    for (let j=1; j<=5; j++) {
        let elementDiv = document.createElement('div')
        elementDiv.id = String(j)
        elementDiv.className = 'color-block__elem'
        elementDiv.style.backgroundColor = arrayColors[j-1]
        mainBlockGame.appendChild(elementDiv)
    }
}

function NoticeTimeChange() {
    let value = document.getElementById('slider').value
    let timeNotice = document.getElementById('time_notice_p')
    timeNotice.innerHTML = 'Период: ' + String(value) + ' секунд'
    headerBlock.appendChild(timeNotice)
}

function startGame() {
    let slider = document.createElement('input')
    slider.className = 'slider'
    slider.id = 'slider'
    slider.type = 'range'
    slider.min = '10'
    slider.max = '120'
    slider.step = '10'
    slider.value = '60'
    slider.oninput = NoticeTimeChange
    mainBlock.appendChild(slider)

    let startButton = document.createElement('a')
    startButton.innerHTML = 'Старт'
    startButton.style.userSelect = 'none'
    startButton.className = 'start_game__a'
    startButton.id = 'start_game__a'
    mainBlockTwo.appendChild(startButton)

    let timeNotice = document.createElement('p')
    timeNotice.id = 'time_notice_p'
    timeNotice.innerHTML = 'Период: ' + String(slider.value) + ' секунд'
    headerBlock.appendChild(timeNotice)

    let description = document.createElement('p')
    description.innerHTML = 'Условия: Необходимо нажать на кнопку' +
        ' того цвета, который описывает слово'
    description.id = 'description'
    footerBlock.appendChild(description)

    draw()
    startButton.onclick = startGameClick
}



function startGameClick() {
    let counter = document.createElement('counter')
    counter.id = 'counter'
    footerBlock.appendChild(counter)

    function timer(){
    let time = document.getElementById('time')
    let word = document.getElementById('block__p')

    if(time.innerHTML > 0){
        time.innerHTML--
    } else {
        time.remove()
        for (let j = 1; j <= 5; j++) {
            let elementDiv = document.getElementById(String(j))
        elementDiv.remove()
        }
        word.remove()
        counter.remove()
        incorrectCounter = 0
        correctCounter = 0
        totalCounter = 0
        clearInterval(interval)
        startGame()
        }
    }

    let listColor = generateColors()

    let value = document.getElementById('slider').value
    let time = document.createElement('p')
    time.id = 'time'
    time.innerHTML = value
    headerBlock.appendChild(time)
    let interval = setInterval(timer, 1000)

    createElementP(listColor[0], listColor[1])
    for (let j=1; j<=5; j++) {
        document.getElementById(String(j)).onclick = correctClick;
    }

    let timeNotice = document.getElementById('time_notice_p')
    let startButton = document.getElementById('start_game__a')
    let slider = document.getElementById('slider')
    let description = document.getElementById('description')
    timeNotice.remove()
    slider.remove()
    startButton.remove()
    description.remove()
}

startGame()