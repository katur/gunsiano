from django.contrib.auth.models import User
from django.db import models


class Vector(models.Model):
    name = models.CharField(max_length=50, blank=True)
    parent_vector = models.ForeignKey('self', models.SET_NULL,
                                      null=True, blank=True)
    created_by = models.ForeignKey(User, models.SET_NULL,
                                   null=True, blank=True)
    genotype_pattern = models.CharField(max_length=200, blank=True)
    gene = models.CharField(max_length=50, blank=True)
    promoter = models.CharField(max_length=50, blank=True)
    three_prime_utr = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name
