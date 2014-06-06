from django.contrib import admin

from website.models import (JoinLabSection, Position, ResearchArea, Resource,
                            Publication)


class PositionAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'display_order',
    )

    list_editable = (
        'display_order',
    )


class ResearchAreaAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
    )


class ResourceAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'url',
        'display_order',
    )

    list_editable = (
        'display_order',
    )


class PublicationAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'pubmed_id',
        'date',
    )


class JoinLabSectionAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'display_order',
    )

    list_editable = (
        'display_order',
    )


admin.site.register(Position, PositionAdmin)
admin.site.register(ResearchArea, ResearchAreaAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(JoinLabSection, JoinLabSectionAdmin)
