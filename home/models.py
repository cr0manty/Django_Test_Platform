from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='', null=True,
                              height_field=None, width_field=None,
                              blank=True)

    @property
    def is_editor(self):
        for group in self.groups.all():
            if group.name == 'Editor':
                return True

    def save(self, *args, **kwargs):
        if not self.check_password(self.password):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def switch_to_user(self):
        self.groups.remove(Group.objects.get(name='Editor'))
        self.groups.add(Group.objects.get(name='User'))

    class Meta:
        ordering = ['-username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
