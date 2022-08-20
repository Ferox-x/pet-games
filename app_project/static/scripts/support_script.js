const supportButton = document.getElementById('support_button')
const supportNewTicket = document.getElementById('support_new_ticket')
const supportChat = document.getElementById('support_chat')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const imageUrl = document.querySelector('[name=image_url]').value
const formMessage = document.getElementById('formMessage')
const sendData1 = document.getElementById('senddata')
const textArea = document.getElementById('textarea_message')
const supportHistoryMessages = document.getElementById('support_history_messages')
const currentUrl = document.location.pathname
let prevChat = -1
let currentTicketStatus = undefined

sendData1.addEventListener('click', () => {
    let xhr = new XMLHttpRequest()
    let formData = new FormData(formMessage)
    if (formData.get('chat_message') !== '') {
        formData.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest')
        formData.append('ticket_id', prevChat.id)
        console.log(currentUrl)
        if (currentTicketStatus === 'OP' && currentUrl === '/support/staff/') {
            changeStatus('IP')
        }
        xhr.open('POST', currentUrl)
        xhr.send(formData)
        textArea.value = ''
        xhr.onreadystatechange = function () {
            if (this.readyState === 4 && this.status === 200) {
                const jsonMessage = JSON.parse(this.responseText)
                addMessageToChat(jsonMessage.username, jsonMessage.date, jsonMessage.message)
                supportHistoryMessages.scrollTop = supportHistoryMessages.scrollHeight - supportHistoryMessages.clientHeight;
            }
        }
    }

})

function getIdOnClick(ticketId, status) {
    let xhr = new XMLHttpRequest()
    let selectedTicket = document.getElementById(ticketId);
    if (prevChat !== -1) {
        prevChat.style.backgroundColor = '#fff'
    }
    prevChat = selectedTicket
    selectedTicket.style.backgroundColor = '#f3f7ff';
    let formDataNew = new FormData()
    formDataNew.append('csrfmiddlewaretoken', csrftoken);
    formDataNew.append('get_chat_from_ticket', 'True');
    formDataNew.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
    formDataNew.append('ticket_id', ticketId);
    xhr.open('POST', currentUrl);
    xhr.send(formDataNew);
    xhr.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const jsonMessage = JSON.parse(this.responseText)
            supportHistoryMessages.innerHTML = ''
            showChat()
            currentTicketStatus = status
            console.log(jsonMessage)
            addHeaderToChat(jsonMessage.ticket.header, jsonMessage.ticket.date, jsonMessage.ticket.first_message, jsonMessage.ticket.user__image.url)
            for (let index = 0, len = jsonMessage.len; index < len; ++index) {
                addMessageToChat(jsonMessage[index].user__username, jsonMessage[index].date, jsonMessage[index].message, jsonMessage[index].user__image);
            }
            supportHistoryMessages.scrollTop = supportHistoryMessages.scrollHeight - supportHistoryMessages.clientHeight;
        }
    }
    if (status === 'CL') {
        blockMessageInput()
    }
    else {
        displayMessageInput()
    }
    changeButtonChat()
}

function blockMessageInput() {
    let inputMessage = document.getElementById('input_message_chat')
    let ticketClosedMessage = document.getElementById('ticket_closed_message')
    inputMessage.style.display = 'none'
    ticketClosedMessage.style.display = 'flex'
}

function displayMessageInput() {
    let inputMessage = document.getElementById('input_message_chat')
    let ticketClosedMessage = document.getElementById('ticket_closed_message')
    inputMessage.style.display = 'inherit'
    ticketClosedMessage.style.display = 'none'
}

function changeStatus(status) {
    let xhr = new XMLHttpRequest()
    let formDataNew = new FormData()
    formDataNew.append('csrfmiddlewaretoken', csrftoken);
    formDataNew.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
    formDataNew.append('change_status', 'status')
    formDataNew.append('status', status)
    formDataNew.append('ticket_id', prevChat.id)
    xhr.open('POST', '/support/staff/')
    xhr.send(formDataNew)
}

function addMessageToChat(username, date, message, image) {
    console.log(image)
    if (image === undefined){
        image = imageUrl
    }
    let htmlCodeMessage = '<div class="support_chat_message">\n' +
        '            <img src="/media/' + image + '" alt="" class="support_avatar_ticket">\n' +
        '            <div class="support_chat_message_info">\n' +
        '              <div class="support_chat_username_and_date">\n' +
        '                <div class="support_chat_username">' + username + '</div>\n' +
        '                <div class="support_chat_message_date">' + date + '</div>\n' +
        '              </div>\n' +
        '              <div class="support_chat_message_text">' + message + '</div>\n' +
        '            </div>\n' +
        '          </div>'
    supportHistoryMessages.insertAdjacentHTML('beforeend', htmlCodeMessage)
}

function addHeaderToChat(header, date, message) {
    let htmlCodeMessage = '<div class="support_chat_message">\n' +
        '            <div class="support_chat_message_info">\n' +
        '              <div class="support_chat_username_and_date">\n' +
        '                <div class="support_chat_username"><b>' + header + '</b></div>\n' +
        '                <div class="support_chat_message_date">' + date + '</div>\n' +
        '              </div>\n' +
        '              <div class="support_chat_message_text">' + message + '</div>\n' +
        '            </div>\n' +
        '          </div>'
    supportHistoryMessages.insertAdjacentHTML('beforeend', htmlCodeMessage)
}

supportButton.addEventListener('click', () => {
    switch (supportButton.innerHTML) {
        case 'New ticket':
            changeButtonTicket()
            showCreateTicket()
            break
        case 'Chats':
            changeButtonChat()
            showChat()
            break
    }
})

function changeButtonTicket() {
    supportButton.innerHTML = 'Chats'
    supportButton.style.backgroundColor = 'white'
    supportButton.style.color = '#14213D'
}

function changeButtonChat() {
    supportButton.innerHTML = 'New ticket'
    supportButton.style.backgroundColor = '#14213D'
    supportButton.style.color = 'white'
}

function showChat() {
    supportNewTicket.style.display = 'none'
    supportChat.style.display = 'inherit'
    supportHistoryMessages.scrollTop = supportHistoryMessages.scrollHeight - supportHistoryMessages.clientHeight;
}

function showCreateTicket() {
    supportNewTicket.style.display = 'inherit'
    supportChat.style.display = 'none'
}
