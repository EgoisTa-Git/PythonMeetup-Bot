from django.contrib import admin

from .models import Poll


class PollModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'city',
                    'job', 'stack', 'topics',
                    'about', 'created', 'is_active']
    raw_id_fields = ('user',)
    search_fields = ('name', 'city', 'job', 'stack', 'topics', 'about')
    list_display_links = ('id', 'name')
    list_filter = ('is_active', 'created')

    fieldsets = (
        (None, {
            'fields': (
                'is_active',
                ('name', 'user', ),
                ('city', 'job', 'stack', ),
                'topics', 'about',
                'created',
            )
        }),
    )
