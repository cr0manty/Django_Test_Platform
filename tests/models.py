from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from slugify import slugify_url
from time import time


class Question(models.Model):
    question = models.CharField(max_length=64)
    answers = models.CharField(max_length=256)
    correct = models.IntegerField()


class Test(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    questions = models.ManyToManyField('Question', related_name='test')
    passes_number = models.IntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('test_show', kwargs={'slug': self.slug})

    def get_comment_add_url(self):
        return reverse('add_comment_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = (slugify_url(self.name) + '-' + str(int(time())))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Comment(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'
