const headerBlock = document.getElementById('headerBlock');
const mainBlock = document.getElementById('mainBlock');
const mainBlockWord = document.getElementById('mainBlockWord');
const mainBlockGame = document.getElementById('mainBlockGame');
const mainBlockTwo = document.getElementById('mainBlockTwo');
const footerBlock = document.getElementById('footerBlock');

const colorsNames = ['Blue', 'Black', 'Green', 'Red', 'Yellow'];
const colorsTypes = ['blue', 'black', 'green', 'red', 'yellow'];

let prevColorName = undefined;
let correctCounter = 0;
let incorrectCounter = 0;
let totalCounter = 0;

function colorsGenerator() {
    function randomElement(array) {
        return colorsNames[Math.floor(Math.random() * array.length)];
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
    wordColor.className = 'word-color';
    wordColor.id = 'wordColor';
    mainBlockWord.appendChild(wordColor);
    prevColorName = colorName;
}

function timerSetting() {
    let value = document.getElementById('slider').value;
    let timer = document.getElementById('timer');
    timer.innerHTML = String(value) + ' seconds';
    headerBlock.appendChild(timer);
}

function clickColorBlock(event) {
    const colorTypeName = {
        'blue': 'Blue',
        'black': 'Black',
        'green': 'Green',
        'red': 'Red',
        'yellow': 'Yellow',
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
    document.getElementById('counter').innerHTML = String(totalCounter) +':' + String(correctCounter)+':' + String(incorrectCounter);
    document.getElementById('wordColor').remove();
    wordColorGenerator(colorsGenerator()[0], colorsGenerator()[1]);
}

function mainMenu() {
    let timer = document.createElement('p');
    timer.id = 'timer';
    timer.className = 'timer';
    timer.style.userSelect = 'none';
    timer.innerHTML = '60 seconds';
    headerBlock.appendChild(timer);

    let slider = document.createElement('input');
    slider.id = 'slider';
    slider.className = 'slider';
    slider.type = 'range';
    slider.min = '10';
    slider.max = '120';
    slider.step = '10';
    slider.value = '60';
    slider.oninput = timerSetting;
    mainBlock.appendChild(slider);

    for (let j=1; j<=5; j++) {
        let colorBlock = document.createElement('div');
        colorBlock.id = String(j);
        colorBlock.className = 'color_block';
        colorBlock.style.backgroundColor = colorsTypes[j-1];
        mainBlockGame.appendChild(colorBlock);
    }

    let startGame = document.createElement('a');
    startGame.id = 'startGame';
    startGame.className = 'start_game';
    startGame.innerHTML = 'Start';
    startGame.style.userSelect = 'none';
    mainBlockTwo.appendChild(startGame);
    startGame.onclick = mainGame;

    let description = document.createElement('p');
    description.id = 'description';
    description.className = 'description';
    description.innerHTML = 'You must click on the button of the color that describes the word.';
    description.style.userSelect = 'none';
    footerBlock.appendChild(description);
}

function mainGame() {
    let counter = document.createElement('counter')
    counter.id = 'counter'
    counter.className = 'counter'
    counter.innerHTML = '0:0:0'
    footerBlock.appendChild(counter)

    let time = document.createElement('p')
    time.id = 'time'
    time.innerHTML = document.getElementById('slider').value
    headerBlock.appendChild(time)

    wordColorGenerator(colorsGenerator()[0], colorsGenerator()[1])
    for (let j=1; j<=5; j++) {
        document.getElementById(String(j)).onclick = clickColorBlock;
    }

    document.getElementById('timer').remove()
    document.getElementById('slider').remove()
    document.getElementById('startGame').remove()
    document.getElementById('description').remove()

    let interval = setInterval(timerDisplay, 1000)

    function timerDisplay(){
        let time = document.getElementById('time')

        if(time.innerHTML > 0){
            time.innerHTML--
        } else {
            time.remove()
            for (let j = 1; j <= 5; j++) {
                let colorBlock = document.getElementById(String(j))
            colorBlock.remove()
            }
            document.getElementById('wordColor').remove()
            counter.remove()
            incorrectCounter = 0
            correctCounter = 0
            totalCounter = 0
            clearInterval(interval)
            mainMenu()
        }
    }
}

mainMenu()