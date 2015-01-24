# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RecordObject.record_object_category_id'
        db.add_column('DataEntry_recordobject', 'record_object_category_id',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RecordObject.record_object_category_id'
        db.delete_column('DataEntry_recordobject', 'record_object_category_id')


    models = {
        'DataEntry.record': {
            'Meta': {'object_name': 'Record'},
            'contributor': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '256'}),
            'contributor_email': ('django.db.models.fields.EmailField', [], {'null': 'True', 'max_length': '75'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'full_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'geonameid': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'rights': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['DataEntry.Right']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'DataEntry.recordobject': {
            'Meta': {'object_name': 'RecordObject'},
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'file_size': ('django.db.models.fields.BigIntegerField', [], {}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'full_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'large_file_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_height': ('django.db.models.fields.IntegerField', [], {}),
            'object_width': ('django.db.models.fields.IntegerField', [], {}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DataEntry.Record']"}),
            'record_object_category_id': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'zoomify_folder': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'DataEntry.right': {
            'Meta': {'object_name': 'Right'},
            'cc_description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'cc_label': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '30'}),
            'cc_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'max_length': '200'}),
            'cccode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['DataEntry']