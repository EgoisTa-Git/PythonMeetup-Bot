"""Менеджмент команда запуска бота"""

from django.conf import settings
from django.core.management import BaseCommand

from meetup_bot.tg_bot_main import TGBot, handle_role, start, handle_menu


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            tg_bot = TGBot(
                settings.TG_BOT_APIKEY,
                {
                    'START': start,
                    'HANDLE_ROLE': handle_role,
                    'HANDLE_MENU': handle_menu,
                }
            )
            tg_bot.updater.start_polling()
            tg_bot.updater.idle()
        except Exception as err:
            print(err)
