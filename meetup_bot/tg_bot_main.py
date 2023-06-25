"""Основной модуль бота"""
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from users.models import CustomUser
from meetup_bot.services import start, invite_to_chat, ask_question, handle_speaker, donate, handle_donate, handle_schedule, \
    handle_speaker_from_schedule, write_speaker_from_schedule, not_meet, start_poll, handle_poll_answer


class TGBot(object):
    """Описывает работу бота"""

    def __init__(self, tg_token, states_functions):
        self.tg_token = tg_token
        self.states_functions = states_functions
        self.updater = Updater(token=self.tg_token, use_context=True)
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.get_user(self.handle_users_reply)))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.get_user(self.handle_users_reply)))
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start_command))

    def start_command(self, update, context):
        """Обработчик команды /start"""
        chat_id = update.message.chat_id
        username = update.message.from_user.username
        user, created = CustomUser.objects.get_or_create(tg_id=chat_id, defaults={'username': username})
        if created:
            user.is_active = False
            user.save()
        context.user_data['user'] = user
        self.handle_users_reply(update, context)

    def handle_users_reply(self, update, context):
        """Метод, который запускается при любом сообщении от пользователя и решает как его обработать"""
        user = context.user_data['user']
        if update.message:
            user_reply = update.message.text
            chat_id = update.message.chat_id
            username = update.message.from_user.username
        elif update.callback_query:
            user_reply = update.callback_query.data
            chat_id = update.callback_query.message.chat_id
            username = update.callback_query.message.from_user.username
        else:
            return

        user_state = user.bot_state if user.bot_state else 'START'
        context.user_data.update({'chat_id': chat_id, 'username': username})

        state_handler = self.states_functions[user_state]
        next_state = state_handler(context.bot, update, context)

        user.bot_state = next_state
        user.save()

    def get_user(self, func):
        """Получает пользователя из базы данных и передает его в дальнейшую функцию"""

        def wrapper(update, context):
            chat_id = context.user_data.get('chat_id')
            username = context.user_data.get('username')
            if not chat_id:
                chat_id = update.message.chat_id
                username = update.message.from_user.username
            user, created = CustomUser.objects.get_or_create(tg_id=chat_id, defaults={'username': username})
            if created:
                user.is_active = False
                user.save()
            context.user_data['user'] = user
            return func(update, context)

        return wrapper


def handle_menu(bot, update, context):
    """Обработчик для навигации в меню бота"""
    user = context.user_data['user']
    chat_id = context.user_data['chat_id']
    menu_selected = update.callback_query.data

    menu_options = {
        'meet': invite_to_chat,
        'question': ask_question,
        'donate': donate,
        'handle_donate': handle_donate,
        'back': start,
        'write_speaker': handle_speaker,
        'schedule': handle_schedule,
        'write_speaker_from_schedule': handle_speaker_from_schedule,
        'not_meet': not_meet,
        'start_poll': start_poll,
        'handle_poll_answer': handle_poll_answer
    }

    if menu_selected.startswith('write_') and menu_selected.split('_')[1].isdigit():
        write_speaker_from_schedule(bot, update, context)
    elif menu_selected in menu_options:
        new_bot_state = menu_options[menu_selected](bot, update, context)
        return new_bot_state
    else:
        return 'HANDLE_MENU'
