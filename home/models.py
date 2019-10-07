from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    birth_date = models.DateField(blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='', null=True,
                              height_field=None, width_field=None,
                              blank=True, default='user-default.png')

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     birth_date = models.DateField(blank=True, null=True)
#     about = models.TextField(blank=True, null=True)
#     image = models.ImageField(upload_to='', null=True,
#                               height_field=None, width_field=None,
#                               blank=True, default='user-default.png')


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
