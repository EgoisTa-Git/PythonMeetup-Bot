# Generated by Django 4.2.2 on 2023-06-23 13:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poll',
            name='question',
        ),
        migrations.AlterField(
            model_name='pollquestion',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 23, 16, 18, 36, 512946), verbose_name='дата публикации'),
        ),
        migrations.AddField(
            model_name='poll',
            name='question',
            field=models.ManyToManyField(related_name='polls', to='polls.pollquestion', verbose_name='вопрос'),
        ),
    ]
