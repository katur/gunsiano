from django.contrib import admin

from protocols.models import Protocol


class ProtocolAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'pub_date',
    )

    search_fields = ('title',)

    fields = ('title', 'slug', 'author', 'text',)

    prepopulated_fields = {'slug': ('title',)}

    def save_model(self, request, obj, form, change):
        # Set author to whoever is logged in
        if not obj.author:
            obj.author = request.user

        obj.save()


admin.site.register(Protocol, ProtocolAdmin)
