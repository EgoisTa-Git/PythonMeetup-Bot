import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_meetup.settings')
django.setup()

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

from django.utils import timezone
from events.models import Report, Question
from users.models import CustomUser


def get_current_speaker():
    now = timezone.now()
    current_report = Report.objects.filter(started_at__lte=now, ended_at__gte=now).first()
    if current_report:
        return current_report.speaker.username
    return None


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

    return 'HANDLE_BUTTONS'


def ask_question(update: Update, context: CallbackContext) -> None:
    speaker_name = get_current_speaker()
    if speaker_name is None:
        update.callback_query.message.reply_text('В данный момент докладов нет.')
        return 'START'

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
        return 'START'
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка.")
        return 'START'


def handle_buttons(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query is not None:
        query.answer()

        if query.data == 'write_speaker_from_schedule':
            reports_today = Report.objects.filter(started_at__date=timezone.now().date()).order_by('started_at')
            speaker_buttons = [[InlineKeyboardButton(report.speaker.username, callback_data=f"write_{report.id}")] for
                               report in reports_today]

            keyboard = speaker_buttons + [[InlineKeyboardButton("Назад", callback_data='back')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text="Выберите спикера", reply_markup=reply_markup)


        elif query.data.startswith('write_') and query.data.split('_')[1].isdigit():
            report_id = int(query.data.split('_')[1])
            context.user_data['report_id'] = report_id
            query.edit_message_text(text="Напишите ваш вопрос:")
            return 'HANDLE_MESSAGE'

        elif query.data == 'write_speaker':
            speaker_name = get_current_speaker()
            if speaker_name is None:
                update.callback_query.message.reply_text('В данный момент докладов нет.')
                return
            context.user_data['report_id'] = Report.objects.filter(started_at__lte=timezone.now(),
                                                                   ended_at__gte=timezone.now()).first().id
            query.edit_message_text(text="Напишите ваш вопрос:")
            return 'HANDLE_MESSAGE'

        elif query.data == 'schedule':
            reports_today = Report.objects.filter(started_at__date=timezone.now().date()).order_by('started_at')

            schedule_message = 'Список докладов на сегодня:\n\n'
            for report in reports_today:
                schedule_message += f"{report.started_at.strftime('%H:%M')}/{report.ended_at.strftime('%H:%M')} - {report.speaker.username} - {report.topic}\n"

            keyboard = [
                [InlineKeyboardButton("Назад", callback_data='back')],
                [InlineKeyboardButton("Написать спикеру", callback_data='write_speaker_from_schedule')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text=schedule_message, reply_markup=reply_markup)


        elif query.data == 'donate':
            keyboard = [
                [InlineKeyboardButton("На главную", callback_data='back')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(text="Поддержать наш проект можно по ссылке:", reply_markup=reply_markup)

        elif query.data == 'back':
            start(update, context)
        elif query.data == 'meet':
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
    token = os.getenv('TG_BOT_APIKEY')
    main()
