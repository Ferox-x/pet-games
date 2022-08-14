from django.shortcuts import render
from django.views import View

from services.code_database import Support


def is_ajax(post):
    if post.get('ajax'):
        return True
    return False


class SupportView(View):
    """Отображение для службы поддержки"""

    def get(self, request):
        chats = Support(request.user, request.POST).get_chats()

        context = {
            'chats': chats
        }

        return render(request, 'support/support.html', context)

    def post(self, request):
        if is_ajax:
            Support(request.user, request.POST).create_ticket_or_add_message()

