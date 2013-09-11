from django.contrib import admin
from website.models import UserProfile, Position
from protocols.models import Protocol

admin.site.register(Position)
admin.site.register(UserProfile)
admin.site.register(Protocol)
