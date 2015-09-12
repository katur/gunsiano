# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('vectors', '0001_initial'),
        ('storage', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mutagen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mutagen', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['mutagen'],
            },
        ),
        migrations.CreateModel(
            name='Transgene',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10, blank=True)),
                ('vector', models.ForeignKey(blank=True, to='vectors.Vector', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WormLab',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lab', models.CharField(max_length=200)),
                ('strain_code', models.CharField(max_length=5)),
                ('allele_code', models.CharField(max_length=5, blank=True)),
            ],
            options={
                'ordering': ['lab'],
            },
        ),
        migrations.CreateModel(
            name='WormSpecies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'worm species',
            },
        ),
        migrations.CreateModel(
            name='WormStrain',
            fields=[
                ('name', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('on_wormbase', models.BooleanField(default=False)),
                ('genotype', models.CharField(max_length=500, blank=True)),
                ('date_created', models.DateField(null=True, blank=True)),
                ('remarks', models.TextField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. For subscripts: H~2~0. For superscripts: 6.02 x 10^23^.', blank=True)),
                ('created_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('mutagen', models.ForeignKey(blank=True, to='worm_strains.Mutagen', null=True)),
                ('parent_strain', models.ForeignKey(blank=True, to='worm_strains.WormStrain', null=True)),
                ('species', models.ForeignKey(default=1, to='worm_strains.WormSpecies')),
                ('transgene', models.ForeignKey(blank=True, to='worm_strains.Transgene', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='WormStrainLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_internally', models.BooleanField(default=False)),
                ('times_outcrossed', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('received_from', models.CharField(max_length=100, blank=True)),
                ('date_received', models.DateField(null=True, blank=True)),
                ('remarks', models.TextField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. For subscripts: H~2~0. For superscripts: 6.02 x 10^23^.', blank=True)),
                ('received_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('stockable', models.ForeignKey(to='storage.Stockable', unique=True)),
                ('strain', models.ForeignKey(to='worm_strains.WormStrain')),
            ],
            options={
                'ordering': ['strain__name'],
            },
        ),
    ]
