# Generated by Django 4.2.2 on 2023-06-26 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='сумма')),
                ('donation_date', models.DateField(auto_now_add=True, verbose_name='дата перевода')),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'чаевые',
                'verbose_name_plural': 'чаевые',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='название')),
                ('description', models.TextField(verbose_name='описание')),
                ('address', models.CharField(max_length=255, verbose_name='место проведения')),
                ('start_date', models.DateTimeField(verbose_name='Начало')),
                ('end_date', models.DateTimeField(verbose_name='Окончание')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='последние изменения')),
            ],
            options={
                'verbose_name': 'мероприятие',
                'verbose_name_plural': 'мероприятия',
                'ordering': ('start_date',),
            },
        ),
        migrations.CreateModel(
            name='GuestQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255, verbose_name='вопрос')),
                ('questioned_at', models.DateTimeField(auto_now_add=True, verbose_name='дата')),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'вопросы',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=255, verbose_name='тема')),
                ('started_at', models.DateTimeField(verbose_name='время начала')),
                ('ended_at', models.DateTimeField(verbose_name='время окончания')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='последние изменения')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='events.event', verbose_name='мероприятие')),
            ],
            options={
                'verbose_name': 'доклад',
                'verbose_name_plural': 'доклады',
                'ordering': ('started_at',),
            },
        ),
    ]
