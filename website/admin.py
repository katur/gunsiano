from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from website.models import Position, UserProfile
from django.contrib.auth.models import User

class PositionAdmin(admin.ModelAdmin):
	list_display = ('position', 'display_order')


class UserProfileAdmin(admin.ModelAdmin):
	list_display = (
		'__unicode__',
		'net_id',
		'url',
		'is_current',
		'in_abu_dhabi'
	)

	list_filter = ('is_current', 'in_abu_dhabi')

	def queryset(self, request):
		qs = super(self.__class__, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(user=request.user)

	def get_form(self, request, obj=None, **kwargs):
		if not request.user.is_superuser:
			self.exclude = ('user', 'in_abu_dhabi', 'is_current', 'image_filename')
		return super(UserProfileAdmin, self).get_form(request, obj, **kwargs)


class MyUserAdmin(UserAdmin):
	list_display = UserAdmin.list_display + ('is_active', 'is_superuser',)

	# for non-superusers, limit the editable users to the logged in user
	def queryset(self, request):
		qs = super(self.__class__, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(username=request.user)

	# define a subset of safe fieldsets that non-superusers can access
	safe_fieldsets = (
		(None, {'fields': ('username',)}),
		(('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
	)

	def change_view(self, request, object_id, extra_context=None):
		if not request.user.is_superuser:
			self.fieldsets = self.safe_fieldsets
			return UserAdmin.change_view(self, request, object_id, extra_context=None)
		else:
			return UserAdmin.change_view(self, request, object_id, extra_context=None)


admin.site.register(Position, PositionAdmin)
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
