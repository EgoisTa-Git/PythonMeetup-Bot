"""Основной модуль бота"""

from textwrap import dedent

from django.conf import settings

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
)

from users.models import CustomUser

from meetup_bot.guests_chat import (
    get_name,
    get_city,
    get_job,
    get_stack,
    get_topics,
    get_about,
    finish_register,
)


def bot():
    updater = Updater(token=settings.TG_BOT_APIKEY, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))
    updater.start_polling()
    updater.idle()


def handle_users_reply(update, context):
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

    user, created = CustomUser.objects.get_or_create(
        tg_id=chat_id,
        defaults={'username': username},
    )
    if created:
        user.is_active = False
        user.save()
    context.user_data['user'] = user
    context.user_data['chat_id'] = chat_id

    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = user.bot_state

    states_functions = {
        'START': start,
        'HANDLE_ROLE': handle_role,
        'HANDLE_MENU': handle_menu,
        'GET_CITY': get_city,
        'GET_JOB': get_job,
        'GET_STACK': get_stack,
        'GET_TOPICS': get_topics,
        'GET_ABOUT': get_about,
        'FINISH_REGISTER': finish_register,
    }
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(update, context)
        user.bot_state = next_state
        user.save()
    except Exception as err:
        print(err)


def start(update, context):
    """Метод вывода стартового диалога"""
    chat_id = update.message.chat_id
    user = context.user_data['user']
    custom_keyboard = [
        [InlineKeyboardButton('Гость', callback_data='guest'),
         InlineKeyboardButton('Спикер', callback_data='speaker'), ]
    ]
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    update.message.reply_text(
        'Привет! Это Python Meetup Bot! Выберите свою роль.',
        reply_markup=reply_markup,
    )
    return 'HANDLE_ROLE'


def handle_role(update, context):
    """Метод обработки выбора роли"""
    user = context.user_data['user']
    chat_id = context.user_data['chat_id']
    role_selected = update.callback_query.data
    if role_selected == 'guest':
        user.role = 'guest'
        user.save()
    elif role_selected == 'speaker':
        user.role = 'speaker'
        user.save()
        text = 'Для подтверждения регистрации в роли спикера напишите \
        менеджеру @meetup.support'
        context.bot.send_message(
            chat_id=chat_id,
            text=text,
        )
    else:
        return 'HANDLE_ROLE'
    return show_menu(update, context)


def show_menu(update, context):
    """Метод отображает главное меню"""
    chat_id = context.user_data['chat_id']
    user = context.user_data['user']
    welcome_message = '''
    Python Meetup Bot - чат-бот, в котором  можно узнать расписание выступлений
    на нашем митапе, а также задать вопрос спикеру во время его выступления. 
    А еще здесь можно знакомиться с другими участниками конференции и 
    поддержать нас донатом!
    '''
    welcome_message = dedent(welcome_message)
    text = " ".join(line.strip() for line in welcome_message.splitlines())
    if user.is_active:
        keyboard = [
            [InlineKeyboardButton("Начать общаться", callback_data='chat')],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton("Хочу познакомиться", callback_data='meet')],
        ]
    keyboard = keyboard + [
        [InlineKeyboardButton("Хочу задать вопрос", callback_data='question')],
        [InlineKeyboardButton("Хочу задонатить", callback_data='donate')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = context.bot.send_message(
        text=text,
        chat_id=chat_id,
    )
    context.bot.edit_message_reply_markup(
        chat_id=chat_id,
        message_id=message.message_id,
        reply_markup=reply_markup,
    )
    query = update.callback_query
    if query:
        context.bot.delete_message(
            chat_id,
            query.message.message_id,
        )
    return 'HANDLE_MENU'


def handle_menu(update, context):
    """Метод обработки выбора в главном меню"""
    user = context.user_data['user']
    chat_id = context.user_data['chat_id']
    menu_selected = update.callback_query.data
    if menu_selected == 'meet':
        return get_name(update, context)
    elif menu_selected == 'chat':
        # TODO Заглушка
        context.bot.send_message(
            text='Отправляем анкету',
            chat_id=chat_id,
        )
        return show_menu(update, context)
    elif menu_selected == 'question':
        # TODO Заглушка
        return show_menu(update, context)
    elif menu_selected == 'donate':
        # TODO Заглушка
        return show_menu(update, context)
