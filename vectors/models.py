from django.db import models
from django.contrib.auth.models import User

class Vector(models.Model):
	name = models.CharField(max_length=50, blank=True)
	parent_vector = models.ForeignKey('self', null=True)
	created_by = models.ForeignKey(User, null=True)
	genotype_pattern = models.CharField(max_length=200, blank=True)
	gene = models.CharField(max_length=50, blank=True)
	promoter = models.CharField(max_length=50, blank=True)
	three_prime_utr = models.CharField(max_length=50, blank=True)
	class Meta:
		ordering = ["id"]
	def __unicode__(self):
		return self.name
