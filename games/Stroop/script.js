const colorName = document.getElementById('wordBlock');
const arrayColorsName = ['Blue', 'Black', 'Green', 'Red', 'Yellow'];
const arrayColors = ['blue', 'black', 'green', 'red', 'yellow'];

let prevColorName = undefined
let correctCounter = 0
let totalCounter = 0

function randomColor(array) {
    let colorName =  Math.floor(Math.random() * array.length);
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
    }
    colorNameP.remove()
    let listColor = generateColors()
    createElementP(listColor[0], listColor[1])
    totalCounter++
    console.log(totalCounter, correctCounter)
}

function generateColors() {
    let currentColorName = randomColor(arrayColorsName);
    let currentColor = randomColor(arrayColors);

    do {
        currentColorName = randomColor(arrayColorsName);
    } while (currentColorName === prevColorName)
    return [currentColor, currentColorName]
}

function createElementP(currentColor, currentColorName) {

    let colorNameP = document.createElement('p')
    colorNameP.innerHTML = currentColorName
    colorNameP.style.color = currentColor
    colorNameP.className = 'world-block__p'
    colorNameP.id = 'block__p'
    colorName.appendChild(colorNameP)
    prevColorName = currentColorName
}

function draw() {
    let listColor = generateColors()
    createElementP(listColor[0], listColor[1])

    for (let j=1; j<=5; j++) {
        document.getElementById(String(j)).onclick = correctClick;
    }
}
draw()
