from django.db import models
from django.contrib.auth.models import User

class StockableType(models.Model):
	name = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name

class Stockable(models.Model):
	type = models.ForeignKey(StockableType)
	def __unicode__(self):
		return str(self.id)

class Stock(models.Model):
	stockable = models.ForeignKey(Stockable, null=True)
	concentration = models.CharField(max_length=30, blank=True)
	prepared_by = models.ForeignKey(User, null=True)
	date_prepared = models.DateField(null=True)
	notes = models.TextField(blank=True)
	def __unicode__(self):
		return str(self.stockable) + " " + str(self.date_prepared)

class ContainerSupertype(models.Model):
	name = models.CharField(max_length=20)
	has_children = models.BooleanField(default=False)
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
	owner = models.ForeignKey(User, null=True)
	stock = models.ForeignKey(Stock, null=True)
	is_thawed = models.BooleanField(default=False)
	thawed_by = models.ForeignKey(User, null=True, related_name="container_thawed_by")
	date_thawed = models.DateField(null=True)
	thaw_results = models.CharField(max_length=100, blank=True)
	def __unicode__(self):
		return self.name
