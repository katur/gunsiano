from django.db import models
from django.shortcuts import get_object_or_404
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
    result = str(self.type)
    if result == "worm strain":
      from worm_strains.models import WormStrainLine
      line = get_object_or_404(WormStrainLine, stockable=self)
      result += " " + str(line)
    return result


class Stock(models.Model):
  stockable = models.ForeignKey(Stockable)
  concentration = models.CharField(max_length=30, blank=True)
  prepared_by = models.ForeignKey(User, null=True, blank=True)
  date_prepared = models.DateField(null=True, blank=True)
  notes = models.TextField(blank=True, help_text=settings.MARKDOWN_PROMPT)

  class Meta:
    ordering = ["stockable"]

  def __unicode__(self):
    result = str(self.stockable)
    if self.date_prepared:
      result += ", " + str(self.date_prepared)
    if self.prepared_by:
      result += ", " + str(self.prepared_by.get_full_name())
    return result


class ContainerSupertype(models.Model):
  name = models.CharField(max_length=20)
  has_children = models.BooleanField(default=False)
  is_outermost = models.BooleanField(default=False)

  class Meta:
    ordering = ["name"]

  def __unicode__(self):
    return self.name


class ContainerType(models.Model):
  name = models.CharField(max_length=50)
  supertype = models.ForeignKey(ContainerSupertype)
  slots_vertical = models.IntegerField(null=True, blank=True)
  slots_horizontal = models.IntegerField(null=True, blank=True)
  slot_type = models.ForeignKey(ContainerSupertype, null=True, blank=True,
      related_name="container_slot_type")
  image_filename = models.CharField(max_length=30, blank=True)

  class Meta:
    ordering = ["supertype", "name"]

  def __unicode__(self):
    return self.name


class Container(models.Model):
  name = models.CharField(max_length=200, blank=True)
  type = models.ForeignKey(ContainerType)
  notes = models.TextField(blank=True, help_text=settings.MARKDOWN_PROMPT)
  parent = models.ForeignKey('self', null=True, blank=True)
  vertical_position = models.PositiveSmallIntegerField(null=True, blank=True)
  horizontal_position = models.PositiveSmallIntegerField(null=True, blank=True)
  owner = models.ForeignKey(User, null=True, blank=True)
  stock = models.ForeignKey(Stock, null=True, blank=True)
  is_thawed = models.BooleanField(default=False)
  thawed_by = models.ForeignKey(User, null=True, blank=True,
      related_name="container_thawed_by")
  date_thawed = models.DateField(null=True, blank=True)
  thaw_results = models.CharField(max_length=100, blank=True)

  class Meta:
    ordering = ["type", "name"]

  def __unicode__(self):
    result = str(self.type.supertype) + ": "
    if self.name:
      result += self.name
    elif self.stock:
      result += str(self.stock)
    else:
      result += "id_" + str(self.id)
    return result
