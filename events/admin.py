from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Event, Report, Donation, Question, Person


# Register your models here.
class EventModelAdmin(admin.ModelAdmin):
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


class QuesttionInline(admin.StackedInline):
    model = Question
    extra = 0

class ReportModelAdmin(admin.ModelAdmin):
    inlines = [QuesttionInline]
    list_display = ['topic', 'speaker', 'event', 'started_at', 'ended_at']
    list_display_links = ['topic', 'speaker', ]
    list_editable = ['started_at', 'ended_at']
    raw_id_fields = ('speaker',)
    list_filter = ['event', 'speaker', ]
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

class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ['author', 'content', 'report']
    raw_id_fields = ['author', ]
    list_filter = ['author', 'report', ]
    readonly_fields = ['report', 'questioned_at', ]
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


class PersonModelAdmin(admin.ModelAdmin):
    list_display = [
        'tg_id',
        'username',
        'first_name',
        'last_name',
        'is_active',
        'role',
    ]
    list_editable = ['is_active', ]
    list_filter = ['role', 'is_active', ]
    fieldsets = (
        (None, {'fields': (('username', 'password'), ('tg_id', 'bot_state'))}),
        ('Персональная информация', {
            'classes': ('collapse', 'extrapretty'),
            'fields': (('first_name', 'last_name'), )
        }),
        ('Разрешения', {
            'classes': ('collapse', 'extrapretty'),
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
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
