from django.contrib import admin

from worm_strains.models import (Mutagen, Transgene, WormLab, WormSpecies,
                                 WormStrain, WormStrainLine)


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

    search_fields = ('name', 'genotype', 'species__name',)


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
    )

    search_fields = ('strain__name', 'strain__genotype', 'received_from',)


class WormLabAdmin(admin.ModelAdmin):
    list_display = (
        'lab',
        'strain_code',
        'allele_code',
    )

    search_fields = ('lab',)


class TransgeneAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'vector',
    )

    search_fields = ('name',)


admin.site.register(Mutagen)
admin.site.register(Transgene, TransgeneAdmin)
admin.site.register(WormLab, WormLabAdmin)
admin.site.register(WormSpecies)
admin.site.register(WormStrain, WormStrainAdmin)
admin.site.register(WormStrainLine, WormStrainLineAdmin)
