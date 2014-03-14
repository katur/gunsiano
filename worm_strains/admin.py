from django.contrib import admin
from worm_strains.models import *


class WormStrainAdmin(admin.ModelAdmin):
  list_display = (
      'name',
      'species',
      'genotype',
      'mutagen',
      'created_by',
      'date_created',
      'on_wormbase',
  )

  list_filter = (
      'created_by',
  )


class WormStrainLineAdmin(admin.ModelAdmin):
  list_display = (
      'strain',
      'stockable',
      'created_internally',
      'received_from',
      'received_by',
      'date_received',
  )

  list_filter = (
      'created_internally',
      'received_by',
  )


class WormLabAdmin(admin.ModelAdmin):
  list_display = (
      'lab',
      'strain_code',
      'allele_code',
  )


admin.site.register(WormSpecies)
admin.site.register(Mutagen)
admin.site.register(Transgene)
admin.site.register(WormLab, WormLabAdmin)
admin.site.register(WormStrain, WormStrainAdmin)
admin.site.register(WormStrainLine, WormStrainLineAdmin)
