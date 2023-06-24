"""Менеджмент команда запуска бота"""

from django.conf import settings
from django.core.management import BaseCommand

from meetup_bot.tg_bot_main import TGBot, handle_role, start, handle_menu, show_menu

from meetup_bot.guests_chat import invite_to_chat, handle_chat_invite


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            tg_bot = TGBot(
                settings.TG_BOT_APIKEY,
                {
                    'START': start,
                    'HANDLE_ROLE': handle_role,
                    'SHOW_MENU': show_menu,
                    'HANDLE_MENU': handle_menu,
                    'CHAT_INVITE': invite_to_chat,
                    'HANDLE_INVITE': handle_chat_invite,
                }
            )
            tg_bot.updater.start_polling()
            tg_bot.updater.idle()
        except Exception as err:
            print(err)
