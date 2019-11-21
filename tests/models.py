from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from slugify import slugify_url
from time import time

User = get_user_model()


class Test(models.Model):
    name = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(max_length=128, blank=True, unique=True)
    author = models.ForeignKey(User, related_name='tests', on_delete=models.CASCADE)
    passes_number = models.IntegerField(default=0)
    description = models.CharField(max_length=256, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('test_show', kwargs={'slug': self.slug})

    def get_comment_add_url(self):
        return reverse('add_comment_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = (slugify_url(self.name) + '-' + str(int(time())))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    question = models.CharField(max_length=256, blank=False, null=False)
    answers = models.CharField(max_length=256, blank=False, null=False)
    correct = models.CharField(max_length=64, blank=False, null=False)
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.question, self.answers)


class Comment(models.Model):
    test = models.ForeignKey(Test, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.PROTECT)
    date_create = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return '{}: {}'.format(self.author.username, self.text)

    class Meta:
        ordering = ['-date_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Коментарии'


class UserTestPass(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    test = models.ForeignKey(Test, on_delete=models.PROTECT)
    correct_answer = models.IntegerField()
    amount_answer = models.IntegerField()
    correct_present = models.IntegerField()
