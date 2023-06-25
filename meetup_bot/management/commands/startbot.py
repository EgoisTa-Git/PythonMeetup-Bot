"""Менеджмент команда запуска бота"""

from django.core.management import BaseCommand

from meetup_bot.tg_bot_main import bot


class Command(BaseCommand):
    def handle(self, *args, **options):
        bot()
