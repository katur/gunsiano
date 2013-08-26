from django.db import models

class WormSpecies(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name

class Mutagen(models.Model):
	mutagen = models.CharField(max_length=50)

class WormStrain(models.Model):
	name = models.CharField(max_length=10, blank=True)
	on_wormbase = models.BooleanField(default=False)
	genotype = models.CharField(max_length=500, blank=True)
	date_created = models.DateField(null=True)
	culture = models.TextField(blank=True)
	remarks = models.TextField(blank=True)
	def __unicode__(self):
		return self.name
