from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class MyUserAdmin(UserAdmin):
	list_display = ('get_full_name',) + UserAdmin.list_display + ('is_active', 'is_superuser',)

	# for non-superusers, limit the editable users to the logged in user
	def queryset(self, request):
		qs = super(self.__class__, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(username=request.user)

	# fieldsets that are safe for non-superusers to access
	safe_fieldsets = (
		(None, {'fields': ('username', 'password')}),
		(('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
	)

	def change_view(self, request, object_id, extra_context=None):
		# both cases necessary to toggle between types of users being logged in
		if request.user.is_superuser:
			self.fieldsets = UserAdmin.fieldsets
		else:
			self.fieldsets = self.safe_fieldsets
		return UserAdmin.change_view(self, request, object_id, extra_context=None)

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)
