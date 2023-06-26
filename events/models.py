from django.db import models
from users.models import CustomUser


class Event(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='название')
    description = models.TextField(
        verbose_name='описание')
    address = models.CharField(
        max_length=255,
        verbose_name='место проведения')
    creator = models.ForeignKey(
        CustomUser,
        verbose_name='организатор',
        on_delete=models.CASCADE,
        related_name='events'
    )
    guests = models.ManyToManyField(
        CustomUser,
        verbose_name='участники',
        related_name='meetups'
    )
    start_date = models.DateTimeField(verbose_name='Начало')
    end_date = models.DateTimeField(verbose_name='Окончание')
    modified = models.DateTimeField(
        verbose_name='последние изменения',
        auto_now=True)

    class Meta:
        verbose_name = 'мероприятие'
        verbose_name_plural = 'мероприятия'
        ordering = ('start_date',)

    def __str__(self):
        return f"{self.title} {self.start_date.year}"


class Report(models.Model):
    event = models.ForeignKey(
        Event,
        verbose_name='мероприятие',
        on_delete=models.CASCADE, related_name='reports')
    speaker = models.ForeignKey(
        CustomUser,
        verbose_name='докладчик',
        on_delete=models.CASCADE,
        related_name='reports')
    topic = models.CharField(max_length=255, verbose_name='тема')
    started_at = models.DateTimeField(verbose_name='время начала')
    ended_at = models.DateTimeField(verbose_name='время окончания')
    modified = models.DateTimeField(verbose_name='последние изменения',auto_now=True)

    class Meta:
        verbose_name = 'доклад'
        verbose_name_plural = 'доклады'
        ordering = ('started_at',)

    def __str__(self):
        return f'{self.topic} ({self.speaker})'


class GuestQuestion(models.Model):
    content = models.CharField(max_length=255, verbose_name='вопрос')
    author = models.ForeignKey(
        CustomUser,
        verbose_name='автор',
        on_delete=models.CASCADE
    )
    report = models.ForeignKey(
        Report,
        verbose_name='доклад',
        on_delete=models.DO_NOTHING,
        related_name='questions'
    )
    questioned_at = models.DateTimeField(
        auto_now_add=True, verbose_name='дата')
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return f'{self.content}'


class Donation(models.Model):
    donor = models.ForeignKey(
        CustomUser,
        verbose_name='спонсор',
        on_delete=models.CASCADE,
        related_name='donations')
    amount = models.IntegerField(verbose_name='сумма', default=0)
    donation_date = models.DateField(verbose_name='дата перевода', auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'чаевые'
        verbose_name_plural = 'чаевые'

    def __str__(self):
        return f'{self.donor} ({self.amount} руб.)'
