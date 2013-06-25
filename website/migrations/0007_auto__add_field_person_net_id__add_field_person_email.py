# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.net_id'
        db.add_column('website_person', 'net_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=25, blank=True),
                      keep_default=False)

        # Adding field 'Person.email'
        db.add_column('website_person', 'email',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.net_id'
        db.delete_column('website_person', 'net_id')

        # Deleting field 'Person.email'
        db.delete_column('website_person', 'email')


    models = {
        'website.person': {
            'Meta': {'object_name': 'Person'},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_abu_dhabi': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'net_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Position']"}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'website.position': {
            'Meta': {'object_name': 'Position'},
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['website']