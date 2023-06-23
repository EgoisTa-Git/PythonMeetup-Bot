"""Менеджмент команда запуска бота"""

from django.conf import settings
from django.core.management import BaseCommand

from meetup_bot import bot
from meetup_bot.tg_bot_main import TGBot


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            tg_bot = TGBot(
                settings.TG_BOT_APIKEY,
                {
                    'START': bot.start,
                    'HANDLE_MESSAGE': bot.handle_message,
                    'HANDLE_BUTTONS': bot.handle_buttons,

                }
            )
            tg_bot.updater.start_polling()
            tg_bot.updater.idle()
        except Exception as err:
            print(err)
