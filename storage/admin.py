from django.contrib import admin

from storage.models import (Container, ContainerType, ContainerSupertype,
                            Stock)


class ContainerInline(admin.StackedInline):
    model = Container

    raw_id_fields = (
        'parent',
    )

    fields = (
        'type', 'parent', 'vertical_position', 'horizontal_position',
        'is_thawed', 'thawed_by', 'date_thawed', 'thaw_results',
        'name', 'owner', 'notes',
    )


class ContainerAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'parent',
        'vertical_position',
        'horizontal_position',
        'owner',
        'is_thawed',
    )

    list_filter = (
        'type__supertype',
        'owner',
        'is_thawed',
    )

    search_fields = (
        'name',
        'owner__username',
        'owner__first_name',
        'owner__last_name',
    )

    raw_id_fields = (
        'parent',
        'stock',
    )

    fieldsets = (
        (None,
            {'fields': (
                'type', 'name', 'parent', 'vertical_position',
                'horizontal_position', 'owner', 'notes',
            )}),
        ('Relevant for tubes/wells only',
            {'fields': (
                'stock', 'is_thawed', 'thawed_by', 'date_thawed',
                'thaw_results',
            )}),
    )


class ContainerTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'supertype',
        'slots_vertical',
        'slots_horizontal',
    )

    list_filter = (
        'supertype',
    )

    search_fields = (
        'name',
    )


class StockAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'stockable',
        'prepared_by',
        'date_prepared',
    )

    list_filter = (
        'prepared_by',
    )

    raw_id_fields = (
        'stockable',
    )

    readonly_fields = (
        'id',
    )

    fields = (
        'id',
        'stockable',
        'prepared_by',
        'date_prepared',
        'concentration',
        'notes',
    )

    inlines = [ContainerInline]


admin.site.register(Container, ContainerAdmin)
admin.site.register(ContainerSupertype)
admin.site.register(ContainerType, ContainerTypeAdmin)
admin.site.register(Stock, StockAdmin)
