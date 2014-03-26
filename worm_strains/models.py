import re

from django.contrib.auth.models import User
from django.db import models

from gunsiano.settings import MARKDOWN_PROMPT
from storage.models import Stockable
from vectors.models import Vector


class WormSpecies(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


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
        if self.is_properly_named() and other.is_properly_named():
            s_code = self.get_lab_code()
            o_code = other.get_lab_code()
            if s_code < o_code:
                return -1
            elif s_code > o_code:
                return 1
            else: # Same lab prefix, so order by number
                if self.get_number() < other.get_number():
                    return -1
                else:
                    return 1
        else: # One or both strains not conventionally named
            s_lower = self.name.lower()
            o_lower = other.name.lower()
            if s_lower < o_lower:
                return -1
            else:
                return 1

    def is_properly_named(self):
        return re.search('^[A-Z]+\d+$', self.name)

    def get_lab_code(self):
        if self.is_properly_named:
            return re.search('^[A-Z]+', self.name).group(0)
        else:
            return None

    def get_number(self):
        if self.is_properly_named:
            return int(re.search('\d+$', self.name).group(0))
        else:
            return None


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
