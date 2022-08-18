const fileInput = document.getElementById('fileInput')
const imageForm = document.getElementById('imageForm')

const editOrSave = document.getElementById('editOrSave')
const textForm = document.getElementById('textForm')
const input = document.getElementsByClassName('display')
const div = document.getElementsByClassName('displ')

fileInput.addEventListener('change', () => {
    imageForm.submit()
})

let display = () => {
    for (let j = 0; j < input.length; j++) {
        input[j].style.display = 'inherit'
        div[j].style.display = 'none'

    }
}

editOrSave.addEventListener('click', () => {
    switch (editOrSave.innerHTML) {
        case 'Edit Profile':
            editOrSave.innerHTML = 'Save'
            editOrSave.style.backgroundColor = '#14213D'
            editOrSave.style.color = 'white'
            display()
            break
        case 'Save':
            editOrSave.innerHTML = 'Edit Profile'
            editOrSave.style.backgroundColor = 'white'
            editOrSave.style.color = '#14213D'
            textForm.submit()
            break
    }
})
