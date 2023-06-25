"""Модуль с используемыми функциями для обработки сообщений"""
from django.utils import timezone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from events.models import Report, Question
from users.models import CustomUser


def send_message(bot, chat_id, text, keyboard):
    """Отправка сообщения с клавиатурой"""
    reply_markup = InlineKeyboardMarkup(keyboard)
    return bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


def start(bot, update, context):
    """Метод вывода стартового диалога"""
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id
    custom_keyboard = [
        [InlineKeyboardButton('Гость', callback_data='guest'), InlineKeyboardButton('Спикер', callback_data='speaker')]]
    send_message(bot, chat_id, 'Привет! Это PythonMeetupBot! Выберите свою роль.', custom_keyboard)
    return 'HANDLE_ROLE'


def handle_role(bot, update, context):
    """Метод обработки выбора роли"""
    user = context.user_data['user']
    chat_id = context.user_data['chat_id']
    role_selected = update.callback_query.data
    welcome_message = 'Это PythonMeetupBot - чатбот, в котором  можно узнать расписание выступлений на нашем ' \
                      'митапе, а также задать вопрос спикеру во время его выступления. А еще здесь можно знакомиться ' \
                      'с другими участниками конференции и поддержать нас донатом!'
    keyboard = [[InlineKeyboardButton("Хочу познакомиться", callback_data='meet')],
                [InlineKeyboardButton("Хочу задать вопрос", callback_data='question')],
                [InlineKeyboardButton("Хочу задонатить", callback_data='donate')]]
    user.role = role_selected
    user.save()
    if role_selected == 'speaker':
        bot.send_message(chat_id=chat_id,
                         text='Для подтверждения регистрации в роли спикера напишите менеджеру @meetup.support')
    message = send_message(bot, chat_id, welcome_message, keyboard)
    if update.callback_query:
        context.bot.delete_message(chat_id, update.callback_query.message.message_id)
    return 'HANDLE_MENU'


def handle_donate(bot, update, context):
    """Обработать донат"""
    query = update.callback_query
    if query is not None:
        query.answer()
        keyboard = [[InlineKeyboardButton("На главную", callback_data='back')]]
        query.edit_message_text(text="Поддержать наш проект можно по ссылке:",
                                reply_markup=InlineKeyboardMarkup(keyboard))
    return 'HANDLE_MENU'


def get_current_speaker():
    """Получить текущего спикера"""
    now = timezone.now()
    current_report = Report.objects.filter(started_at__lte=now, ended_at__gte=now).first()
    if current_report:
        return current_report.speaker.username
    return None


def handle_speaker(bot, update, context):
    """Обработать спикера для отправки ему вопроса"""
    query = update.callback_query
    query.answer()
    speaker_name = get_current_speaker()
    if speaker_name is None:
        update.callback_query.message.reply_text('В данный момент докладов нет.')
        return
    context.user_data['report_id'] = Report.objects.filter(started_at__lte=timezone.now(),
                                                           ended_at__gte=timezone.now()).first().id
    query.edit_message_text(text="Напишите ваш вопрос:")
    return 'HANDLE_MESSAGE'


def handle_schedule(bot, update, context):
    """Обработать расписание выступлений спикеров на сегодня"""
    query = update.callback_query
    query.answer()
    reports_today = Report.objects.filter(started_at__date=timezone.now().date()).order_by('started_at')

    schedule_message = 'Список докладов на сегодня:\n\n'
    for report in reports_today:
        schedule_message += f"{report.started_at.strftime('%H:%M')}/{report.ended_at.strftime('%H:%M')} - {report.speaker.username} - {report.topic}\n"

    keyboard = [[InlineKeyboardButton("Назад", callback_data='back')],
                [InlineKeyboardButton("Написать спикеру", callback_data='write_speaker_from_schedule')]]
    query.edit_message_text(text=schedule_message, reply_markup=InlineKeyboardMarkup(keyboard))


def handle_speaker_from_schedule(bot, update, context):
    """Обработать выбор спикера из расписания"""
    query = update.callback_query
    query.answer()
    reports_today = Report.objects.filter(started_at__date=timezone.now().date()).order_by('started_at')
    speaker_buttons = [[InlineKeyboardButton(report.speaker.username, callback_data=f"write_{report.id}")]
                       for report in reports_today]
    keyboard = speaker_buttons + [[InlineKeyboardButton("На главную", callback_data='back')]]
    query.edit_message_text(text="Выберите спикера", reply_markup=InlineKeyboardMarkup(keyboard))
    return 'WRITE_SPEAKER_FROM_SCHEDULE'


