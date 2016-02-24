import re

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import formats

from gunsiano.settings import MARKDOWN_PROMPT
from storage.models import Stockable, Stock, Container
from vectors.models import Vector


class WormSpecies(models.Model):
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


class Mutagen(models.Model):
    mutagen = models.CharField(max_length=50)

    class Meta:
        ordering = ['mutagen']

    def __unicode__(self):
        return self.mutagen


class Transgene(models.Model):
    name = models.CharField(max_length=10, blank=True)
    vector = models.ForeignKey(Vector, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class WormLab(models.Model):
    lab = models.CharField(max_length=200)
    strain_code = models.CharField(max_length=5)
    allele_code = models.CharField(max_length=5, blank=True)

    class Meta:
        ordering = ['lab']

    def __unicode__(self):
        return self.lab


class WormStrain(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    on_wormbase = models.BooleanField(default=False)
    species = models.ForeignKey(WormSpecies, default=1)
    genotype = models.CharField(max_length=500, blank=True)
    parent_strain = models.ForeignKey('self', null=True, blank=True)
    transgene = models.ForeignKey(Transgene, null=True, blank=True)
    mutagen = models.ForeignKey(Mutagen, null=True, blank=True)
    date_created = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True)
    remarks = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

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
            s_lower = self.name.lower()
            o_lower = other.name.lower()
            if s_lower < o_lower:
                return -1
            else:
                return 1

    def get_absolute_url(self):
        return reverse('worm_url', args=[self.name])

    def get_wormbase_url(self):
        return ('http://www.wormbase.org/species/c_elegans/'
                'strain/{}'.format(self.name))

    def is_conventionally_named(self):
        return re.search('^[A-Z]+\d+$', self.name)

    def get_lab_code(self):
        if self.is_conventionally_named():
            return re.search('^[A-Z]+', self.name).group(0)
        else:
            return None

    def get_number(self):
        if self.is_conventionally_named():
            return int(re.search('\d+$', self.name).group(0))
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

            if self.parent_strain.name == 'DP38':
                background = 'unc-119(ed3) III;'
            else:
                background = None
            if background:
                genotype = '{0} {1}'.format(background, genotype)

            return genotype

        else:
            return None

    def is_frozen(self):
        lines = WormStrainLine.objects.filter(strain=self.name)
        for line in lines:
            stocks = Stock.objects.filter(stockable=line.stockable)
            for stock in stocks:
                containers = Container.objects.filter(stock=stock)
                if containers:
                    return True

        return False


class WormStrainLine(models.Model):
    strain = models.ForeignKey(WormStrain)
    stockable = models.ForeignKey(Stockable, unique=True)
    created_internally = models.BooleanField(default=False)
    times_outcrossed = models.PositiveSmallIntegerField(null=True, blank=True)
    received_from = models.CharField(max_length=100, blank=True)
    received_by = models.ForeignKey(User, null=True, blank=True)
    date_received = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True, help_text=MARKDOWN_PROMPT)

    class Meta:
        ordering = ['strain__name']

    def __unicode__(self):
        return str(self.strain)

    def has_receipt_detail(self):
        return self.received_by or self.received_from or self.date_received

    def get_receipt_detail(self):
        result = 'Received'
        if self.received_by:
            result += (' by ' + self.received_by.get_full_name())
        if self.received_from:
            result += (' from ' + self.received_from)
        if self.date_received:
            result += (' on ' + formats.date_format(self.date_received))
        return result
