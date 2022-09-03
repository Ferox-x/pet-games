const menuIcon = document.querySelector('.menu__icon')
const menuBody = document.querySelector('.menu__body')
if (menuIcon){
    menuIcon.addEventListener('click', function(e){
        document.body.classList.toggle('_lock')
        menuIcon.classList.toggle('_active')
        menuBody.classList.toggle('_active')
    })
}
