const supportButton = document.getElementById('support_button')
const supportNewTicket = document.getElementById('support_new_ticket')
const supportChat = document.getElementById('support_chat')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
const formMessage = document.getElementById('formMessage')
const sendData1 = document.getElementById('senddata')
const textArea = document.getElementById('textarea_message')
const supportHistoryMessages = document.getElementById('support_history_messages')
const currentUrl = document.location.pathname
const supportButtonTickets = document.getElementById('support_button_tickets')
const supportRight = document.getElementById('support-right')
const supportTickets = document.getElementById('support-tickets')
const mediaQuery800 = window.matchMedia("(max-width: 800px)")

let prevChat = -1
let currentTicketStatus = undefined
let lastMessageInChat = 0
let checkMessagesTimer

sendData1.addEventListener('click', () => {
    let xhr = new XMLHttpRequest()
    let formData = new FormData(formMessage)
    if (formData.get('chat_message') !== '') {
        let jsonMessage = {
            'ticket_id': prevChat.id,
            'chat_message': formData.get('chat_message')
        }
        if (currentTicketStatus === 'OP' && currentUrl === '/support/staff/') {
            changeStatus('IP')
        }
        let messageChatForm = new FormData()
        messageChatForm.append('csrfmiddlewaretoken', csrftoken)
        messageChatForm.append('add_message_to_chat', 'true')
        messageChatForm.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest')
        messageChatForm.append('json_message', JSON.stringify(jsonMessage))
        xhr.open('POST', currentUrl)
        xhr.send(messageChatForm)
        textArea.value = ''
    }

})

function getIdOnClick(ticketId, status) {
    if (checkMessagesTimer) {
        clearInterval(checkMessagesTimer)
    }
    let xhr = new XMLHttpRequest()
    let selectedTicket = document.getElementById(ticketId);
    if (prevChat !== -1) {
        prevChat.style.backgroundColor = '#fff'
    }
    prevChat = selectedTicket
    selectedTicket.style.backgroundColor = '#f3f7ff';
    let getTicketChatForm = new FormData()
    let jsonMessage = {
        'ticket_id': ticketId
    }
    getTicketChatForm.append('csrfmiddlewaretoken', csrftoken);
    getTicketChatForm.append('get_chat_from_ticket', 'True');
    getTicketChatForm.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
    getTicketChatForm.append('ticket_id', ticketId);
    getTicketChatForm.append('json_message', JSON.stringify(jsonMessage))
    xhr.open('POST', currentUrl);
    xhr.send(getTicketChatForm);
    xhr.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const jsonMessage = JSON.parse(this.responseText)
            supportHistoryMessages.innerHTML = ''
            showChat()
            currentTicketStatus = status
            addHeaderToChat(jsonMessage.ticket.header, jsonMessage.ticket.date, jsonMessage.ticket.first_message)
            for (let index = 0, len = jsonMessage.len; index < len; ++index) {
                addMessageToChat(
                    jsonMessage[index].user__username,
                    jsonMessage[index].date,
                    jsonMessage[index].message,
                    jsonMessage[index].user__image,
                );
                lastMessageInChat = jsonMessage[index].id
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
    checkMessagesTimer = setInterval(checkMessages, 10000)
    if (mediaQuery800) {
        supportButtonTickets.style.display = 'flex'
        supportRight.style.display = 'block'
        supportTickets.style.display = 'none'
        supportRight.style.flexBasis = '100%'
    }
}

function checkMessages() {
    let xhr = new XMLHttpRequest()
    let checkMessagesForm = new FormData()
    let jsonMessage = {
        'ticket_id': prevChat.id,
        'last_message_id': lastMessageInChat
    }
    console.log(jsonMessage)
    checkMessagesForm.append('csrfmiddlewaretoken', csrftoken);
    checkMessagesForm.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
    checkMessagesForm.append('update_chat', 'True');
    checkMessagesForm.append('json_message', JSON.stringify(jsonMessage))
    xhr.open('POST', currentUrl)
    xhr.send(checkMessagesForm)
    xhr.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            const jsonMessage = JSON.parse(this.responseText)
            console.log(jsonMessage)
            for (let index = 0, len = jsonMessage.len; index < len; ++index) {
                addMessageToChat(
                    jsonMessage[index].user__username,
                    jsonMessage[index].date,
                    jsonMessage[index].message,
                    jsonMessage[index].user__image,
                );
                lastMessageInChat = jsonMessage[index].id
            }
            supportHistoryMessages.scrollTop = supportHistoryMessages.scrollHeight - supportHistoryMessages.clientHeight;
        }
    }
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
    let changeStatusForm = new FormData()
    let jsonMessage = {
        'ticket_id': prevChat.id,
        'status': status
    }
    changeStatusForm.append('csrfmiddlewaretoken', csrftoken);
    changeStatusForm.append('HTTP_X_REQUESTED_WITH', 'XMLHttpRequest');
    changeStatusForm.append('change_status', 'status')
    changeStatusForm.append('json_message', JSON.stringify(jsonMessage))
    xhr.open('POST', '/support/staff/')
    xhr.send(changeStatusForm)
}

