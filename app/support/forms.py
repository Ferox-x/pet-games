from django import forms


class CreateTicketForm(forms.Form):
    """Форма создания тикета, и первого к нему сообщения."""
    header = forms.CharField(max_length=32)
    chat_message = forms.Textarea()


class ChatMessageForm(forms.Form):
    """Форма сообщения к тикету."""
    chat_message = forms.Textarea()
