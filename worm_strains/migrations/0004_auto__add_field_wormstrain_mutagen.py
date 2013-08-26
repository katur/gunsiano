# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WormStrain.mutagen'
        db.add_column(u'worm_strains_wormstrain', 'mutagen',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['worm_strains.Mutagen'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WormStrain.mutagen'
        db.delete_column(u'worm_strains_wormstrain', 'mutagen_id')


    models = {
        u'worm_strains.mutagen': {
            'Meta': {'object_name': 'Mutagen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mutagen': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'worm_strains.wormspecies': {
            'Meta': {'object_name': 'WormSpecies'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'worm_strains.wormstrain': {
            'Meta': {'object_name': 'WormStrain'},
            'culture': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'genotype': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mutagen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['worm_strains.Mutagen']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'on_wormbase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['worm_strains']