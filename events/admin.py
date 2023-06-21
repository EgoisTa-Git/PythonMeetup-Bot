from django.contrib import admin
from admins.admin import events_admin
from .models import Event, Report, Donation, Question


# Register your models here.
class EventModelAdmin(admin.ModelAdmin):
    ...


class ReportModelAdmin(admin.ModelAdmin):
    ...


class DonationModelAdmin(admin.ModelAdmin):
    ...


class QuestionModelAdmin(admin.ModelAdmin):
    ...


events_admin.register(Event)
events_admin.register(Report)
events_admin.register(Donation)
events_admin.register(Question)
