# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WormStrain'
        db.create_table(u'worm_strains_wormstrain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'worm_strains', ['WormStrain'])


    def backwards(self, orm):
        # Deleting model 'WormStrain'
        db.delete_table(u'worm_strains_wormstrain')


    models = {
        u'worm_strains.wormstrain': {
            'Meta': {'object_name': 'WormStrain'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['worm_strains']