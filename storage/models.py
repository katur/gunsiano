from django.db import models
from website.models import UserProfile

class Stockable(models.Model):
	id = models.IntegerField(primary_key=True)

class Stock(models.Model):
	stockable = models.ForeignKey(Stockable, null=True)
	concentration = models.CharField(max_length=30, blank=True)
	prepared_by = models.ForeignKey(UserProfile, null=True)
	date_prepared = models.DateField(null=True)
	notes = models.TextField(blank=True)
