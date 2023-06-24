"""Менеджмент команда запуска бота"""
from django.conf import settings
from django.core.management import BaseCommand

from meetup_bot.tg_bot_main import TGBot, handle_menu
from meetup_bot.services import start, handle_role, handle_message, write_speaker_from_schedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            tg_bot = TGBot(
                settings.TG_BOT_APIKEY,
                {
                    'START': start,
                    'HANDLE_ROLE': handle_role,
                    'HANDLE_MENU': handle_menu,
                    'HANDLE_MESSAGE': handle_message,
                    'WRITE_SPEAKER_FROM_SCHEDULE': write_speaker_from_schedule,
                }
            )
            tg_bot.updater.start_polling()
            tg_bot.updater.idle()
        except Exception as err:
            print(err)
