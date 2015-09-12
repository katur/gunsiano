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
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, blank=True)),
                ('vertical_position', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('horizontal_position', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('is_thawed', models.BooleanField(default=False)),
                ('date_thawed', models.DateField(null=True, blank=True)),
                ('thaw_results', models.CharField(max_length=100, blank=True)),
                ('notes', models.TextField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. For subscripts: H~2~0. For superscripts: 6.02 x 10^23^.', blank=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('parent', models.ForeignKey(blank=True, to='storage.Container', null=True)),
            ],
            options={
                'ordering': ['type', 'name'],
            },
        ),
        migrations.CreateModel(
            name='ContainerSupertype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('has_children', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ContainerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slots_vertical', models.IntegerField(null=True, blank=True)),
                ('slots_horizontal', models.IntegerField(null=True, blank=True)),
                ('image_filename', models.CharField(max_length=30, blank=True)),
                ('slot_type', models.ForeignKey(related_name='container_slot_type', blank=True, to='storage.ContainerSupertype', null=True)),
                ('supertype', models.ForeignKey(to='storage.ContainerSupertype')),
            ],
            options={
                'ordering': ['supertype', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('concentration', models.CharField(max_length=30, blank=True)),
                ('date_prepared', models.DateField(null=True, blank=True)),
                ('notes', models.TextField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. For subscripts: H~2~0. For superscripts: 6.02 x 10^23^.', blank=True)),
                ('prepared_by', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['stockable'],
            },
        ),
        migrations.CreateModel(
            name='Stockable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='StockableType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='stockable',
            name='type',
            field=models.ForeignKey(to='storage.StockableType'),
        ),
        migrations.AddField(
            model_name='stock',
            name='stockable',
            field=models.ForeignKey(to='storage.Stockable'),
        ),
        migrations.AddField(
            model_name='container',
            name='stock',
            field=models.ForeignKey(blank=True, to='storage.Stock', null=True),
        ),
        migrations.AddField(
            model_name='container',
            name='thawed_by',
            field=models.ForeignKey(related_name='container_thawed_by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='container',
            name='type',
            field=models.ForeignKey(to='storage.ContainerType'),
        ),
    ]
