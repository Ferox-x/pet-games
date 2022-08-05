from django.db import models

from users.models import Users


class SchulteModel(models.Model):
    user = models.ForeignKey(
        Users,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )

    record = models.CharField(
        max_length=10,
        verbose_name='Время',
    )

    date = models.DateTimeField(
        verbose_name='Время',
        auto_now=True,
        editable=False
    )

    class Meta:
        db_table = 'games_schulte'
        verbose_name = 'Schulte'


class StroopModel(models.Model):
    user = models.ForeignKey(
        Users,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )

    record = models.CharField(
        max_length=32,
        verbose_name='Результат'
    )

    score = models.CharField(
        max_length=32,
        verbose_name='Счет',
    )

    date = models.DateTimeField(
        verbose_name='Время',
        auto_now=True,
        editable=False
    )

    class Meta:
        db_table = 'games_stroop'
        verbose_name = 'Stroop'
