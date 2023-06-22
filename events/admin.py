from django.contrib import admin
from .models import Event, Report, Donation, GuestQuestion


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


class GuestQuestionInline(admin.StackedInline):
    model = GuestQuestion
    extra = 0


class ReportModelAdmin(admin.ModelAdmin):
    inlines = [GuestQuestionInline]
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


class GuestQuestionModelAdmin(admin.ModelAdmin):
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
