from django.contrib import admin
from worm_strains.models import *

class WormStrainAdmin(admin.ModelAdmin):
	list_display = (
		'name',
		'species',
		'genotype',
	)
	list_filter = ('created_by',)

class WormStrainLineAdmin(admin.ModelAdmin):
	list_display = (
		'strain',
		'created_internally',
		'times_outcrossed',
		'received_from',
		'received_by',
		'date_received'
	)
	list_filter = (
		'created_internally',
		'received_by'
	)

admin.site.register(WormSpecies)
admin.site.register(Mutagen)
admin.site.register(Transgene)
admin.site.register(WormLab)
admin.site.register(WormStrain, WormStrainAdmin)
admin.site.register(WormStrainLine, WormStrainLineAdmin)
