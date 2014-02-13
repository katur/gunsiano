from django.db import models
from django.conf import settings
from django.db.models.signals import post_init
from django.contrib.auth.models import User


class Position(models.Model):
	position = models.CharField(max_length=50)
	display_order = models.PositiveSmallIntegerField(unique=True)
	def __unicode__(self):
		return self.position
	class Meta:
		ordering = ["display_order"]


class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	position = models.ForeignKey(Position)

	# True for Abu Dhabi, False for NYC, null for both
	in_abu_dhabi = models.NullBooleanField(null=True)

	# is_current dictates where to show on public Lab Members page
	is_current = models.BooleanField(default=True)
	net_id = models.CharField(max_length=25, blank=True)
	url = models.URLField(blank=True)
	image_filename = models.CharField(max_length=100, blank=True)
	blurb = models.TextField('Blurb',
		help_text = settings.MARKDOWN_ADMIN_PROMPT,
		blank=True
	)

	def __unicode__(self):
		return self.user.get_full_name()

	def first_name(self):
		return self.user.first_name

	def last_name(self):
		return self.user.last_name

	class Meta:
		ordering = ["user__first_name", "user__last_name"]


def add_user_location(**kwargs):
	instance = kwargs.get('instance')
	if instance.in_abu_dhabi:
		instance.location = "NYUAD"
	elif instance.in_abu_dhabi == 0:
		instance.location = "NYUNY"
	else:
		instance.location = "NYUAD/NY"


post_init.connect(add_user_location, UserProfile)


class ResearchArea(models.Model):
	name = models.CharField(max_length=60, unique=True)
	description = models.TextField('Description',
		help_text = settings.MARKDOWN_ADMIN_PROMPT,
	)
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ["name"]


class Resource(models.Model):
	name = models.CharField(max_length=40, unique=True)
	display_order = models.PositiveSmallIntegerField(unique=True)
	logo_filename = models.CharField(max_length=50, blank=True)
	url = models.CharField(max_length=100, blank=True)
	description = models.TextField('Description',
		help_text = settings.MARKDOWN_ADMIN_PROMPT,
	)
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ["display_order"]


class JoinLabSection(models.Model):
	title = models.CharField(max_length=100, unique=True)
	description = models.TextField('Description',
		help_text = settings.MARKDOWN_ADMIN_PROMPT,
	)
	display_order = models.PositiveSmallIntegerField(unique=True)
	def __unicode__(self):
		return self.title
	class Meta:
		ordering = ["display_order"]
