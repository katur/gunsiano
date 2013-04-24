from django.db import models

class Person(models.Model):
	first_name = models.CharField(max_length=25)
	last_name = models.CharField(max_length=25)
	
	def __unicode__(self):
		return self.last_name
