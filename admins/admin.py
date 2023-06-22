from django.contrib import admin

# Register your models here.
class DefaultAdminSite(admin.AdminSite):
    name = 'admin'
    # permission = 'is_superuser'

    def get_app_list(self, request, app_label=None):
        return list(self._build_app_dict(request, app_label).values())

    # def has_permission(self, request):
    #     return super().has_permission(request) and (not getattr(self, 'permission', None) or request.user.has_perm(self.permission))

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

# class EventsAdminSite(DefaultAdminSite):
#     permission = None
#
# events_admin = EventsAdminSite(name='events-admin')
