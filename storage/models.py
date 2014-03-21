from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404

from gunsiano.settings import MARKDOWN_PROMPT


class StockableType(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Stockable(models.Model):
    type = models.ForeignKey(StockableType)

    def __unicode__(self):
        result = str(self.type)
        if result == "worm strain":
            from worm_strains.models import WormStrainLine
            line = get_object_or_404(WormStrainLine, stockable=self)
            result = str(line)
        return result


class Stock(models.Model):
    stockable = models.ForeignKey(Stockable)
    concentration = models.CharField(max_length=30, blank=True)
    prepared_by = models.ForeignKey(User, null=True, blank=True)
    date_prepared = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['stockable']

    def __unicode__(self):
        result = str(self.stockable)
        date = str(self.date_prepared)
        preparer = self.prepared_by.get_full_name()
        if date:
            result = ", ".join((result, date))
        if preparer:
            result = ", ".join((result, preparer))
        return result


class ContainerSupertype(models.Model):
    name = models.CharField(max_length=20)
    has_children = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ContainerType(models.Model):
    name = models.CharField(max_length=50)
    supertype = models.ForeignKey(ContainerSupertype)
    slots_vertical = models.IntegerField(null=True, blank=True)
    slots_horizontal = models.IntegerField(null=True, blank=True)
    slot_type = models.ForeignKey(ContainerSupertype, null=True, blank=True,
                                  related_name='container_slot_type')
    image_filename = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ['supertype', 'name']

    def __unicode__(self):
        return self.name

    def has_children(self):
        return self.supertype.has_children


class Container(models.Model):
    name = models.CharField(max_length=200, blank=True)
    type = models.ForeignKey(ContainerType)
    parent = models.ForeignKey('self', null=True, blank=True)
    vertical_position = models.PositiveSmallIntegerField(null=True, blank=True)
    horizontal_position = models.PositiveSmallIntegerField(null=True,
                                                           blank=True)
    stock = models.ForeignKey(Stock, null=True, blank=True)
    owner = models.ForeignKey(User, null=True, blank=True)
    is_thawed = models.BooleanField(default=False)
    thawed_by = models.ForeignKey(User, null=True, blank=True,
                                  related_name='container_thawed_by')
    date_thawed = models.DateField(null=True, blank=True)
    thaw_results = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['type', 'name']

    def __unicode__(self):
        supertype = str(self.get_supertype())
        if self.name:
            detail = self.name
        elif self.stock:
            detail = str(self.stock)
        elif self.owner:
            detail = self.owner.get_full_name()
        elif self.notes:
            detail= self.notes
        else:
            detail= "Unnamed Container"
        return "{0}: {1}".format(supertype, detail)

    def has_children(self):
        return self.type.has_children()

    def get_supertype(self):
        return self.type.supertype
