# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WormStrainLine.received_from'
        db.add_column(u'worm_strains_wormstrainline', 'received_from',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=50, blank=True),
                      keep_default=False)

        # Adding field 'WormStrainLine.received_by'
        db.add_column(u'worm_strains_wormstrainline', 'received_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.UserProfile'], null=True),
                      keep_default=False)

        # Adding field 'WormStrainLine.date_received'
        db.add_column(u'worm_strains_wormstrainline', 'date_received',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WormStrainLine.received_from'
        db.delete_column(u'worm_strains_wormstrainline', 'received_from')

        # Deleting field 'WormStrainLine.received_by'
        db.delete_column(u'worm_strains_wormstrainline', 'received_by_id')

        # Deleting field 'WormStrainLine.date_received'
        db.delete_column(u'worm_strains_wormstrainline', 'date_received')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'vectors.vector': {
            'Meta': {'object_name': 'Vector'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.UserProfile']", 'null': 'True'}),
            'gene': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'genotype_pattern': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'parent_vector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vectors.Vector']", 'null': 'True'}),
            'promoter': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'three_prime_utr': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'website.position': {
            'Meta': {'object_name': 'Position'},
            'display_order': ('django.db.models.fields.PositiveSmallIntegerField', [], {'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'website.userprofile': {
            'Meta': {'ordering': "['net_id']", 'object_name': 'UserProfile'},
            'blurb': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'image_filename': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'in_abu_dhabi': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'net_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'position': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Position']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'worm_strains.mutagen': {
            'Meta': {'object_name': 'Mutagen'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mutagen': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'worm_strains.transgene': {
            'Meta': {'object_name': 'Transgene'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'vector': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['vectors.Vector']", 'null': 'True'})
        },
        u'worm_strains.wormspecies': {
            'Meta': {'object_name': 'WormSpecies'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'worm_strains.wormstrain': {
            'Meta': {'object_name': 'WormStrain'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.UserProfile']", 'null': 'True'}),
            'culture': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'genotype': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_identifier': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'mutagen': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['worm_strains.Mutagen']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'on_wormbase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent_strain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['worm_strains.WormStrain']", 'null': 'True'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['worm_strains.WormSpecies']"}),
            'strain_sort': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'transgene': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['worm_strains.Transgene']", 'null': 'True'})
        },
        u'worm_strains.wormstrainline': {
            'Meta': {'object_name': 'WormStrainLine'},
            'date_received': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'received_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.UserProfile']", 'null': 'True'}),
            'received_from': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'strain': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['worm_strains.WormStrain']"})
        }
    }

    complete_apps = ['worm_strains']