from django.contrib import admin
from textwrap import dedent
from .models import Event, Report, Donation, GuestQuestion
from users.models import CustomUser



class ReportInline(admin.TabularInline):
    model = Report
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                ('topic', 'speaker', ),
                ('started_at', 'ended_at'),
            )
        }),
    )


class EventModelAdmin(admin.ModelAdmin):
    inlines = [ReportInline]
    list_display = ['title', 'description', 'address', 'start_date', 'end_date', 'creator']
    list_display_links = ['title',]
    raw_id_fields = ('creator', )
    list_filter = ['address', ]
    readonly_fields = ['modified', ]
    fieldsets = (
        (None, {'fields': (('title', 'creator'), 'address', 'description')}),
        ('Даты проведения', {
            'classes': ('collapse', 'extrapretty'),
            'fields': (('start_date', 'end_date'), 'modified')
        }),
    )


class GuestQuestionInline(admin.StackedInline):
    model = GuestQuestion
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                ('content', 'author',),
            )
        }),
    )


def get_mailing(queryset):
    """Возвращает сообщение для рассылки"""
    reports_descriptions = []
    for report in queryset:
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


class ReportModelAdmin(admin.ModelAdmin):
    inlines = [GuestQuestionInline]
    list_display = ['topic', 'speaker', 'event', 'started_at', 'ended_at', 'modified']
    list_display_links = ['topic', 'speaker', ]
    list_editable = ['started_at', 'ended_at']
    raw_id_fields = ('speaker',)
    list_filter = ['event', 'speaker', 'started_at']
    readonly_fields = ['modified', ]
    fieldsets = (
        (None, {
            'fields': (
                'event',
                ('topic', 'speaker', ),
                ('started_at', 'ended_at'),
                'modified',
            )
        }),
    )
    actions = ['publish']

    @admin.action(description='Рассылка')
    def publish(self, request, queryset, bot):
        """Направляет рассылку на подписчиков"""
        subscribers_ids = CustomUser.objects.filter(
            is_subscriber=True, is_active=True)\
            .values_list('tg_id', flat=True)
        mailing_message = get_mailing(queryset)
        for tg_id in subscribers_ids:
            bot.send_message(
                chat_id=tg_id,
                message=dedent(mailing_message)
            )
        self.message_user(request, f'Рассылка отправлена {subscribers_ids.count()} подписчикам.')


class GuestQuestionModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'report']
    raw_id_fields = ['author', ]
    list_filter = ['author', 'report', ]
    readonly_fields = ['questioned_at', ]
    fieldsets = (
        (None, {
            'fields': (
                ('content', 'author'),
                ('report', 'questioned_at'),
            )
        }),
    )


class DonationModelAdmin(admin.ModelAdmin):
    list_display = ['donor', 'amount', 'donation_date']
    raw_id_fields = ['donor', ]
    list_filter = ['donor', 'donation_date', ]
    readonly_fields = ['donation_date', ]
    fieldsets = (
        (None, {
            'fields': (
                ('donor', 'amount'),
                'donation_date',
            )
        }),
    )