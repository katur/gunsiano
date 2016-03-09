from django.contrib import admin

from worm_strains.models import (Mutagen, WormLab, WormSpecies,
                                 WormStrain, WormStrainLine)


class WormStrainLineInline(admin.StackedInline):
    model = WormStrainLine

    readonly_fields = (
        'stockable_ptr_id',
    )

    # Define field order so that readonly stockable_ptr_id is first
    fields = (
        'stockable_ptr_id',
        'created_internally',
        'received_from',
        'received_by',
        'date_received',
        'times_outcrossed',
        'remarks',
    )


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

    fields = (
        'id',
        'species',
        'genotype',
        'on_wormbase',
        'mutagen',
        'created_by',
        'date_created',
        'remarks',
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


admin.site.register(Mutagen)
admin.site.register(WormLab, WormLabAdmin)
admin.site.register(WormSpecies)
admin.site.register(WormStrain, WormStrainAdmin)
