# Generated by Django 4.2.2 on 2023-06-25 12:48

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='вопрос')),
                ('published', models.DateTimeField(default=datetime.datetime(2023, 6, 25, 16, 48, 35, 756003), verbose_name='дата публикации')),
                ('is_active', models.BooleanField(verbose_name='опубликован')),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'вопросы',
            },
        ),
        migrations.CreateModel(
            name='PollAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255, verbose_name='ответ')),
                ('votes', models.IntegerField(default=0, verbose_name='голосов')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='polls.pollquestion', verbose_name='вопрос')),
            ],
            options={
                'verbose_name': 'ответ',
                'verbose_name_plural': 'ответы',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='название')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('is_active', models.BooleanField(default=True, verbose_name='активно')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='polls', to='events.event', verbose_name='мероприятие')),
                ('question', models.ManyToManyField(related_name='polls', to='polls.pollquestion', verbose_name='вопрос')),
            ],
            options={
                'verbose_name': 'анкета',
                'verbose_name_plural': 'анкеты',
            },
        ),
    ]
