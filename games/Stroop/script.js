const colorName = document.getElementById('wordBlock');


let arrayColorsName = ['Blue', 'Black', 'Green', 'Red', 'Yellow'];
let arrayColors = ['blue', 'black', 'green', 'red', 'yellow'];

function randomColorName() {
    let colorName =  Math.floor(Math.random() * arrayColors.length);
    return arrayColorsName[colorName]
}

function randomColor() {
    let colorType = Math.floor(Math.random() * arrayColors.length);
    return arrayColorsName[colorType]

}

function draw() {
    let colorNameDiv = document.createElement('p')
    colorNameDiv.innerHTML = randomColorName();
    colorNameDiv.style.color = randomColor();
    colorNameDiv.className = 'world-block__p'
    colorName.appendChild(colorNameDiv)
}
draw()