def write_speaker_from_schedule(bot, update, context):
    """Написать выбранному из расписания спикеру"""
    query = update.callback_query
    query.answer()

    if query.data == 'back':
        return start(bot, update, context)

    report_id = int(query.data.split('_')[1])
    context.user_data['report_id'] = report_id
    query.edit_message_text(text="Напишите ваш вопрос:")
    return 'HANDLE_MESSAGE'


def handle_message(bot, update, context):
    """Обработчик вопросов для спикеров"""
    if context.user_data.get('asking_question', False):
        context.user_data['asking_question'] = False
        question_text = update.message.text
        report_id = context.user_data['report_id']
        report = Report.objects.get(id=report_id)
        interviewer = CustomUser.objects.get(username=update.message.from_user.username)
        question = Question(content=question_text, interviewer=interviewer, report=report)
        question.save()

        keyboard = [
            [InlineKeyboardButton("На главную", callback_data='back')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("Спасибо! Спикер ответит на ваш вопрос в конце своего доклада.",
                                  reply_markup=reply_markup)


    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка.")
    return 'START'


def ask_question(bot, update, context):
    """Сообщение с выбором спикера для вопроса"""
    speaker_name = get_current_speaker()
    if speaker_name is None:
        update.callback_query.message.reply_text('В данный момент докладов нет.')

    keyboard = [
        [InlineKeyboardButton("Написать текущему спикеру", callback_data='write_speaker')],
        [InlineKeyboardButton("Открыть расписание всех спикеров", callback_data='schedule')],
        [InlineKeyboardButton("Назад", callback_data='back')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data['asking_question'] = True

    update.callback_query.message.reply_text(f'Текущий спикер: {speaker_name}', reply_markup=reply_markup)


def invite_to_chat(bot, update, context):
    """Приглашение познакомиться"""
    chat_id = context.user_data['chat_id']
    keyboard = [
        [InlineKeyboardButton('Хочу познакомиться', callback_data='get_name')],
        [InlineKeyboardButton('Не хочу знакомиться', callback_data='not_meet')]
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

    return 'HANDLE_MENU'


def not_meet(bot, update, context):
    """Сообщение для пользователей, не желающих знакомиться"""
    chat_id = context.user_data['chat_id']
    keyboard = [[InlineKeyboardButton("На главную", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        text='Жаль!',
        chat_id=chat_id,
        reply_markup=reply_markup
    )
    return 'HANDLE_MENU'


def get_name(bot, update, context):
    """Запрос имени пользователя для анкеты"""
    chat_id = context.user_data['chat_id']
    question = 'Как к тебе могут обращаться другие участники?'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'GET_CITY'


def get_city(bot, update, context):
    """Запрос города пользователя для анкеты"""
    context.user_data['name'] = update.message.text
    chat_id = context.user_data['chat_id']
    question = 'Из какого ты города?'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'GET_JOB'


def get_job(bot, update, context):
    """Запрос должности пользователя для анкеты"""
    context.user_data['city'] = update.message.text
    chat_id = context.user_data['chat_id']
    question = 'Где и кем ты работаешь?'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'GET_STACK'


def get_stack(bot, update, context):
    """Запрос стека пользователя для анкеты"""
    context.user_data['job'] = update.message.text
    chat_id = context.user_data['chat_id']
    question = 'Твой стек. Какие технологии используешь в работе?'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'GET_TOPICS'


def get_topics(bot, update, context):
    """Запрос предпологаемых тем общения пользователя для анкеты"""
    context.user_data['stack'] = update.message.text
    chat_id = context.user_data['chat_id']
    question = 'О чем бы ты хотел пообщаться?'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'GET_ABOUT'


def get_about(bot, update, context):
    """Запрос интересов пользователя для анкеты"""
    context.user_data['topics'] = update.message.text
    chat_id = context.user_data['chat_id']
    question = 'Расскажи ещё немного о себе (хобби, пет-проекты и т.д.)'
    context.bot.send_message(
        text=question,
        chat_id=chat_id,
    )
    return 'FINISH_REGISTER'


def finish_register(bot, update, context):
    """Сообщение о завершении опроса пользователя для анкеты"""
    context.user_data['about'] = update.message.text
    chat_id = context.user_data['chat_id']
    user = context.user_data['user']
    user.is_active = True
    user.save()
    keyboard = [[InlineKeyboardButton("На главную", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        text='Анкета заполнена, регистрация завершена.',
        chat_id=chat_id,
        reply_markup=reply_markup
    )
    return 'START'
