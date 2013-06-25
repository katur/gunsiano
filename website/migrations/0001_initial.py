# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Position'
        db.create_table(u'website_position', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('display_order', self.gf('django.db.models.fields.PositiveSmallIntegerField')(unique=True)),
        ))
        db.send_create_signal(u'website', ['Position'])

        # Adding model 'Person'
        db.create_table(u'website_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('full_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('position', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Position'])),
        ))
        db.send_create_signal(u'website', ['Person'])


    def backwards(self, orm):
        # Deleting model 'Position'
        db.delete_table(u'website_position')

        # Deleting model 'Person'
        db.delete_table(u'website_person')


    models = {
        u'website.person': {
            'Meta': {'object_name': 'Person'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Position']"})
        },
        u'website.position': {
            'Meta': {'object_name': 'Position'},
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['website']