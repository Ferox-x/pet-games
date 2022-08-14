from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import Users


class SchulteModel(models.Model):
    """Модель обработки результатов пользователя в игре Schulte."""
    user = models.ForeignKey(Users, verbose_name=_('User'),
                             on_delete=models.CASCADE)

    record = models.IntegerField(verbose_name=_('Record Time'), )

    date = models.DateTimeField(verbose_name=_('Time'), auto_now=True,
                                editable=False)

    class Meta:
        db_table = 'games_schulte'
        verbose_name = _('Schulte')


class StroopModel(models.Model):
    """Модель обработки результатов пользователя в игре Stroop."""

    user = models.ForeignKey(Users, verbose_name=_('User'),
                             on_delete=models.CASCADE)

    record = models.CharField(max_length=32, verbose_name=_('Record'))

    score = models.IntegerField(verbose_name=_('Score'))

    date = models.DateTimeField(verbose_name=_('Time'), auto_now=True,
                                editable=False)

    class Meta:
        db_table = 'games_stroop'
        verbose_name = _('Stroop')
