# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 21:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0007_auto_20160229_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='stockable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='storage.Stockable'),
        ),
    ]
