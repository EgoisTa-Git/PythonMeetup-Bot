from django.contrib import admin

from .models import Poll, PollQuestion, PollAnswer


class PollQuestionInline(admin.TabularInline):
    model = PollQuestion
    extra = 1


class PollAnswerInline(admin.TabularInline):
    model = PollAnswer
    extra = 1


class PollQuestionModelAdmin(admin.ModelAdmin):
    inlines = [PollAnswerInline]
    list_display = ['title', 'is_active']
    fieldsets = (
        (None, {
            'fields': (
                'title', 'is_active',
            )
        }),
    )


class PollAnswerModelAdmin(admin.ModelAdmin):
    list_display = ['answer', 'votes']
    list_display_links = ['answer']


class PollModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    raw_id_fields = ('question', 'event')
