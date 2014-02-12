from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
	"""
	Extends Django's UserAdmin class to limit what users and User fields
	are editable by non-privileged users
	"""
	list_display = (
		'username', 'first_name', 'last_name', 'email',
		'is_active', 'is_staff', 'has_personnel_admin_privileges',
		'is_superuser',
	)

	def queryset(self, request):
		"""
		Override queryset, so that non-privileged users
		can only edit their own (logged-in) user
		"""
		qs = super(self.__class__, self).queryset(request)
		if request.user.has_personnel_admin_privileges():
			return qs
		return qs.filter(username=request.user)

	def get_fieldsets(self, request, obj=None):
		unprivileged_fieldsets = (
			(None, {'fields': ('password', )}),
			(('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
		)
		if request.user.has_personnel_admin_privileges():
			return UserAdmin.fieldsets
		else:
			return unprivileged_fieldsets


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
