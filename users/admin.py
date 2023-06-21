from django.contrib import admin
from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from admins.admin import users_admin

# @admin.register(CustomUser)
class CustomUserModelAdmin(admin.ModelAdmin):
    paginate_by = 20
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'tg_id',
        'username',
        'first_name',
        'last_name',
        'is_active',
        'role',
    ]
    list_editable = ['is_active',]
    list_filter = [
        'role',
        'is_active',
    ]
    add_fieldsets = (
        (
            None,
            {
                'fields': (
                    'tg_id',
                    'username',
                    'role',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
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
                    'first_name',
                    'last_name',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'password',
                    'bot_state'
                )
            }
        ),
    )

users_admin.register(CustomUser)
