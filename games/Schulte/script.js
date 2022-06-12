const mainDiv = document.getElementById('mainDiv');

let arrayNumbers =  ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'];
let counter = 1


window.addEventListener('keydown', (hotKey) => {
    console.log(hotKey.code)
    if (hotKey.code === 'KeyR') {
        reloadGame()
    }
})


function scaleGame(){
    let size = document.getElementById('slider').value;
    document.getElementById('mainDiv').style.width = size + 'px';
    document.getElementById('mainDiv').style.height = size + 'px';

    for (let j = 1; j <= 25; j++) {
        if (j === 25) {
            document.getElementById(String(j)).style.fontSize = size * 0.1 + 'px';
        }
        else {
            document.getElementById(String(j)).style.fontSize = size * 0.075 + 'px';
        }
    }
}

function reloadGame() {
    for (let i = 1; i <=25; i++){
            let child = document.getElementById(String(i))
            child.remove()
        }
        arrayNumbers = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'];
        counter = 1
        draw()
}

function correctClick (event) {
    let divId = event.target.id
    let flag = correctQuery(divId)
    let selectedDiv = document.getElementById(divId);
    selectedDiv.addEventListener('animationend', function () {
        selectedDiv.classList.remove('shake')
    });

    if (flag === true) {
        selectedDiv.style.backgroundColor = '#6b6b6b17';
    }
    else {
        selectedDiv.className = 'main_div__button shake';
    }

    if (counter === 25) {
        reloadGame()
    }

    function correctQuery (id) {
        if (Number(id) === counter ) {
            counter++
            return true
        }
    }
}

function draw() {
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

    for (let i = 1; i <= 5; i++) {
        for (let j = 1; j <= 5; j++) {
            let elementDiv = document.createElement('div');

            if (i === 3 && j === 3) {
                elementDiv.innerHTML = '·';
                elementDiv.style.fontSize = '50px';
                elementDiv.id = '25';
            }
            else {

                let elementId = randomId();
                elementDiv.id = elementId;
                elementDiv.style.fontSize = size * 0.075 + 'px';
                elementDiv.innerHTML = elementId;
                elementDiv.onclick = correctClick;
            }
            elementDiv.className = 'main_div__button'
            mainDiv.insertBefore(elementDiv, null)
        }
    }
}

draw()