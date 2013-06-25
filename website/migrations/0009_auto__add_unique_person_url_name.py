# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Person', fields ['url_name']
        db.create_unique(u'website_person', ['url_name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Person', fields ['url_name']
        db.delete_unique(u'website_person', ['url_name'])


    models = {
        u'website.person': {
            'Meta': {'object_name': 'Person'},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_abu_dhabi': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'net_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Position']"}),
            'url_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'website.position': {
            'Meta': {'object_name': 'Position'},
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['website']