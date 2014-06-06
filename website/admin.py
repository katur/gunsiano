from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from website.models import (JoinLabSection, Position, ResearchArea, Resource,
                            Publication, UserProfile)


class UserProfileInline(admin.StackedInline):
    model = UserProfile

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


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    """
    Extends Django's UserAdmin class to limit what users and User fields
    are editable by non-privileged users
    """
    inlines = [UserProfileInline]
    form = MyUserChangeForm

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
        unprivileged_fieldsets = (
            (None, {
                'fields': ('password', 'first_name', 'last_name', 'email',)
            }),
        )

        if request.user.has_personnel_admin_privileges():
            return self.declared_fieldsets
        else:
            return unprivileged_fieldsets


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'display_order',
    )

    list_editable = (
        'display_order',
    )


class ResearchAreaAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
    )


class ResourceAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'url',
        'display_order',
    )

    list_editable = (
        'display_order',
    )


class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'pubmed_id',
        'date',
    )


class JoinLabSectionAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'display_order',
    )

    list_editable = (
        'display_order',
    )


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(ResearchArea, ResearchAreaAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(JoinLabSection, JoinLabSectionAdmin)
