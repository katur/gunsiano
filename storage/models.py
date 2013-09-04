from django.db import models
from website.models import UserProfile

class Stockable(models.Model):
	id = models.IntegerField(primary_key=True)

class Stock(models.Model):
	stockable = models.ForeignKey(Stockable, null=True)
	concentration = models.CharField(max_length=30, blank=True)
	prepared_by = models.ForeignKey(UserProfile, null=True)
	date_prepared = models.DateField(null=True)
	notes = models.TextField(blank=True)

class ContainerSupertype(models.Model):
	name = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name

class ContainerType(models.Model):
	supertype = models.ForeignKey(ContainerSupertype, null=True)
	name = models.CharField(max_length=50, blank=True)
	slots_vertical = models.IntegerField(null=True)
	slots_horizontal = models.IntegerField(null=True)
	slot_type = models.ForeignKey(ContainerSupertype, null=True, related_name="container_slot_type")
	image_filename = models.CharField(max_length=30, blank=True)
	def __unicode__(self):
		return self.name

class Container(models.Model):
	type = models.ForeignKey(ContainerType, null=True)
	name = models.CharField(max_length=200, blank=True)
	notes = models.TextField(blank=True)
	parent = models.ForeignKey('self', null=True)
	vertical_position = models.PositiveSmallIntegerField(null=True)
	horizontal_position = models.PositiveSmallIntegerField(null=True)
	owner = models.ForeignKey(UserProfile, null=True)
	stock = models.ForeignKey(Stock, null=True)
	is_thawed = models.BooleanField(default=False)
	thawed_by = models.ForeignKey(UserProfile, null=True, related_name="container_thawed_by")
	date_thawed = models.DateField(null=True)
	thaw_results = models.CharField(max_length=100, blank=True)
	def __unicode__(self):
		return self.name
