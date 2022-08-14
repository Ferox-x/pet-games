from django import forms


class CreateTicketForm(forms.Form):
    header = forms.CharField(max_length=32)
    chat_message = forms.Textarea()


class ChatMessageForm(forms.Form):
    chat_message = forms.Textarea()
