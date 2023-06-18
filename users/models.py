from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = [
    ('manager', 'Менеджер'),
    ('guest', 'Гость'),
    ('speaker', 'Спикер'),
]


class CustomUser(AbstractUser):
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLES,
        blank=True,
    )
    tg_id = models.IntegerField(
        'ID в Telegram',
        null=True,
    )
    bot_state = models.IntegerField(
        'Текущее состояния бота',
        default=0,
        blank=True,
        help_text="Номер стейта"
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
