from django.contrib import admin

# Register your models here.
class DefaultAdminSite(admin.AdminSite):
    name = 'admin'
    permission = None

    def get_app_list(self, request, app_label=None):
        return list(self._build_app_dict(request, app_label).values())

    def admin_view(self, view, cacheable = False):

        def wrapper(func):

            def wrapped(*args, **kwargs):
                instance = getattr(func, '__self__', None)
                if isinstance(instance, admin.ModelAdmin):
                    new_instance = type(instance)(instance.model, instance.admin_site)
                    return func.__func__(new_instance, *args, **kwargs)
                return func(*args, **kwargs)

            return wrapped

        return super().admin_view(wrapper(view), cacheable=False)


default_admin = admin.sites.site


class CustomUserAdminSite(DefaultAdminSite):
    permission = None


users_admin = CustomUserAdminSite(name='users-admin')


class TelegramBotAdminSite(DefaultAdminSite):
    permission = None


tgbot_admin = TelegramBotAdminSite(name='tgbot-admin')

class EventsAdminSite(DefaultAdminSite):
    permission = None


events_admin = EventsAdminSite(name='events-admin')