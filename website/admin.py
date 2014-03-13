from django.contrib import admin
from moderation.admin import ModerationAdmin
from website.models import *


class UserProfileAdmin(admin.ModelAdmin):
	list_display = (
		'first_name', 'last_name', 'user', 'net_id', 'url', 'image_filename',
		'is_current', 'in_abu_dhabi',
	)

	list_filter = ('is_current', 'in_abu_dhabi',)

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
			(('Personal info'), {'fields': ('net_id',)}),
			(('Public Profile info'), {'fields': ('url', 'blurb',)}),
		)

		if request.user.has_personnel_admin_privileges():
			return super(UserProfileAdmin, self).get_fieldsets(request, obj)
		else:
			return unprivileged_fieldsets


class PositionAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'display_order',)


class ResearchAreaAdmin(admin.ModelAdmin):
	list_display = ('__unicode__',)


class ResourceAdmin(admin.ModelAdmin):
	list_display = (
		'__unicode__',
		'url',
		'display_order',
	)


class JoinLabSectionAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'display_order',)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(ResearchArea, ResearchAreaAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(JoinLabSection, JoinLabSectionAdmin)
