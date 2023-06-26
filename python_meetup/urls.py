from django.contrib import admin
from django.urls import path
from django.contrib.admin.sites import all_sites

admin.site.site_header = 'Python Meetup'
admin.site.site_title = 'Python Meetup'
admin.site.index_title = 'Python Meetup administration'


urlpatterns = [
    path(f'{site.name}/', site.urls) for site in all_sites
]
