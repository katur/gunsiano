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

class ContainerType(models.Model):
	name = models.CharField(max_length=50, blank=True)
	supertype = models.ForeignKey(ContainerSupertype, null=True)
	slots_vertical = models.IntegerField(null=True)
	slots_horizontal = models.IntegerField(null=True)
	image_filename = models.CharField(max_length=30, blank=True)
	
class Container(models.Model):
	name = models.CharField(max_length=200, blank=True)
	contents = models.CharField(max_length=200, blank=True)
	type = models.ForeignKey(ContainerType, null=True)
	vertical_position = models.PositiveSmallIntegerField(null=True)
	horizontal_position = models.PositiveSmallIntegerField(null=True)
	stock = models.ForeignKey(Stock, null=True)
