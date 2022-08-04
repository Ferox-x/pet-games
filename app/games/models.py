from django.db import models

from core.models import CustomerUser


class SchulteModel(models.Model):
    user = models.ForeignKey(
        CustomerUser, verbose_name='Пользователь', on_delete=models.CASCADE,
    )

    record = models.CharField(
        max_length=10, verbose_name='Время',
    )

    date = models.DateTimeField(
        verbose_name='Время', auto_now=True, editable=False
    )


class StroopModel(models.Model):
    user = models.ForeignKey(
        CustomerUser, verbose_name='Пользователь', on_delete=models.CASCADE,
    )

    result = models.CharField(
        max_length=32, verbose_name='Результат'
    )

    score = models.CharField(
        max_length=32, verbose_name='Время',
    )

    date = models.DateTimeField(
        verbose_name='Время', auto_now=True, editable=False
    )
