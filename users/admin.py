from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'tg_id',
        'username',
        'real_name',
        'role',
        'ready_to_chat',
    ]
    list_filter = [
        'role',
        'ready_to_chat',
    ]
    add_fieldsets = (
        (
            None,
            {
                'fields': (
                    'tg_id',
                    'username',
                    'role',
                    'ready_to_chat',
                    'real_name',
                    'city',
                    'work_place',
                    'stack',
                    'topics',
                    'about_me',
                    'password1',
                    'password2',
                    'publish_date',
                )
            }
        ),
    )
    fieldsets = (
        (
            None,
            {
                'fields': (
                    'tg_id',
                    'username',
                    'role',
                    'ready_to_chat',
                    'real_name',
                    'city',
                    'work_place',
                    'stack',
                    'topics',
                    'about_me',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'password',
                    'bot_state',
                    'publish_date',
                )
            }
        ),
    )
