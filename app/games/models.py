from django.db import models

from core.models import CustomerUser


class SchulteModel(models.Model):
    user = models.ForeignKey(
        CustomerUser,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )

    records = models.CharField(
        max_length=10,
        verbose_name='Время',
    )
