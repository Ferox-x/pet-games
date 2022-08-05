from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django_countries.fields import CountryField


class MyUserManager(BaseUserManager):
    def create_user(self, username, country, password):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username,
            country=country,
            password=password
        )

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.model(
            username=username,
            password=password
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
        verbose_name='Username'
    )
    country = CountryField(
        blank_label='Select Country',
        verbose_name='Country'
    )
    description = models.CharField(
        max_length=256,
        verbose_name='Description',
        blank=True,
        null=True
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email adress',
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='First Name',
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Last Name',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'username'

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'Users'
