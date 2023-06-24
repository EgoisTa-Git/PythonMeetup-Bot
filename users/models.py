from django.db import models
from django.contrib.auth.models import AbstractUser

from polls.models import Poll


ROLES = [
        ('manager', 'менеджер'),
        ('guest', 'гость'),
        ('speaker', 'спикер'),
]


class CustomUser(AbstractUser):
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLES,
        blank=True,
    )
    tg_id = models.IntegerField(
        'ID участника',
        null=True,
    )
    bot_state = models.CharField(
        'Текущее состояние бота',
        max_length=50,
        blank=True,
        help_text='Стейт машина'
    )
    is_subscriber = models.BooleanField(
        verbose_name='подписчик',
        default=False
    )
    polls = models.ManyToManyField(
        Poll,
        verbose_name='опросы',
        related_name='users'
    )

    class Meta:
        verbose_name = 'участник'
        verbose_name_plural = 'участники'

    def __str__(self):
        return self.username
