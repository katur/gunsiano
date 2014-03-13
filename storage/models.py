from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class StockableType(models.Model):
	name = models.CharField(max_length=20)
	class Meta:
		ordering = ["name"]
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
	notes = models.TextField(blank=True,
		help_text = settings.MARKDOWN_ADMIN_PROMPT,
	)
	class Meta:
		ordering = ["stockable"]
	def __unicode__(self):
		return str(self.stockable)

class ContainerSupertype(models.Model):
	name = models.CharField(max_length=20)
	has_children = models.BooleanField(default=False)
	class Meta:
		ordering = ["name"]
	def __unicode__(self):
		return self.name

class ContainerType(models.Model):
	name = models.CharField(max_length=50)
	supertype = models.ForeignKey(ContainerSupertype)
	slots_vertical = models.IntegerField(null=True, blank=True)
	slots_horizontal = models.IntegerField(null=True, blank=True)
	slot_type = models.ForeignKey(ContainerSupertype, null=True, blank=True, related_name="container_slot_type")
	image_filename = models.CharField(max_length=30, blank=True)
	class Meta:
		ordering = ["supertype", "name"]
	def __unicode__(self):
		return self.name

class Container(models.Model):
	name = models.CharField(max_length=200, blank=True)
	type = models.ForeignKey(ContainerType)
	notes = models.TextField(blank=True,
		help_text = settings.MARKDOWN_ADMIN_PROMPT,
	)
	parent = models.ForeignKey('self', null=True, blank=True)
	vertical_position = models.PositiveSmallIntegerField(null=True, blank=True)
	horizontal_position = models.PositiveSmallIntegerField(null=True, blank=True)
	owner = models.ForeignKey(User, null=True, blank=True)
	stock = models.ForeignKey(Stock, null=True, blank=True)
	is_thawed = models.BooleanField(default=False)
	thawed_by = models.ForeignKey(User, null=True, blank=True, related_name="container_thawed_by")
	date_thawed = models.DateField(null=True, blank=True)
	thaw_results = models.CharField(max_length=100, blank=True)
	class Meta:
		ordering = ["id"]
	def __unicode__(self):
		return self.name
