from django.db import models
from django.contrib.auth.models import AbstractUser
from letters.models import Letter


class User(AbstractUser):
    first_name = None
    last_name = None

    views = models.ManyToManyField(
        Letter, blank=True, related_name='letter_views', editable=False, verbose_name='недавние')
    saves = models.ManyToManyField(
        Letter, blank=True, related_name='letter_saves', editable=False, verbose_name='сохраненные')

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'
        ordering = ['-username']
