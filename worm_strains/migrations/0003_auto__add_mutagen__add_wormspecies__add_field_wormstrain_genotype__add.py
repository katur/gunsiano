# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mutagen'
        db.create_table(u'worm_strains_mutagen', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mutagen', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'worm_strains', ['Mutagen'])

        # Adding model 'WormSpecies'
        db.create_table(u'worm_strains_wormspecies', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'worm_strains', ['WormSpecies'])

        # Adding field 'WormStrain.genotype'
        db.add_column(u'worm_strains_wormstrain', 'genotype',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=500, blank=True),
                      keep_default=False)

        # Adding field 'WormStrain.date_created'
        db.add_column(u'worm_strains_wormstrain', 'date_created',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'WormStrain.culture'
        db.add_column(u'worm_strains_wormstrain', 'culture',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'WormStrain.remarks'
        db.add_column(u'worm_strains_wormstrain', 'remarks',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Mutagen'
        db.delete_table(u'worm_strains_mutagen')

        # Deleting model 'WormSpecies'
        db.delete_table(u'worm_strains_wormspecies')

        # Deleting field 'WormStrain.genotype'
        db.delete_column(u'worm_strains_wormstrain', 'genotype')

        # Deleting field 'WormStrain.date_created'
        db.delete_column(u'worm_strains_wormstrain', 'date_created')

        # Deleting field 'WormStrain.culture'
        db.delete_column(u'worm_strains_wormstrain', 'culture')

        # Deleting field 'WormStrain.remarks'
        db.delete_column(u'worm_strains_wormstrain', 'remarks')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'on_wormbase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['worm_strains']