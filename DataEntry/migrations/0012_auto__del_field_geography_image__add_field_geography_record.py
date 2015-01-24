# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Geography.image'
        db.delete_column('DataEntry_geography', 'image_id')

        # Adding field 'Geography.record'
        db.add_column('DataEntry_geography', 'record',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['DataEntry.Record']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Geography.image'
        db.add_column('DataEntry_geography', 'image',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['DataEntry.Record']),
                      keep_default=False)

        # Deleting field 'Geography.record'
        db.delete_column('DataEntry_geography', 'record_id')


    models = {
        'DataEntry.geography': {
            'Meta': {'object_name': 'Geography'},
            'geonameid': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '256'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DataEntry.Record']"})
        },
        'DataEntry.record': {
            'Meta': {'object_name': 'Record'},
            'agency_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'contributor': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '256'}),
            'contributor_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'null': 'True', 'max_length': '75'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'full_text': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'rights': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DataEntry.Right']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'blank': 'True', 'max_length': '60'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'DataEntry.recordobject': {
            'Meta': {'object_name': 'RecordObject'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'file_size': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'file_type': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '10'}),
            'full_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'large_file_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '256'}),
            'object_height': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'object_width': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '256'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DataEntry.Record']"}),
            'record_object_category_id': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '256'}),
            'zoomify_folder': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '256'})
        },
        'DataEntry.right': {
            'Meta': {'object_name': 'Right'},
            'cc_description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'cc_label': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'}),
            'cc_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200'}),
            'cccode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'DataEntry.site': {
            'Meta': {'object_name': 'Site'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'site_url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'DataEntry.sitesetup': {
            'Meta': {'object_name': 'SiteSetup'},
            'afield': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'avalue': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DataEntry.Site']"})
        }
    }

    complete_apps = ['DataEntry']