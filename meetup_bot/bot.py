import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters


def start(update: Update, context: CallbackContext) -> None:
    welcome_message = 'Привет! Это PythonMeetupBot - чатбот, в котором  можно узнать расписание выступлений на нашем ' \
                      'митапе, а также задать вопрос спикеру во время его выступления. А еще здесь можно знакомиться ' \
                      'с другими участниками конференции и поддержать нас донатом!'
    keyboard = [
        [InlineKeyboardButton("Хочу познакомиться", callback_data='meet')],
        [InlineKeyboardButton("Хочу задать вопрос", callback_data='question')],
        [InlineKeyboardButton("Хочу задонатить", callback_data='donate')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data['asking_question'] = False

    if update.message is not None:
        update.message.reply_text(welcome_message, reply_markup=reply_markup)
    else:
        update.callback_query.message.reply_text(welcome_message, reply_markup=reply_markup)


def ask_question(update: Update, context: CallbackContext) -> None:
    speaker_name = 'Марк Цукерберг'
    keyboard = [
        [InlineKeyboardButton("Написать текущему спикеру", callback_data='write_speaker')],
        [InlineKeyboardButton("Открыть расписание всех спикеров", callback_data='schedule')],
        [InlineKeyboardButton("Назад", callback_data='back')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data['asking_question'] = True

    update.callback_query.message.reply_text(f'Текущий спикер: {speaker_name}', reply_markup=reply_markup)


def handle_message(update: Update, context: CallbackContext) -> None:
    if context.user_data.get('asking_question', False):
        context.user_data['asking_question'] = False
        keyboard = [
            [InlineKeyboardButton("На главную", callback_data='back')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Спасибо! Спикер ответит на ваш вопрос в конце своего доклада.",
                                  reply_markup=reply_markup)
    else:
        update.message.reply_text("Ошибка.")


def handle_buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'write_speaker':
        query.edit_message_text(text="Напишите ваш вопрос:")
    elif query.data == 'schedule':
        keyboard = [
            [InlineKeyboardButton("Назад", callback_data='back')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Список выступлений:", reply_markup=reply_markup)

    elif query.data == 'donate':
        keyboard = [
            [InlineKeyboardButton("На главную", callback_data='back')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text="Поддержать наш проект можно по ссылке:", reply_markup=reply_markup)

    elif query.data == 'back':
        start(update, context)
    if query.data == 'meet':
        query.edit_message_text(text="Функционал знакомств ещё в разработке.")
    elif query.data == 'question':
        ask_question(update, context)


def main() -> None:
    updater = Updater(token)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(handle_buttons))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TG_TOKEN')
    main()
