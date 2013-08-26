# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WormStrain.on_wormbase'
        db.add_column(u'worm_strains_wormstrain', 'on_wormbase',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WormStrain.on_wormbase'
        db.delete_column(u'worm_strains_wormstrain', 'on_wormbase')


    models = {
        u'worm_strains.wormstrain': {
            'Meta': {'object_name': 'WormStrain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'on_wormbase': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['worm_strains']