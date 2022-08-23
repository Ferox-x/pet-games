let gameContainer = document.getElementById('gameContainer')
let rulesContainer = document.getElementById('rulesContainer')
let playButton = document.getElementById('rulesPlayBtn')


playButton.addEventListener('click', () => {
    rulesContainer.style.display = 'none'
    gameContainer.style.display = 'flex'
})
