from django.contrib import admin

from vectors.models import Vector


class VectorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'parent_vector',
        'created_by',
        'genotype_pattern',
        'gene',
        'promoter',
        'three_prime_utr',
    )

    list_filter = (
        'created_by',
    )

    raw_id_fields = (
        'parent_vector',
    )


admin.site.register(Vector, VectorAdmin)
