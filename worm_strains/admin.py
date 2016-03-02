from django.contrib import admin

from worm_strains.models import (Mutagen, Transgene, WormLab, WormSpecies,
                                 WormStrain, WormStrainLine)


class WormStrainLineInline(admin.StackedInline):
    model = WormStrainLine

    readonly_fields = ('stockable_ptr_id',)

    fields = ('stockable_ptr_id', 'created_internally', 'received_from',
              'received_by', 'date_received', 'times_outcrossed',
              'remarks')


class WormStrainAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'species',
        'genotype',
        'created_by',
        'on_wormbase',
    )

    search_fields = (
        'id',
        'genotype',
        'species__name',
    )

    raw_id_fields = (
        'parent_strain',
        'transgene',
    )

    inlines = [WormStrainLineInline]


class WormLabAdmin(admin.ModelAdmin):
    list_display = (
        'lab',
        'strain_code',
        'allele_code',
    )

    search_fields = (
        'lab',
    )


class TransgeneAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'vector',
    )

    search_fields = (
        'name',
    )

    raw_id_fields = (
        'vector',
    )


admin.site.register(Mutagen)
admin.site.register(Transgene, TransgeneAdmin)
admin.site.register(WormLab, WormLabAdmin)
admin.site.register(WormSpecies)
admin.site.register(WormStrain, WormStrainAdmin)
