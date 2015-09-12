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
            name='Protocol',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_markdown', models.CharField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. For subscripts: H~2~0. For superscripts: 6.02 x 10^23^.', unique=True, max_length=250, verbose_name=b'Title')),
                ('title_url', models.CharField(unique=True, max_length=250)),
                ('pub_date', models.DateField(auto_now=True, verbose_name=b'Publication Date')),
                ('body_markdown', models.TextField(help_text=b'Use Markdown syntax for italics, bullets, etc. See <a href="http://www.darkcoding.net/software/markdown-quick-reference">a quick reference</a>, <a href="http://www.markdowntutorial.com/">a tutorial</a>, or practice <a href="http://dillinger.io/">here</a>. For subscripts: H~2~0. For superscripts: 6.02 x 10^23^.', verbose_name=b'Body')),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, help_text=b'If none selected, will default to logged in user.', null=True)),
            ],
        ),
    ]
