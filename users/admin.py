import logging
from textwrap import dedent

from django.conf import settings
from django.contrib import admin
from django.db.models import QuerySet
from django.utils import timezone
from telegram import Bot

from events.models import Report

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_format = logging.Formatter(
    fmt='{asctime} - {levelname} - {name} - {message}',
    style='{'
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
logger.addHandler(stream_handler)


def get_mailing():
    """Возвращает сообщение для рассылки"""
    now = timezone.localtime(timezone.now())
    reports = Report.objects.filter(
        event__start_date__lte=now, event__end_date__gte=now
    ).order_by('started_at')

    reports_descriptions = []
    for report in reports:
        report_date = report.started_at.strftime('%d-%m-%Y')
        time_start = report.started_at.strftime('%H:%M')
        time_finish = report.ended_at.strftime('%H:%M')
        description = """\
                Тема: %s
                Докладчик: %s
                Дата: %s
                Время: %s-%s
                """ % (report.topic, report.speaker,
                       report_date, time_start, time_finish)
        reports_descriptions.append(dedent(description))
    mailing = 'Мероприятия на митапе:\n\n' +\
              '\n'.join(reports_descriptions)
    return mailing


class ReportInline(admin.TabularInline):
    model = Report
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                ('topic', 'event', ),
                ('started_at', 'ended_at'),
            )
        }),
    )


class CustomUserModelAdmin(admin.ModelAdmin):
    inlines = [ReportInline]
    list_display = [
        'tg_id',
        'username',
        'first_name',
        'last_name',
        'role',
        'is_subscriber',
        'is_active',
    ]
    list_filter = ['role', 'is_active', 'is_subscriber',]
    fieldsets = (
        (None, {'fields': (
            ('username', 'password'),
            ('tg_id', 'bot_state'),
            ('is_subscriber', 'is_active'),
        )}),
        ('Персональная информация', {
            'classes': ('collapse', 'extrapretty'),
            'fields': (('first_name', 'last_name'), )
        }),
        ('Разрешения', {
            'classes': ('collapse', 'extrapretty'),
            'fields': ('role', 'is_staff', 'is_superuser')
        }),
        ('Дополнительная информация', {
            'classes': ('collapse', 'extrapretty'),
            'fields': ('date_joined', 'last_login')
        }),
    )
    add_fieldsets = (
        (
            None,
            {
                'fields': ('tg_id', 'username', 'password1', 'password2'),
            }
        ),
    )
    search_fields = ('tg_id', 'username', 'first_name', 'last_name')
    readonly_fields = ['date_joined', 'last_login', ]
    list_per_page = 20
    save_on_top = True
    actions = ['publish']

    @admin.action(description='Рассылка списка выступлений')
    def publish(self, request, qs: QuerySet):
        """Направляет рассылку на подписчиков"""
        bot = Bot(settings.TG_BOT_APIKEY)
        mailing = get_mailing()
        subscribers_ids = qs.filter(
            tg_id__isnull=False,
            tg_id__gte=99999999)\
            .values_list('tg_id', flat=True)
        if subscribers_ids:
            for tg_id in subscribers_ids:
                try:
                    bot.send_message(
                        chat_id=tg_id,
                        text=dedent(mailing)
                    )
                except Exception as e:
                    logger.error(e, exc_info=True)
            return self.message_user(
                request,
                f'Рассылка отправлена {subscribers_ids.count()} подписчикам.')
        return self.message_user(request, f'Рассылка не отправлена.')
