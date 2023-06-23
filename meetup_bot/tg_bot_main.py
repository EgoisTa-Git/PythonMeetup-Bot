"""Основной модуль бота"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from users.models import CustomUser


class TGBot(object):
    """Описывает работу бота"""

    def __init__(self, tg_token, states_functions):
        self.tg_token = tg_token
        self.states_functions = states_functions
        self.updater = Updater(token=self.tg_token, use_context=True)
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.get_user(self.handle_users_reply)))
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.get_user(self.handle_users_reply)))
        self.updater.dispatcher.add_handler(CommandHandler('start', self.get_user(self.handle_users_reply)))

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
        next_state = state_handler(update, context)
        user.bot_state = next_state
        user.save()

    def get_user(self, func):
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


def start_role(bot, update, context):
    """Метод вывода стартового диалога"""
    chat_id = update.message.chat_id
    user = context.user_data['user']
    if user.role in ['guest', 'speaker', 'manager']:
        return user.bot_state
    else:
        custom_keyboard = [
            [InlineKeyboardButton('Гость', callback_data='guest'),
             InlineKeyboardButton('Спикер', callback_data='speaker'), ]
        ]
        reply_markup = InlineKeyboardMarkup(custom_keyboard)

        update.message.reply_text(
            'Привет! Это PythonMeetupBot! Выберите свою роль.',
            reply_markup=reply_markup,
        )
        return 'HANDLE_ROLE'


def handle_role(bot, update, context):
    """Метод обработки выбора роли"""
    user = context.user_data['user']
    chat_id = context.user_data['chat_id']
    role_selected = update.callback_query.data
    welcome_message = 'Привет! Это PythonMeetupBot - чатбот, в котором  можно узнать расписание выступлений на нашем ' \
                      'митапе, а также задать вопрос спикеру во время его выступления. А еще здесь можно знакомиться ' \
                      'с другими участниками конференции и поддержать нас донатом!'
    keyboard = [
        [InlineKeyboardButton("Хочу познакомиться", callback_data='meet')],
        [InlineKeyboardButton("Хочу задать вопрос", callback_data='question')],
        [InlineKeyboardButton("Хочу задонатить", callback_data='donate')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if role_selected == 'guest':
        user.role = 'guest'
        user.is_active = True
        user.save()
    elif role_selected == 'speaker':
        user.role = 'speaker'
        user.save()
        bot.send_message(
            chat_id=chat_id,
            text='Для подтверждения регистрации в роли спикера напишите менеджеру @meetup.support',
        )
    else:
        return 'HANDLE_ROLE'
    message = context.bot.send_message(
        text=welcome_message,
        chat_id=update.effective_chat.id,
    )
    context.bot.edit_message_reply_markup(
        chat_id=message.chat_id,
        message_id=message.message_id,
        reply_markup=reply_markup,
    )
    query = update.callback_query
    if query:
        context.bot.delete_message(
            query.message.chat_id,
            query.message.message_id,
        )
    return 'HANDLE_MENU'


def handle_menu(bot, update, context):
    """Заглушка для дальнейшей навигации по меню. Реальную функцию можно писать уже в отдельном файле."""
    message = context.bot.send_message(
        text='welcome_message',
        chat_id=update.effective_chat.id,
    )
    return 'START'
