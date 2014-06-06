from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from website.models import (UserProfile)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

    def queryset(self, request):
        """
        Override queryset, so that non-privileged users
        can only edit their own (logged-in) user
        """
        qs = super(self.__class__, self).queryset(request)

        if request.user.has_personnel_admin_privileges():
            return qs
        else:
            return qs.filter(user=request.user)

    def get_fieldsets(self, request, obj=None):
        unprivileged_fieldsets = (
            ((), {'fields': ('net_id', 'url', 'blurb',)}),
        )

        if request.user.has_personnel_admin_privileges():
            return super(UserProfileInline, self).get_fieldsets(request, obj)
        else:
            return unprivileged_fieldsets


class MyUserAdmin(UserAdmin):
    """
    Extends Django's UserAdmin class to limit what users and User fields
    are editable by non-privileged users
    """
    inlines = (UserProfileInline,)

    list_display = (
        'first_name',
        'last_name',
        'username',
        'email',
        'is_active',
        'is_staff',
        'has_personnel_admin_privileges',
        'is_superuser',
    )

    ordering = (
        'first_name',
        'last_name',
    )

    def queryset(self, request):
        """
        Override queryset, so that non-privileged users
        can only edit their own (logged-in) user
        """
        qs = super(self.__class__, self).queryset(request)

        if request.user.has_personnel_admin_privileges():
            return qs
        else:
            return qs.filter(username=request.user)

    def get_fieldsets(self, request, obj=None):
        if obj:
            unprivileged_fieldsets = (
                (None, {
                    'fields': ('username', 'password', 'first_name',
                               'last_name', 'email')
                }),
            )

            if request.user.has_personnel_admin_privileges():
                print self.declared_fieldsets
                return self.declared_fieldsets
            else:
                return unprivileged_fieldsets

        else:
            return self.add_fieldsets


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
