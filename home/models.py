from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='', null=True,
                              height_field=None, width_field=None,
                              blank=True, default='user-default.png')

    class Meta:
        ordering = ['-username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
