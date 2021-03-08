from django.db import models
from django.conf import settings


class Letter(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True, verbose_name='автор')
    message = models.TextField(max_length=3000, verbose_name='письмо')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='дата')
    views = models.IntegerField(default=0, editable=False, verbose_name='просмотров')
    saves = models.IntegerField(default=0, editable=False, verbose_name='сохранений')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'
        ordering = ['-datetime', '-author']
