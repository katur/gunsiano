# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoinLabSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100)),
                ('description', models.TextField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. For subscripts: H~2~0. For superscripts: 6.02 x 10^23^.', verbose_name=b'Description')),
                ('display_order', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['display_order'],
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(max_length=50)),
                ('display_order', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['display_order', 'position'],
                'verbose_name_plural': 'lab member positions',
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pubmed_id', models.PositiveIntegerField(null=True, blank=True)),
                ('title', models.TextField(blank=True)),
                ('authors', models.TextField(blank=True)),
                ('abstract', models.TextField(blank=True)),
                ('journal', models.CharField(max_length=100, blank=True)),
                ('date', models.CharField(max_length=30, blank=True)),
                ('detail', models.CharField(max_length=60, blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name=b'Hide?')),
            ],
        ),
        migrations.CreateModel(
            name='ResearchArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60)),
                ('description', models.TextField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. For subscripts: H~2~0. For superscripts: 6.02 x 10^23^.', verbose_name=b'Description')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'research area blurbs',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=40)),
                ('display_order', models.PositiveSmallIntegerField()),
                ('logo_filename', models.CharField(max_length=50, blank=True)),
                ('url', models.CharField(max_length=100, blank=True)),
                ('description', models.TextField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. For subscripts: H~2~0. For superscripts: 6.02 x 10^23^.', verbose_name=b'Description')),
            ],
            options={
                'ordering': ['display_order'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('in_abu_dhabi', models.NullBooleanField()),
                ('display_on_website', models.BooleanField(default=True)),
                ('is_current', models.BooleanField(default=True)),
                ('net_id', models.CharField(max_length=25, verbose_name=b'NYU NetID', blank=True)),
                ('url', models.URLField(help_text=b'Your public profile will redirect to this URL if your blurb is empty.', verbose_name=b'Personal website URL', blank=True)),
                ('image_filename', models.CharField(max_length=100, blank=True)),
                ('blurb', models.TextField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. For subscripts: H~2~0. For superscripts: 6.02 x 10^23^.', verbose_name=b'Blurb about yourself', blank=True)),
                ('position', models.ForeignKey(to='website.Position')),
            ],
            options={
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
    ]
