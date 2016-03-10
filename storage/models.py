from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models

from utils.models import RealInstanceProvider


class Stockable(models.Model, RealInstanceProvider):
    """
    An entity that can be made into stocks (a particular worm strain line,
    a particular chemical, etc.)
    """

    def __unicode__(self):
        return u'Stockable #{}'.format(self.id)


class Stock(models.Model):
    """
    A stock that was prepared of something Stockable.
    """

    stockable = models.ForeignKey(Stockable, models.CASCADE)
    prepared_by = models.ForeignKey(User, models.SET_NULL,
                                    null=True, blank=True)
    date_prepared = models.DateField(null=True, blank=True)
    concentration = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True, help_text=settings.MARKDOWN_PROMPT)

    class Meta:
        ordering = ['stockable']

    def __unicode__(self):
        return u'Stock #{}'.format(self.id)


class ContainerSupertype(models.Model):
    """
    Broad characterization of a container.

    E.g., "vat", "box", "rack", "tube"
    """

    name = models.CharField(max_length=20)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class ContainerType(models.Model):
    """
    Specific characterization of a container.

    E.g., "9x9 box", "1.5mL tube"
    """

    name = models.CharField(max_length=50)
    supertype = models.ForeignKey(ContainerSupertype, models.CASCADE)
    slots_vertical = models.IntegerField(default=0)
    slots_horizontal = models.IntegerField(default=0)
    image = models.ImageField(upload_to='storage_vats',
                              null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Container(models.Model):
    """
    A container used for storing stocks in the lab.

    A container could be an outermost/largest container (a dewar or
    freezer), an innermost/smallest container (a tube or a well), or
    anything in between (a rack, a box, etc).
    """

    type = models.ForeignKey(ContainerType, models.CASCADE)
    parent = models.ForeignKey('self', models.SET_NULL,
                               null=True, blank=True)
    vertical_position = models.PositiveSmallIntegerField(default=1)
    horizontal_position = models.PositiveSmallIntegerField(default=1)

    name = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(
        User, models.SET_NULL, null=True, blank=True,
        # Need this related name so reverse FK lookup doesn't clash
        # with the other User pointer (thawed_by)
        related_name='owner')

    stock = models.ForeignKey(
        Stock, models.SET_NULL, null=True, blank=True,
        help_text=('If this container is a tube or well, it might hold '
                   'a stock'))
    is_thawed = models.BooleanField(
        default=False,
        help_text=('Check this if this is a tube that was thawed, or '
                   'another type of container that was removed'))
    thawed_by = models.ForeignKey(
        User, models.SET_NULL, null=True, blank=True)
    date_thawed = models.DateField(null=True, blank=True)
    thaw_results = models.CharField(max_length=100, blank=True)

    # TODO: perhaps thaw_results can be recorded in notes
    # TODO: tubes being mislabelled stock-wide should be recorded in stock
    # TODO: perhaps rename "notes" to "remarks", a la worms app
    notes = models.CharField(max_length=200, blank=True,
                             help_text=settings.MARKDOWN_PROMPT)

    class Meta:
        ordering = ['parent__id', 'horizontal_position',
                    'vertical_position']

    def __unicode__(self):
        return u'Container #{}'.format(self.id)

    def get_absolute_url(self):
        return reverse('container_url', args=[self.id])

    def get_stock(self):
        if self.stock:
            return self.stock.stockable.get_actual_instance()

    def get_display_string(self):
        """
        Get a nice display string for this container, which includes
        its supertype.
        """
        if self.name:
            detail = self.name
        elif self.owner:
            detail = self.owner.get_full_name()
        elif self.stock:
            detail = self.get_stock()
        else:
            detail = 'unnamed'
        return '{}: {}'.format(self.get_supertype(), detail)

    def get_supertype(self):
        """
        Get this container's supertype.
        """
        return self.type.supertype

    def has_children(self):
        """
        Determine whether this container has nested children containers.
        """
        return self.container_set.filter(is_thawed=False).exists()

    def get_ancestors(self):
        """
        Get a list of this tube's ancestors, starting with its
        immediate parent.

        Returns an empty list if this container has no parent.
        """
        ancestors = []
        current = self.parent
        while current:
            ancestors.append(current)
            current = current.parent
        return ancestors

    def get_position_within_parent(self):
        """
        Get this container's position within its parent container.

        Format is e.g. 'B6', where 'B' represents the second vertical
        position and '6' represents the sixth horizontal position.

        Returns an empty string if neither vertical nor horizontal
        position is set.
        """
        x = ''
        if self.vertical_position:
            x += chr(self.vertical_position + 64)
        if self.horizontal_position:
            x += str(self.horizontal_position)
        return x
