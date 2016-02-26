from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import formats


class StockableType(models.Model):
    """
    A stockable type (e.g. "worm", "bacteria", etc)
    """
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Stockable(models.Model):
    """
    An entity that can be made into stocks (a particular worm strain line,
    a particular chemical, etc.)
    """
    type = models.ForeignKey(StockableType, models.CASCADE)

    def __unicode__(self):
        return str(self.id)


class Stock(models.Model):
    """
    A stock that was prepared of something Stockable.
    """
    stockable = models.ForeignKey(Stockable, models.CASCADE)
    concentration = models.CharField(max_length=30, blank=True)
    prepared_by = models.ForeignKey(User, models.SET_NULL,
                                    null=True, blank=True)
    date_prepared = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text=settings.MARKDOWN_PROMPT)

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
    """
    Broad characterization of a container (e.g. "vat", "box", "rack", "tube")
    """
    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ContainerType(models.Model):
    """
    Specific characterization of a container (e.g. "9x9 box", "1.5mL tube")
    """
    name = models.CharField(max_length=50)
    supertype = models.ForeignKey(ContainerSupertype, models.CASCADE)
    slots_vertical = models.IntegerField(null=True, blank=True)
    slots_horizontal = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='storage_vats',
                              null=True, blank=True)

    class Meta:
        ordering = ['supertype', 'name']

    def __unicode__(self):
        return self.name


class Container(models.Model):
    """
    A container used for storing stocks in the lab.

    A container could be an outermost/largest container (a dewar or
    freezer), an innermost/smallest container (a tube or a well), or
    anything in between (a rack, a box, etc).
    """
    name = models.CharField(max_length=200, blank=True)
    type = models.ForeignKey(ContainerType, models.CASCADE)
    parent = models.ForeignKey('self', models.SET_NULL,
                               null=True, blank=True)
    vertical_position = models.PositiveSmallIntegerField(
        null=True, blank=True)
    horizontal_position = models.PositiveSmallIntegerField(
        null=True, blank=True)
    owner = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True,
                             help_text=settings.MARKDOWN_PROMPT)

    # Below here are only really relevant for tubes/wells
    stock = models.ForeignKey(Stock, models.SET_NULL,
                              null=True, blank=True)
    is_thawed = models.BooleanField(default=False)
    thawed_by = models.ForeignKey(User, models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='container_thawed_by')
    date_thawed = models.DateField(null=True, blank=True)
    thaw_results = models.CharField(max_length=100, blank=True)

    def has_children(self):
        children = Container.objects.all().filter(parent_id=self.id,
                                                  is_thawed=False)
        if children:
            return True
        else:
            return False

    def get_absolute_url(self):
        return reverse('storage_detail_url', args=[self.id])

    def get_supertype(self):
        return self.type.supertype

    def get_ancestors(self):
        """Get a list of this tube's ancestors, starting with the oldest.
        Returns an empty list if this container has no parent.
        """
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return list(reversed(ancestors))

    def get_title(self):
        """Get a simple title for this container including its supertype"""
        return '{0}: {1}'.format(str(self.get_supertype()), str(self))

    def get_ancestor_title(self):
        """Get a title for this container that includes both
        supertype and ancestors
        """
        ancestors = self.get_ancestors()
        ancestors.append(self)
        strings = [ancestor.get_title() for ancestor in ancestors]
        return u' \u2192 '.join(strings)

    def get_position_in_parent(self):
        """Get this container's position within its parent container
        in format 'B6', where 'B' represents the second vertical position
        and '6' represents the sixth horizontal position
        """
        if self.vertical_position and self.horizontal_position:
            return '{0}{1}'.format(chr(self.vertical_position + 64),
                                   self.horizontal_position)
        else:
            return None

    def get_overall_position(self):
        """Get a string of this container's overall position,
        including both ancestors and this container's position.
        This differs from get_ancestor_title() because it includes this
        container's position rather than this container's title.
        """
        ancestors = self.get_ancestors()
        strings = [ancestor.get_title() for ancestor in ancestors]
        box_position = self.get_position_in_parent()
        if box_position:
            strings.append('Position: ' + box_position)
        return u' \u2192 '.join(strings)

    def has_hover_detail(self):
        """Determine whether there is hover information for this container"""
        return self.owner or self.notes or (self.stock and
                                            self.stock.has_freeze_detail())

    def get_hover_detail(self):
        """Get information to display when hovering over this container"""
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

    def get_thaw_detail(self):
        result = 'Thaw'
        if self.thawed_by:
            result += (' by ' + self.thawed_by.get_full_name())
        if self.date_thawed:
            result += (' on ' + formats.date_format(self.date_thawed))
        if self.thaw_results:
            result += (' was ' + self.thaw_results)
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
