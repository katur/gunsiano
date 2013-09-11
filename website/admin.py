from django.contrib import admin
from website.models import UserProfile, Position

class PositionAdmin(admin.ModelAdmin):
	list_display = ('position', 'display_order')

class UserProfileAdmin(admin.ModelAdmin):
	list_display = (
		'__unicode__',
		'net_id', 'url',
		'is_current',
		'in_abu_dhabi'
	)
	list_filter = ('is_current', 'in_abu_dhabi')

	def queryset(self, request):
		qs = super(UserProfileAdmin, self).queryset(request)
		if request.user.is_superuser:
			return qs
		return qs.filter(user=request.user)

admin.site.register(Position, PositionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
