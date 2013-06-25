from django.db import models

class Position(models.Model):
	position = models.CharField(max_length=50)
	display_order = models.PositiveSmallIntegerField(unique=True)

class Person(models.Model):
	full_name = models.CharField(max_length=50)
	url_name = models.CharField(max_length=50, unique=True)
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	position = models.ForeignKey(Position)
	in_abu_dhabi = models.NullBooleanField(null=True)
	is_current = models.BooleanField(default=True)
	net_id = models.CharField(max_length=25, blank=True)
	email = models.CharField(max_length=100, blank=True)
	website = models.CharField(max_length=100, blank=True)
	blurb = models.TextField(blank=True)

	def __unicode__(self):
		return self.full_name
