from django import forms
from django.contrib import admin

from protocols.models import Protocol


class ProtocolAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProtocolAdminForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget = admin.widgets.AdminTextareaWidget(
            attrs={'cols': 100, 'rows': 20})


class ProtocolAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'pub_date',
    )

    search_fields = (
        'title',
    )

    prepopulated_fields = {
        'slug': ('title',)
    }

    form = ProtocolAdminForm

    def save_model(self, request, obj, form, change):
        # Set author to whoever is logged in
        if not obj.author:
            obj.author = request.user

        obj.save()


admin.site.register(Protocol, ProtocolAdmin)
