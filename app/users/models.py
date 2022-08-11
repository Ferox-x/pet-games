from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.utils.translation import gettext_lazy as _


class MyUserManager(BaseUserManager):
    def create_user(self, username, country, password, **kwargs):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            country=country,
            password=password,
            **kwargs
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.model(
            username=username,
            password=password,
            **kwargs
        )

        user.is_superuser = True
        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        unique=True,
        max_length=50,
        verbose_name=_('Username')
    )
    country = CountryField(
        blank_label=_('select country'),
        verbose_name=_('Country')
    )
    description = models.CharField(
        max_length=256,
        verbose_name=_('Description'),
        blank=True,
        null=True
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_('Email adress')
    )
    full_name = models.CharField(
        max_length=150,
        verbose_name=_('Full name')
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['country', 'email', 'full_name']

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        db_table = 'Users'
