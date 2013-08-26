from django.db import models

class WormStrain(models.Model):
	name = models.CharField(max_length=10)
	def __unicode__(self):
		return self.name
