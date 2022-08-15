from django.shortcuts import render
from django.views import View

from services.code_database import Support
from services.services import is_ajax
from support.forms import CreateTicketForm, ChatMessageForm


class SupportView(View):
    """Отображение для службы поддержки."""

    def get(self, request):
        # chats = Support(request.user, request.POST).get_chats()
        # ticket_form = CreateTicketForm()
        # chat_form = ChatMessageForm()
        # context = {
        #     'chats': chats,
        #     'ticket_form': ticket_form,
        #     'chat_form': chat_form
        # }

        return render(request, 'support/support.html', {})

    def post(self, request):
        if request.user.is_authenticated and is_ajax(request):
            Support(request.user, request.POST).create_ticket_or_add_message()
