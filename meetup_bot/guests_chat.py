from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def invite_to_chat(bot, update, context):
    """Приглашение вступить в чат"""
    chat_id = context.user_data['chat_id']
    keyboard = [
        [InlineKeyboardButton('Хочу познакомиться', callback_data='get_answers')],
        [InlineKeyboardButton('Не хочу знакомиться', callback_data='menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = context.bot.send_message(
        text='Тут можно познакомиться с другими участниками митапа. \
        Для этого нужно ответить на несколько вопросов.',
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
    return 'HANDLE_ROLE'
