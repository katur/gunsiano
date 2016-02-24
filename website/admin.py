from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from website.models import (JoinLabSection, Position, ResearchArea,
                            Resource, Publication, UserProfile)


def has_personnel_admin_privileges(user):
    return (user.is_superuser or
            user.groups.filter(name='Personnel').exists())


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

    def get_queryset(self, request):
        """
        Override queryset, so that non-privileged users
        can only edit their own (logged-in) user
        """
        qs = super(self.__class__, self).get_queryset(request)

        if has_personnel_admin_privileges(request.user):
            return qs
        else:
            return qs.filter(user=request.user)

    def get_fieldsets(self, request, obj=None):
        unprivileged_fieldsets = (
            ((), {'fields': ('net_id', 'url', 'image', 'blurb',)}),
        )

        if has_personnel_admin_privileges(request.user):
            return super(UserProfileInline, self).get_fieldsets(request, obj)
        else:
            return unprivileged_fieldsets


class MyUserAdmin(UserAdmin):
    """
    Extends Django's UserAdmin class to limit what users and User fields
    are editable by non-privileged users
    """
    inlines = (UserProfileInline,)

    list_display = ('first_name', 'last_name', 'username', 'email',)

    ordering = ('first_name', 'last_name',)

    def get_queryset(self, request):
        """
        Override queryset, so that non-privileged users
        can only edit their own (logged-in) user
        """
        qs = super(self.__class__, self).get_queryset(request)

        if has_personnel_admin_privileges(request.user):
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

            if has_personnel_admin_privileges(request.user):
                return super(MyUserAdmin, self).get_fieldsets(request, obj)
            else:
                return unprivileged_fieldsets

        else:
            return self.add_fieldsets


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
        'display_order',
    )

    list_editable = (
        'display_order',
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
        'pubmed_id',
        'title',
        'date',
        'journal',
        'hidden',
    )

    search_fields = ('title', 'authors', 'abstract', 'journal',)


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
