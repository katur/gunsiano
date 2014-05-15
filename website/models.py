from django.contrib.auth.models import User
from django.db import models

from gunsiano.settings import MARKDOWN_PROMPT


class Position(models.Model):
    position = models.CharField(max_length=50)
    display_order = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return self.position


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    position = models.ForeignKey(Position)

    # True for Abu Dhabi, False for NYC, null for both
    in_abu_dhabi = models.NullBooleanField()

    # Whether to show as current on Lab Members page
    is_current = models.BooleanField(default=True)

    net_id = models.CharField(max_length=25, blank=True)
    url = models.URLField(blank=True)
    image_filename = models.CharField(max_length=100, blank=True)
    blurb = models.TextField('Blurb', help_text=MARKDOWN_PROMPT, blank=True)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']

    def __unicode__(self):
        return self.user.get_full_name()

    def get_first_name(self):
        return self.user.first_name

    def get_last_name(self):
        return self.user.last_name

    def get_location(self):
        if self.in_abu_dhabi == 1:
            return 'NYUAD'
        elif self.in_abu_dhabi == 0:
            return 'NYUNY'
        else:
            return 'NYUAD/NY'


class ResearchArea(models.Model):
    name = models.CharField(max_length=60, unique=True)
    description = models.TextField('Description', help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Resource(models.Model):
    name = models.CharField(max_length=40, unique=True)
    display_order = models.PositiveSmallIntegerField(unique=True)
    logo_filename = models.CharField(max_length=50, blank=True)
    url = models.CharField(max_length=100, blank=True)
    description = models.TextField('Description', help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return self.name


class JoinLabSection(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField('Description', help_text=MARKDOWN_PROMPT)
    display_order = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ['display_order']

    def __unicode__(self):
        return self.title
