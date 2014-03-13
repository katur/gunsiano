# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Stock.stockable'
        db.alter_column(u'storage_stock', 'stockable_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['storage.Stockable']))

    def backwards(self, orm):

        # Changing field 'Stock.stockable'
        db.alter_column(u'storage_stock', 'stockable_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['storage.Stockable'], null=True))

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
        u'storage.container': {
            'Meta': {'ordering': "['id']", 'object_name': 'Container'},
            'date_thawed': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'horizontal_position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_thawed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['storage.Container']", 'null': 'True', 'blank': 'True'}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['storage.Stock']", 'null': 'True', 'blank': 'True'}),
            'thaw_results': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'thawed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'container_thawed_by'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['storage.ContainerType']"}),
            'vertical_position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'storage.containersupertype': {
            'Meta': {'ordering': "['name']", 'object_name': 'ContainerSupertype'},
            'has_children': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'storage.containertype': {
            'Meta': {'ordering': "['supertype', 'name']", 'object_name': 'ContainerType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_filename': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slot_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'container_slot_type'", 'null': 'True', 'to': u"orm['storage.ContainerSupertype']"}),
            'slots_horizontal': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slots_vertical': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'supertype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['storage.ContainerSupertype']"})
        },
        u'storage.stock': {
            'Meta': {'ordering': "['stockable']", 'object_name': 'Stock'},
            'concentration': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'date_prepared': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'prepared_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'stockable': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['storage.Stockable']"})
        },
        u'storage.stockable': {
            'Meta': {'ordering': "['id']", 'object_name': 'Stockable'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['storage.StockableType']"})
        },
        u'storage.stockabletype': {
            'Meta': {'ordering': "['name']", 'object_name': 'StockableType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['storage']