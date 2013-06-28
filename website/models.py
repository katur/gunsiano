from django.db import models
from django.contrib.auth.models import User

class Position(models.Model):
	position = models.CharField(max_length=50)
	display_order = models.PositiveSmallIntegerField(unique=True)

class Person(models.Model):
	user = models.ForeignKey(User, unique=True, null=True)
	full_name = models.CharField(max_length=50)
	url_name = models.CharField(max_length=50, unique=True)
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	position = models.ForeignKey(Position)
	in_abu_dhabi = models.NullBooleanField(null=True)
	is_current = models.BooleanField(default=True)
	net_id = models.CharField(max_length=25, blank=True)
	email = models.EmailField(max_length=254, blank=True)
	url = models.URLField(blank=True)
	blurb = models.TextField(blank=True)

	def __unicode__(self):
		return self.full_name

class Resource(models.Model):
	name = models.CharField(max_length=50)
	logo_filename = models.CharField(max_length=50, blank=True)
	url = models.CharField(max_length=100, blank=True)
	description = models.CharField(max_length=300, blank=True)
