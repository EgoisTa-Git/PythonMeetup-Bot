from django.contrib import admin
from .models import CustomUser
from events.models import Report


class PollInline(admin.TabularInline):
    model = CustomUser.polls.through
    extra = 0


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
    inlines = [ReportInline, PollInline]
    list_display = [
        'tg_id',
        'username',
        'first_name',
        'last_name',
        'role',
        'is_subscriber',
        'is_active',
    ]
    # list_editable = ['is_active', ]
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