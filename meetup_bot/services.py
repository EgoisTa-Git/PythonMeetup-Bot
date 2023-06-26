"""Модуль с используемыми функциями для обработки сообщений"""
from django.utils import timezone
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from events.models import Report, GuestQuestion, Donation
from users.models import CustomUser
from polls.models import Poll


def start(bot, update, context):
    """Метод вывода стартового диалога"""
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat_id
    keyboard = [
        [InlineKeyboardButton(
            'Гость', callback_data='guest'),
            InlineKeyboardButton('Спикер', callback_data='speaker')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=chat_id,
        text='Привет! Это PythonMeetupBot! Выберите свою роль.',
        reply_markup=reply_markup
    )
    return 'HANDLE_ROLE'


def reply_markup_to_main():
    """Кнопка На главную"""
    keyboard = [[InlineKeyboardButton("На главную", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


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

    reply_markup = InlineKeyboardMarkup(keyboard)
    user.role = role_selected
    user.save()
    if role_selected == 'speaker':
        bot.send_message(chat_id=chat_id,
                         text='Для подтверждения регистрации в роли спикера напишите менеджеру @python-meetup.support')

    bot.send_message(chat_id=chat_id, text=welcome_message, reply_markup=reply_markup)
    if update.callback_query:
        context.bot.delete_message(chat_id, update.callback_query.message.message_id)
    return 'HANDLE_MENU'


def donate(bot, update, context):
    """Сообщение для доната организаторам"""
    query = update.callback_query
    if query is not None:
        query.answer()
        query.edit_message_text(text="Введите сумму вашего доната:")
    return 'HANDLE_DONATE'


def handle_donate(bot, update, context):
    """Обработать донат пользователя"""
    try:
        amount = int(update.message.text)
    except ValueError:
        context.bot.send_message(
            text="Пожалуйста, введите число.",
            chat_id=update.message.chat_id,
        )
        return 'HANDLE_DONATE'

    custom_user = CustomUser.objects.get(tg_id=update.effective_user.id)
    Donation.objects.create(
        donor=custom_user,
        amount=amount
    )
    reply_markup = reply_markup_to_main()
    context.bot.send_message(
        text="Спасибо за вашу поддержку!",
        chat_id=update.message.chat_id,
        reply_markup=reply_markup
    )
    return 'START'


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
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text="Выберите спикера", reply_markup=reply_markup)
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
        questioned_at = timezone.now()
        user_id = update.effective_user.id
        author, created = CustomUser.objects.get_or_create(tg_id=user_id)

        question, status = GuestQuestion.objects.get_or_create(
            content=question_text,
            report=report,
            author=author
        )

        reply_markup = reply_markup_to_main()
        update.message.reply_text("Спасибо! Спикер ответит на ваш вопрос в конце своего доклада.",
                                  reply_markup=reply_markup)
    else:
        reply_markup = reply_markup_to_main()
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка.", reply_markup=reply_markup)
    return 'START'


def ask_question(bot, update, context):
    """Сообщение с выбором спикера для вопроса"""
    speaker_name = get_current_speaker()
    if speaker_name is None:
        update.callback_query.message.reply_text('На сегодняшний день выступлений не планируется.')

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
        [InlineKeyboardButton('Хочу познакомиться', callback_data='start_poll')],
        [InlineKeyboardButton('Не хочу знакомиться', callback_data='not_meet')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    message = context.bot.send_message(
        text='Тут можно познакомиться с другими участниками митапа. Для этого нужно заполнить анкету,'
             ' ответив на несколько вопросов, а затем мы пришлем вам анкету другого посетителя нашего митапа!',
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


def start_poll(bot, update, context):
    """Начальное сообщение для заполнения анкеты пользователем"""
    poll = Poll.objects.filter(is_active=True).first()

    if not poll:
        reply_markup = reply_markup_to_main()
        context.bot.send_message(
            text='В данный момент нет активных анкет. Пожалуйста, попробуйте позже.',
            chat_id=update.callback_query.message.chat_id,
            reply_markup=reply_markup
        )
        return 'START'

    questions = poll.question.all()

    context.user_data['questions'] = list(questions)
    context.user_data['current_question'] = context.user_data['questions'].pop(0)

    context.bot.send_message(
        text=context.user_data['current_question'].title,
        chat_id=update.callback_query.message.chat_id,
    )

    return 'HANDLE_POLL_ANSWER'


def handle_poll_answer(bot, update, context):
    """Обработчик ответов пользователя для анкеты"""
    current_question = context.user_data['current_question']

    PollAnswer.objects.create(
        question=current_question,
        answer=update.message.text
    )

    if context.user_data['questions']:
        context.user_data['current_question'] = context.user_data['questions'].pop(0)
        context.bot.send_message(
            text=context.user_data['current_question'].title,
            chat_id=update.message.chat_id,
        )
    else:
        reply_markup = reply_markup_to_main()
        context.bot.send_message(
            text='Отлично! Вот анкета другого случайного посетителя нашего митапа:',
            chat_id=update.message.chat_id,
            reply_markup=reply_markup
        )
        return 'START'

    return 'HANDLE_POLL_ANSWER'


def not_meet(bot, update, context):
    """Сообщение для пользователей, не желающих знакомиться"""
    chat_id = context.user_data['chat_id']
    reply_markup = reply_markup_to_main()
    context.bot.send_message(
        text='Очень жаль :( Рекомендуем все же попробовать, ведь чем активнее вы знакомитесь с людьми,'
             ' тем увереннее и гармоничнее себя чувствуете!',
        chat_id=chat_id,
        reply_markup=reply_markup
    )
    return 'HANDLE_MENU'
