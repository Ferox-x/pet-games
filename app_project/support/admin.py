from django.contrib import admin

from support.models import Chat, SupportTicket


class SupportTicketAdminModel(admin.ModelAdmin):
    """Админ панель для тикета"""
    list_display = ['user', 'header', 'date', 'status']


class ChatModelAdmin(admin.ModelAdmin):
    """Админ панель для чата"""
    list_display = ['ticket', 'message', 'date', 'user']


admin.site.register(SupportTicket, SupportTicketAdminModel)
admin.site.register(Chat, ChatModelAdmin)
