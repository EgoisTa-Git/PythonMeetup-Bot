def get_name(update, context):
    chat_id = context.user_data['chat_id']
    question = 'Как к тебе могут обращаться другие участники?'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'GET_CITY'


def get_city(update, context):
    context.user_data['name'] = update.message.text
    chat_id = context.user_data['chat_id']
    question = 'Из какого ты города?'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'GET_JOB'


def get_job(update, context):
    context.user_data['city'] = update.message.text
    chat_id = context.user_data['chat_id']
    question = 'Где и кем ты работаешь?'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'GET_STACK'


def get_stack(update, context):
    context.user_data['job'] = update.message.text
    chat_id = context.user_data['chat_id']
    question = 'Твой стек. Какие технологии используешь в работе?'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'GET_TOPICS'


def get_topics(update, context):
    context.user_data['stack'] = update.message.text
    chat_id = context.user_data['chat_id']
    question = 'О чем бы ты хотел пообщаться?'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'GET_ABOUT'


def get_about(update, context):
    context.user_data['topics'] = update.message.text
    chat_id = context.user_data['chat_id']
    question = 'Расскажи ещё немного о себе (хобби, пет-проекты и т.д.)'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'FINISH_REGISTER'


def finish_register(update, context):
    from meetup_bot.tg_bot_main import show_menu
    context.user_data['about'] = update.message.text
    chat_id = context.user_data['chat_id']
    user = context.user_data['user']
    user.is_active = True
    user.save()
    context.bot.send_message(
        text='Анкета заполнена, регистрация завершена.',
        chat_id=chat_id,
    )
    return show_menu(update, context)
