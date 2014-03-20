from django.contrib import admin
from slugify import slugify

from protocols.models import Protocol


class ProtocolAdmin(admin.ModelAdmin):
    list_display = (
        'title_markdown',
        'author',
        'pub_date',
    )

    fieldsets = [
        (None, {'fields': [('title_markdown', 'body_markdown')]}),
    ]

    def save_model(self, request, obj, form, change):
        # update the author to whoever is logged in to admin interface
        obj.author = request.user

        # if no url already determined, create it from the title
        if obj.title_url == "":
            obj.title_url = slugify(obj.title_markdown)

        obj.save()


admin.site.register(Protocol, ProtocolAdmin)
