# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-25 23:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocols', '0006_auto_20160225_1809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='protocol',
            name='slug',
            field=models.SlugField(max_length=250, unique=True),
        ),
    ]