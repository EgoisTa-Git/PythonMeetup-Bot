from django.contrib import admin

from .models import Poll


class PollModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'city',
                    'job', 'stack', 'topics',
                    'about', 'created', 'is_active']
    raw_id_fields = ('user',)
    search_fields = ('name', 'city', 'job', 'stack', 'topics', 'about')
    list_display_links = ('user', )
    list_filter = ('is_active', 'created')

    fieldsets = (
        (None, {
            'fields': (
                'is_active',
                ('user', 'name', ),
                ('city', 'job', 'stack', ),
                'topics', 'about',
            )
        }),
    )
