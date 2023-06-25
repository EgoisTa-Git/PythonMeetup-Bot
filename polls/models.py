import datetime
from django.db import models

from users.models import CustomUser


class Poll(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        verbose_name='пользователь',
        related_name='polls'
    )
    name = models.CharField(
        max_length=255,
        verbose_name='имя'
    )
    city = models.CharField(
        max_length=255,
        verbose_name='город'
    )
    job = models.CharField(
        max_length=255,
        verbose_name='работа'
    )
    stack = models.CharField(
        max_length=255,
        verbose_name='стек'
    )
    topics = models.TextField(
        verbose_name='темы'
    )
    about = models.TextField(
        verbose_name='о себе'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    modified = models.DateTimeField(
        auto_now=True,
        verbose_name='дата изменения'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='активна'
    )

    class Meta:
        verbose_name = 'анкета'
        verbose_name_plural = 'анкеты'

    def __str__(self):
        return f'Анкета N {self.id} ({self.user})'
