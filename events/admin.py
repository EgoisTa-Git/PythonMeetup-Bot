from django.contrib import admin
from admins.admin import events_admin
from .models import Event, Report, Donation, Question


# Register your models here.
class EventModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'address', 'start_date', 'end_date', 'creator']
    list_display_links = ['title',]
    raw_id_fields = ('creator', )


class ReportModelAdmin(admin.ModelAdmin):
    list_display = ['topic', 'speaker', 'event', 'started_at', 'ended_at']
    list_display_links = ['topic', 'speaker', ]
    list_editable = ['started_at', 'ended_at']
    raw_id_fields = ('speaker',)


class DonationModelAdmin(admin.ModelAdmin):
    list_display = ['donor', 'amount', 'donation_date']
    raw_id_fields = ['donor', ]


class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ['content', 'interviewer', 'report']
    raw_id_fields = ['interviewer', ]


events_admin.register(Event)
events_admin.register(Report)
events_admin.register(Donation)
events_admin.register(Question)
