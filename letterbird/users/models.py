from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from letters.models import Letter


class User(AbstractUser):
    first_name = None
    last_name = None

    username = models.CharField(
        _('username'),
        max_length=18,
        unique=True,
        help_text=_('Required. 18 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    recently = models.ManyToManyField(
        Letter, blank=True, related_name='letter_views', editable=True, verbose_name='просмотренные')
    saves = models.ManyToManyField(
        Letter, blank=True, related_name='letter_saves', editable=True, verbose_name='сохраненные')

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['-date_joined']
