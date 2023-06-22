from django.db import models
from django.contrib.auth.models import AbstractUser


ROLES = [
        ('manager', 'менеджер'),
        ('guest', 'гость'),
        ('speaker', 'спикер'),
    ]


# Create your models here.
class Person(AbstractUser):
    role = models.CharField(
        'роль',
        max_length=30,
        choices=ROLES,
        default='guest',
        blank=True,
    )
    tg_id = models.IntegerField(
        'ID участника',
        null=True,
    )
    bot_state = models.IntegerField(
        'Статус бота',
        default=0,
        blank=True,
        help_text='номер стейта'
    )
    ready_to_chat = models.BooleanField(
        'Готовность общаться',
        default=False,
        db_index=True,
        help_text='Анкета заполнена?',
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
        help_text='Из какого города?',
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
        help_text='О чем хочешь пообщаться?',
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
        verbose_name = 'участник'
        verbose_name_plural = 'участники'

    def __str__(self):
        return self.username


class Event(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='название')
    description = models.TextField(
        verbose_name='описание')
    address = models.CharField(
        max_length=255,
        verbose_name='место проведения')
    start_date = models.DateTimeField(verbose_name='Начало')
    end_date = models.DateTimeField(verbose_name='Окончание')
    creator = models.ForeignKey(
        Person,
        verbose_name='организатор',
        on_delete=models.CASCADE)
    modified = models.DateTimeField(
        verbose_name='последние изменения',
        auto_now=True)

    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'

    def __str__(self):
        return f"{self.title} {self.start_date.year}"


class Report(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name='мероприятие',
        on_delete=models.CASCADE, related_name='reports')
    speaker = models.ForeignKey(
        Person,
        verbose_name='докладчик',
        on_delete=models.CASCADE, related_name='reports')
    topic = models.CharField(max_length=255, verbose_name='тема')
    started_at = models.DateTimeField(verbose_name='время начала')
    ended_at = models.DateTimeField(verbose_name='время окончания')
    modified = models.DateTimeField(verbose_name='последние изменения',auto_now=True)

    class Meta:
        verbose_name = 'доклад'
        verbose_name_plural = 'доклады'

    def __str__(self):
        return f'{self.topic} ({self.speaker})'


class Question(models.Model):
    content = models.CharField(max_length=255, verbose_name='вопрос')
    author = models.ForeignKey(
        Person,
        verbose_name='автор',
        on_delete=models.CASCADE
    )
    report = models.ForeignKey(
        Report,
        verbose_name='доклад',
        on_delete=models.DO_NOTHING,
        related_name='questions'
    )
    questioned_at = models.DateTimeField(verbose_name='дата')
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return f'{self.content}'


class Donation(models.Model):
    donor = models.ForeignKey(
        Person,
        verbose_name='спонсор',
        on_delete=models.DO_NOTHING,
        related_name='donations')
    amount = models.IntegerField(verbose_name='сумма', default=0)
    donation_date = models.DateField(verbose_name='дата перевода', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'чаевые'
        verbose_name_plural = 'чаевые'

    def __str__(self):
        return f'{self.donor} ({self.amount} руб.)'