function addMessageToChat(username, date, message, image) {

    let htmlCodeMessage = '<div class="support-chat__message">\n' +
        '            <img src="/media/' + image + '" alt="" class="support-tickets__avatar">\n' +
        '            <div class="support-chat__message-info">\n' +
        '              <div class="support-chat__username-and-date">\n' +
        '                <div class="support-chat__username">' + username + '</div>\n' +
        '                <div class="support-chat__message-date">' + date + '</div>\n' +
        '              </div>\n' +
        '              <div class="support-chat__message-text">' + message + '</div>\n' +
        '            </div>\n' +
        '          </div>'
    supportHistoryMessages.insertAdjacentHTML('beforeend', htmlCodeMessage)
}

function addHeaderToChat(header, date, message) {
    let htmlCodeMessage = '<div class="support-chat__message">\n' +
        '            <div class="support-chat__message-info">\n' +
        '              <div class="support-chat__username-and-date">\n' +
        '                <div class="support-chat__username"><b>' + header + '</b></div>\n' +
        '                <div class="support-chat__message-date">' + date + '</div>\n' +
        '              </div>\n' +
        '              <div class="support-chat__message-text">' + message + '</div>\n' +
        '            </div>\n' +
        '          </div>'
    supportHistoryMessages.insertAdjacentHTML('beforeend', htmlCodeMessage)
}

if (currentUrl === '/support/') {
    supportButton.addEventListener('click', () => {

        switch (supportButton.innerHTML) {
            case 'New ticket':
                changeButtonTicket()
                showCreateTicket()
                if (mediaQuery800) {
                    supportButtonTickets.style.display = 'flex'
                    supportRight.style.display = 'block'
                    supportTickets.style.display = 'none'
                    supportRight.style.flexBasis = '100%'
                }
                break
            case 'Chats':
                changeButtonChat()
                showChat()
                break
        }

    })
}

function changeButtonTicket() {
    if (currentUrl === '/support/') {
        supportButton.innerHTML = 'Chats'
        supportButton.style.backgroundColor = 'white'
        supportButton.style.color = '#14213D'
    }
}

function changeButtonChat() {
    if (currentUrl === '/support/') {
        supportButton.innerHTML = 'New ticket'
        supportButton.style.backgroundColor = '#14213D'
        supportButton.style.color = 'white'
    }
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

supportButtonTickets.addEventListener('click', () => {
    if (mediaQuery800) {
        supportButtonTickets.style.display = 'none'
        supportRight.style.display = 'none'
        supportTickets.style.display = 'block'
        supportTickets.style.flexBasis = '100%'
        changeButtonChat()
    }
})

