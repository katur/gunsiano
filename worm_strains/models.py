from django.db import models
from website.models import UserProfile

class WormSpecies(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name

class Mutagen(models.Model):
	mutagen = models.CharField(max_length=50)
	def __unicode__(self):
		return self.mutagen

class WormStrain(models.Model):
	name = models.CharField(max_length=10, blank=True)
	internal_identifier = models.CharField(max_length=30, blank=True)
	on_wormbase = models.BooleanField(default=False)
	species = models.ForeignKey(WormSpecies, default=1)
	genotype = models.CharField(max_length=500, blank=True)
	genotype_code = models.PositiveIntegerField(null=True)
	mutagen = models.ForeignKey(Mutagen, null=True)
	date_created = models.DateField(null=True)
	created_by = models.ForeignKey(UserProfile, null=True)
	culture = models.TextField(blank=True)
	remarks = models.TextField(blank=True)
	def __unicode__(self):
		return self.name
