# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('genotype_pattern', models.CharField(max_length=200, blank=True)),
                ('gene', models.CharField(max_length=50, blank=True)),
                ('promoter', models.CharField(max_length=50, blank=True)),
                ('three_prime_utr', models.CharField(max_length=50, blank=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent_vector', models.ForeignKey(blank=True, to='vectors.Vector', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
