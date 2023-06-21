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
    bot_state = models.CharField(
        'Текущее состояния бота',
        max_length=50,
        blank=True,
        help_text='Стейт машина'
    )
    ready_to_chat = models.BooleanField(
        'Готовность общаться',
        default=False,
        db_index=True,
        help_text='Заполнена ли анкета?',
    )
    real_name = models.CharField(
        'Имя',
        max_length=50,
        blank=True,
        help_text='Как к тебе могут обращаться другие участники?',
    )
    city = models.CharField(
        'Город',
        max_length=50,
        blank=True,
        help_text='Из какого ты города?',
    )
    work_place = models.CharField(
        'Место работы и должность',
        max_length=100,
        blank=True,
        help_text='Где и кем ты работаешь?',
    )
    stack = models.CharField(
        'Стек технологий',
        max_length=150,
        blank=True,
        help_text='Твой стек. Какие технологии используешь в работе?',
    )
    topics = models.CharField(
        'Предпочитаемые темы для общения',
        max_length=150,
        blank=True,
        help_text='О чем бы ты хотел пообщаться?',
    )
    about_me = models.CharField(
        'Информация о пользователе',
        max_length=250,
        blank=True,
        help_text='Расскажи ещё немного о себе (хобби, пет-проекты и т.д.)',
    )
    publish_date = models.DateTimeField(
        'Дата и время публикации анкеты',
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
