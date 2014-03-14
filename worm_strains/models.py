from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from vectors.models import Vector
from storage.models import Stockable
import string, re


class WormSpecies(models.Model):
  name = models.CharField(max_length=50, unique=True)

  class Meta:
    ordering = ["name"]

  def __unicode__(self):
    return self.name


class Mutagen(models.Model):
  mutagen = models.CharField(max_length=50)

  class Meta:
    ordering = ["mutagen"]

  def __unicode__(self):
    return self.mutagen


class Transgene(models.Model):
  name = models.CharField(max_length=10, blank=True)
  vector = models.ForeignKey(Vector, null=True, blank=True)

  class Meta:
    ordering = ["name"]

  def __unicode__(self):
    return self.name


class WormLab(models.Model):
  lab = models.CharField(max_length=200)
  strain_code = models.CharField(max_length=5)
  allele_code = models.CharField(max_length=5, blank=True)

  class Meta:
    ordering = ["lab"]

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
  remarks = models.TextField(blank=True, help_text=settings.MARKDOWN_PROMPT)

  class Meta:
    ordering = ["name"]

  def __unicode__(self):
    return self.name

  def is_properly_named(self):
    return re.search('^[A-Z]+\d+$', self.name)

  def extract_lab_code(self):
    return re.search('^[A-Z]+', self.name).group(0)

  def extract_number(self):
    return int(re.search('\d+$', self.name).group(0))

  def __cmp__(self, other):
    if self.is_properly_named() and other.is_properly_named():
      s_code = self.extract_lab_code()
      o_code = other.extract_lab_code()
      if s_code < o_code:
        return -1
      elif s_code > o_code:
        return 1
      else: # if same lab prefix
        if self.extract_number() < other.extract_number():
          return -1
        else: # strain names must be unique, so necessarily >
          return 1

    else: # if one or both strains are not properly named
      s_lower = self.name.lower()
      o_lower = other.name.lower()
      if s_lower < o_lower:
        return -1
      elif s_lower > o_lower:
        return 1
      else:
        return 0


class WormStrainLine(models.Model):
  strain = models.ForeignKey(WormStrain)
  stockable = models.ForeignKey(Stockable, unique=True)
  created_internally = models.BooleanField(default=False)
  times_outcrossed = models.PositiveSmallIntegerField(null=True, blank=True)
  received_from = models.CharField(max_length=100, blank=True)
  received_by = models.ForeignKey(User, null=True, blank=True)
  date_received = models.DateField(null=True, blank=True)
  remarks = models.TextField(blank=True, help_text=settings.MARKDOWN_PROMPT)

  class Meta:
    ordering = ["strain__name"]

  def __unicode__(self):
    return str(self.strain)
