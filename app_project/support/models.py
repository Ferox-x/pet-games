from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Users

TICKET_STATUS = [
    ('OP', 'Open'),
    ('IP', 'In Progress'),
    ('CL', 'Closed')
]


class SupportTicket(models.Model):
    """Модель тикета для службы поддержки."""

    user = models.ForeignKey(Users, verbose_name=_('User'),
                             on_delete=models.CASCADE)
    header = models.CharField(max_length=64, verbose_name=_('Header'))
    date = models.DateTimeField(auto_now_add=True, editable=False,
                                verbose_name=_('Date'))
    status = models.CharField(verbose_name=_('Status'), choices=TICKET_STATUS,
                              default='OP', max_length=2)
    first_message = models.TextField(verbose_name='First message')

    class Meta:
        db_table = 'tickets'
        verbose_name = _('Ticket')

    @property
    def short_header(self):
        return self.header[:15] + '...'

    def __str__(self):
        return self.header


class Chat(models.Model):
    """Модель чата для определённого тикета."""

    ticket = models.ForeignKey(SupportTicket, verbose_name=_('Ticket'),
                               on_delete=models.CASCADE)
    message = models.TextField(verbose_name=_('Message'))
    date = models.DateTimeField(verbose_name=_('Date'), auto_now_add=True,
                                editable=False)
    user = models.ForeignKey(Users, verbose_name=_('User'),
                             on_delete=models.CASCADE)

    class Meta:
        db_table = 'chat'
        verbose_name = _('Chat')
