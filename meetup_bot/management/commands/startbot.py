"""Менеджмент команда запуска бота"""
import logging
from django.conf import settings
from django.core.management import BaseCommand

from meetup_bot.tg_bot_main import TGBot, handle_menu
from meetup_bot.services import start, handle_role, handle_donate, handle_message, write_speaker_from_schedule, \
    start_poll, handle_poll_answer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_format = logging.Formatter(
    fmt='{asctime} - {levelname} - {name} - {message}',
    style='{')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
logger.addHandler(stream_handler)


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
                    'START_POLL': start_poll,
                    'HANDLE_POLL_ANSWER': handle_poll_answer,
                    'HANDLE_DONATE': handle_donate
                }
            )
            tg_bot.updater.start_polling()
            tg_bot.updater.idle()
        except Exception as err:
            logger.error(err, exc_info=True)
