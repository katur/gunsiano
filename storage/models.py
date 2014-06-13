from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils import formats

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
        if result == 'worm strain':
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

    def has_freeze_detail(self):
        return self.prepared_by or self.date_prepared

    def get_freeze_detail(self):
        result = 'Frozen'
        if self.prepared_by:
            result += (' by ' + self.prepared_by.get_full_name())
        if self.date_prepared:
            result += (' on ' + formats.date_format(self.date_prepared))
        return result

    class Meta:
        ordering = ['stockable']

    def __unicode__(self):
        return str(self.stockable)


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

    def has_children(self):
        return self.supertype.has_children

    class Meta:
        ordering = ['supertype', 'name']

    def __unicode__(self):
        return self.name


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

    def has_children(self):
        children = Container.objects.all().filter(parent_id=self.id)
        if children:
            return True
        else:
            return False

    def get_supertype(self):
        return self.type.supertype

    def get_title(self):
        return '{0}: {1}'.format(str(self.get_supertype()), str(self))

    def get_ancestors(self):
        """ Return a list of this tube's ancestors,
        starting with oldest.
        Returns an empty list if no parent.
        """
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return list(reversed(ancestors))

    def get_position_in_box(self):
        if self.vertical_position and self.horizontal_position:
            return '{0}{1}'.format(chr(self.vertical_position + 64),
                                   self.horizontal_position)
        else:
            return None

    def get_ancestor_title(self):
        ancestors = self.get_ancestors()
        ancestors.append(self)
        strings = [ancestor.get_title() for ancestor in ancestors]
        return u' \u2192 '.join(strings)

    def get_overall_position(self):
        """ Return a string of the tube's overall position,
        including any ancestors and the box position
        """
        ancestors = self.get_ancestors()
        strings = [ancestor.get_title() for ancestor in ancestors]
        box_position = self.get_position_in_box()
        if box_position:
            strings.append('Position: ' + box_position)
        return u' \u2192 '.join(strings)

    def has_hover_detail(self):
        return self.owner or self.notes or (self.stock and
                                            self.stock.has_freeze_detail())

    def get_hover_detail(self):
        result = ''
        if self.stock and self.stock.has_freeze_detail():
            result = self.stock.get_freeze_detail()
        else:
            if self.owner:
                result += self.owner.get_full_name()
            if self.owner and self.notes:
                result += ' ('
            if self.notes:
                result += self.notes
            if self.owner and self.notes:
                result += ')'
        return result

    class Meta:
        ordering = ['type', 'name']

    def __unicode__(self):
        if self.name:
            result = self.name
        elif self.stock:
            result = str(self.stock)
        else:
            result = 'unnamed'
        return result
