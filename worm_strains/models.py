import re

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import formats

from storage.models import Stockable, Stock
from vectors.models import Vector


class Mutagen(models.Model):
    """
    A mutagen or other technique (e.g. crossing) used to make new worm strains.
    """

    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Transgene(models.Model):
    """
    A transgene in a worm's genotype.
    """

    name = models.CharField(max_length=10, blank=True)
    vector = models.ForeignKey(Vector, models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class WormSpecies(models.Model):
    """
    A worm species (e.g. Caenorhabditis elegans)
    """

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'worm species'

    def __unicode__(self):
        return self.name

    def get_short_name(self):
        parts = self.name.partition(' ')
        genus = parts[0][0]
        species = parts[2]
        return genus + '. ' + species


class WormStrain(models.Model):
    """
    A worm strain (e.g. PF100)
    """

    id = models.CharField(
        max_length=30, primary_key=True,
        help_text=('Since this is the primary key it cannot be edited '
                   'once saved. If you need to edit it, please do '
                   'so in the database directly. You will need to edit '
                   'the worm strain field for any corresponding worm '
                   'strain lines as well, turning off foreign key '
                   'constrains while editing.'))
    species = models.ForeignKey(WormSpecies, models.CASCADE, default=1)
    genotype = models.CharField(
        max_length=500,
        help_text=('If a precise genotype is unavailable or not easily '
                   'written, put something meaningful about what the '
                   'strain is -- e.g. "suppressor of X". If no '
                   'information is available, put "n/a".'))

    on_wormbase = models.BooleanField(
        default=False,
        help_text=('Check this if the strain is on WormBase. In this case, '
                   'aside from genotype and important remarks such as '
                   'temperature sensitivitiy, there is no need to fill '
                   'in the fields which can be found on WormBase.'))

    mutagen = models.ForeignKey(Mutagen, models.SET_NULL,
                                null=True, blank=True)
    created_by = models.ForeignKey(User, models.SET_NULL,
                                   null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, help_text=settings.MARKDOWN_PROMPT)

    # These two fields are disabled in the admin. They were used to
    # generate genotypes automatically for Miyeko's worm strains,
    # but might not be flexible enough going forward.
    parent_strain = models.ForeignKey(
        'self', models.SET_NULL, null=True, blank=True,
        help_text='Worm strain that this strain was made from'
    )
    transgene = models.ForeignKey(Transgene, models.SET_NULL,
                                  null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __unicode__(self):
        return self.id

    def __cmp__(self, other):
        """
        Compare two strains. Don't just order alphabetically, because
        PF99 should precede PF100. If both strains are properly named,
        order by lab code and then by number. If a strain is not
        properly named, just order it alphabetically.
        """
        if self.is_conventionally_named() and other.is_conventionally_named():
            s_code = self.get_lab_code()
            o_code = other.get_lab_code()
            if s_code < o_code:
                return -1
            elif s_code > o_code:
                return 1

            # If same lab prefix, order by number
            else:
                if self.get_number() < other.get_number():
                    return -1
                else:
                    return 1

        # One or both strains not conventionally named
        else:
            s_lower = self.id.lower()
            o_lower = other.id.lower()
            if s_lower < o_lower:
                return -1
            else:
                return 1

    def get_absolute_url(self):
        return reverse('worm_url', args=[self.id])

    def get_wormbase_url(self):
        return ('http://www.wormbase.org/species/c_elegans/'
                'strain/{}'.format(self.id))

    def is_conventionally_named(self):
        """
        Determine whether this strain has a proper strain name.

        Some strains in the database have an placeholder name because
        they haven't received a proper strain name yet.
        """
        return re.search('^[A-Z]+\d+$', self.id)

    def get_lab_code(self):
        """
        Extract the lab code from this strain's name.

        The letters at the beginning of a strain name designate the lab.
        See http://cbs.umn.edu/cgc/lab-code
        """
        if self.is_conventionally_named():
            return re.search('^[A-Z]+', self.id).group(0)
        else:
            return None

    def get_number(self):
        """
        Extract the number from this strain's name.
        """
        if self.is_conventionally_named():
            return int(re.search('\d+$', self.id).group(0))
        else:
            return None

    def generate_genotype(self):
        """
        Return string of genotype by calculating it from transgene name
        and parent strain. If these fields do not exist, return None.
        """
        if self.transgene and self.parent_strain:
            transgene_name = self.transgene.name
            vector = self.transgene.vector
            pattern = ''
            if vector and vector.parent_vector:
                pattern = vector.parent_vector.genotype_pattern
                if pattern and vector.promoter:
                    pattern = pattern.replace('promoter', vector.promoter)
                if pattern and vector.three_prime_utr:
                    pattern = pattern.replace('threePrimeUTR',
                                              vector.three_prime_utr)
                if pattern and vector.gene:
                    pattern = pattern.replace('gene', vector.gene)
            genotype = '{0}[{1}]'.format(transgene_name, pattern)

            if self.parent_strain.id == 'DP38':
                background = 'unc-119(ed3) III;'
            else:
                background = None
            if background:
                genotype = '{0} {1}'.format(background, genotype)

            return genotype

        else:
            return None

    def is_frozen(self):
        """
        Determine if some line of this strain is frozen.
        """
        for line in self.wormstrainline_set.all():
            stocks = Stock.objects.filter(
                stockable=line.stockable_ptr_id)

            for stock in stocks:
                if stock.container_set.exists():
                    return True

        return False


class WormStrainLine(Stockable):
    """
    A particular line of a worm strain.

    While theoretically all worms of the same strain should be alike,
    in practice sometimes a line gets silenced or suffers from other
    issues. So we use WormStrainLine to keep track when we receive
    the "same" strain from multiple place (e.g. from the CGC, from
    another lab, etc).
    """

    strain = models.ForeignKey(WormStrain, models.CASCADE)
    created_internally = models.BooleanField(
        default=False,
        help_text=(
            'Check this if the line was created in our lab. In this case, '
            'the fields about receiving the strain will typically be blank.'))
    times_outcrossed = models.PositiveSmallIntegerField(
        null=True, blank=True)
    received_from = models.CharField(max_length=100, blank=True)
    received_by = models.ForeignKey(User, models.SET_NULL,
                                    null=True, blank=True)
    date_received = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, help_text=settings.MARKDOWN_PROMPT)

    class Meta:
        ordering = ['strain__id']

    def __unicode__(self):
        return '{} Line'.format(self.strain)

    def get_absolute_url(self):
        return self.strain.get_absolute_url()

    def get_receipt_string(self):
        if not (self.received_by or self.received_from or
                self.date_received):
            return ''

        result = 'Line received'
        if self.received_by:
            result += ' by {}'.format(self.received_by.get_full_name())
        if self.received_from:
            result += ' from {}'.format(self.received_from)
        if self.date_received:
            result += ' on {}'.format(formats.date_format(self.date_received))
        return result


class WormLab(models.Model):
    """
    A lab that studies worms.

    This information is available at the CGC:
        http://cbs.umn.edu/cgc/lab-code
    """

    lab = models.CharField(max_length=200)
    strain_code = models.CharField(max_length=5)
    allele_code = models.CharField(max_length=5, blank=True)

    class Meta:
        ordering = ['lab']

    def __unicode__(self):
        return self.lab
