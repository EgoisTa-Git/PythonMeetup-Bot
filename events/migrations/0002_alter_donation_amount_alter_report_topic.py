# Generated by Django 4.2.1 on 2023-06-22 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='report',
            name='topic',
            field=models.CharField(max_length=255, verbose_name='тема'),
        ),
    ]
