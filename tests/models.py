from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from slugify import slugify_url
from time import time


class Test(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    passes_number = models.IntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('test_show', kwargs={'slug': self.slug})

    def get_comment_add_url(self):
        return reverse('add_comment_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = (slugify_url(self.name) + '-' + str(int(time())))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    question = models.CharField(max_length=256, blank=False, null=False)
    answers = models.CharField(max_length=256, blank=False, null=False)
    correct = models.CharField(max_length=64, blank=False, null=False)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)


class Comment(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'


class UserTestPass(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    test = models.OneToOneField(Test, on_delete=models.CASCADE)
    correct_answer = models.IntegerField(default=0)
    amount_answer = models.IntegerField(default=0)
    correct_present = models.IntegerField(default=0)
