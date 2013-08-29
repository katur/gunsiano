from django.db import models
from website.models import UserProfile
from vectors.models import Vector
from storage.models import Stockable

class WormSpecies(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __unicode__(self):
		return self.name

class Mutagen(models.Model):
	mutagen = models.CharField(max_length=50)
	def __unicode__(self):
		return self.mutagen

class Transgene(models.Model):
	name = models.CharField(max_length=10, blank=True)
	vector = models.ForeignKey(Vector, null=True)
	def __unicode__(self):
		return self.name

class WormLab(models.Model):
	lab = models.CharField(max_length=200)
	strain_code = models.CharField(max_length=5)
	allele_code = models.CharField(max_length=5, blank=True)
	def __unicode__(self):
		return self.lab

class WormStrain(models.Model):
	name = models.CharField(max_length=20, blank=True, unique=True)
	strain_sort = models.CharField(max_length=20, blank=True, unique=True)
	internal_identifier = models.CharField(max_length=30, blank=True)
	on_wormbase = models.BooleanField(default=False)
	species = models.ForeignKey(WormSpecies, default=1)
	genotype = models.CharField(max_length=500, blank=True)
	parent_strain = models.ForeignKey('self', null=True)
	transgene = models.ForeignKey(Transgene, null=True)
	mutagen = models.ForeignKey(Mutagen, null=True)
	date_created = models.DateField(null=True)
	created_by = models.ForeignKey(UserProfile, null=True)
	culture = models.TextField(blank=True)
	remarks = models.TextField(blank=True)
	def __unicode__(self):
		return self.name

class WormStrainLine(models.Model):
	stockable = models.ForeignKey(Stockable, null=True)
	strain = models.ForeignKey(WormStrain)
	received_from = models.CharField(max_length=50, blank=True)
	received_by = models.ForeignKey(UserProfile, null=True)
	date_received = models.DateField(null=True)
	times_outcrossed = models.PositiveSmallIntegerField(null=True)
	remarks = models.TextField(blank=True)
