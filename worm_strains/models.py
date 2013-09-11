from django.db import models
from django.contrib.auth.models import User
from vectors.models import Vector
from storage.models import Stockable
import string, re


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
	name = models.CharField(max_length=20, primary_key=True)
	on_wormbase = models.BooleanField(default=False)
	species = models.ForeignKey(WormSpecies, default=1)
	genotype = models.CharField(max_length=500, blank=True)
	parent_strain = models.ForeignKey('self', null=True)
	transgene = models.ForeignKey(Transgene, null=True)
	mutagen = models.ForeignKey(Mutagen, null=True)
	date_created = models.DateField(null=True)
	created_by = models.ForeignKey(User, null=True)
	remarks = models.TextField(blank=True)
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
			scode = self.extract_lab_code()
			ocode = other.extract_lab_code()
			if scode < ocode:
				return -1
			elif scode > ocode:
				return 1
			else: # if same lab prefix
				if self.extract_number() < other.extract_number():
					return -1
				else: # strain names must be unique, so necessarily >
					return 1
		else: # if one or both strains are not properly named
			slower = self.name.lower()
			olower = other.name.lower()
			if slower < olower:
				return -1
			elif slower > olower:
				return 1
			else:
				return 0


class WormStrainLine(models.Model):
	stockable = models.ForeignKey(Stockable, null=True)
	strain = models.ForeignKey(WormStrain, null=True)
	created_internally = models.BooleanField(default=False)
	times_outcrossed = models.PositiveSmallIntegerField(null=True)
	received_from = models.CharField(max_length=100, blank=True)
	received_by = models.ForeignKey(User, null=True)
	date_received = models.DateField(null=True)
	remarks = models.TextField(blank=True)
	def __unicode__(self):
		return self.strain.name
