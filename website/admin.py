from django.contrib import admin
from website.models import UserProfile, Position, ResearchArea, Resource

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

class PositionAdmin(admin.ModelAdmin):
	list_display = (
		'position',
		'display_order'
	)

class ResearchAreaAdmin(admin.ModelAdmin):
	list_display = (
		'__unicode__',
		'display_order'
	)

class ResourceAdmin(admin.ModelAdmin):
	list_display = (
		'__unicode__',
	)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(ResearchArea, ResearchAreaAdmin)
admin.site.register(Resource, ResourceAdmin)
