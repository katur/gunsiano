# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Stockable'
        db.create_table(u'storage_stockable', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
        ))
        db.send_create_signal(u'storage', ['Stockable'])


    def backwards(self, orm):
        # Deleting model 'Stockable'
        db.delete_table(u'storage_stockable')


    models = {
        u'storage.stockable': {
            'Meta': {'object_name': 'Stockable'},
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['storage']