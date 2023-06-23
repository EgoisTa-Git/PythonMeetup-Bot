import datetime
from django.db import models


class PollQuestion(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='вопрос')
    published = models.DateTimeField(
        verbose_name='дата публикации',
        default=datetime.datetime.now())
    is_active = models.BooleanField(
        verbose_name='опубликован')

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return self.title


class PollAnswer(models.Model):
    question = models.ForeignKey(
        PollQuestion,
        verbose_name='вопрос',
        on_delete=models.CASCADE,
        related_name='answers')
    answer = models.CharField(
        max_length=255,
        verbose_name='ответ')
    votes = models.IntegerField(
        verbose_name='голосов',
        default=0)

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def __str__(self):
        return self.answer


class Poll(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='название',
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        verbose_name='мероприятие',
        related_name='polls'
    )
    question = models.ManyToManyField(
        PollQuestion,
        verbose_name='вопрос',
        related_name='polls'
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
        verbose_name='активно'
    )

    class Meta:
        verbose_name = 'анкета'
        verbose_name_plural = 'анкеты'

    def __str__(self):
        return  f'Анкета "{self.title}" ({self.event})'
