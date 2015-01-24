# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RecordObject.zoomify_folder'
        db.alter_column('DataEntry_recordobject', 'zoomify_folder', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'RecordObject.object_width'
        db.alter_column('DataEntry_recordobject', 'object_width', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'RecordObject.file_type'
        db.alter_column('DataEntry_recordobject', 'file_type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True))

        # Changing field 'RecordObject.file_size'
        db.alter_column('DataEntry_recordobject', 'file_size', self.gf('django.db.models.fields.BigIntegerField')(null=True))

        # Changing field 'RecordObject.full_text'
        db.alter_column('DataEntry_recordobject', 'full_text', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'RecordObject.original_file_name'
        db.alter_column('DataEntry_recordobject', 'original_file_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'RecordObject.large_file_name'
        db.alter_column('DataEntry_recordobject', 'large_file_name', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

        # Changing field 'RecordObject.object_height'
        db.alter_column('DataEntry_recordobject', 'object_height', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'RecordObject.thumbnail'
        db.alter_column('DataEntry_recordobject', 'thumbnail', self.gf('django.db.models.fields.CharField')(max_length=256, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'RecordObject.zoomify_folder'
        raise RuntimeError("Cannot reverse this migration. 'RecordObject.zoomify_folder' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'RecordObject.zoomify_folder'
        db.alter_column('DataEntry_recordobject', 'zoomify_folder', self.gf('django.db.models.fields.CharField')(max_length=256))

        # User chose to not deal with backwards NULL issues for 'RecordObject.object_width'
        raise RuntimeError("Cannot reverse this migration. 'RecordObject.object_width' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'RecordObject.object_width'
        db.alter_column('DataEntry_recordobject', 'object_width', self.gf('django.db.models.fields.IntegerField')())

        # User chose to not deal with backwards NULL issues for 'RecordObject.file_type'
        raise RuntimeError("Cannot reverse this migration. 'RecordObject.file_type' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'RecordObject.file_type'
        db.alter_column('DataEntry_recordobject', 'file_type', self.gf('django.db.models.fields.CharField')(max_length=10))

        # User chose to not deal with backwards NULL issues for 'RecordObject.file_size'
        raise RuntimeError("Cannot reverse this migration. 'RecordObject.file_size' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'RecordObject.file_size'
        db.alter_column('DataEntry_recordobject', 'file_size', self.gf('django.db.models.fields.BigIntegerField')())

        # User chose to not deal with backwards NULL issues for 'RecordObject.full_text'
        raise RuntimeError("Cannot reverse this migration. 'RecordObject.full_text' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'RecordObject.full_text'
        db.alter_column('DataEntry_recordobject', 'full_text', self.gf('django.db.models.fields.TextField')())

        # User chose to not deal with backwards NULL issues for 'RecordObject.original_file_name'
        raise RuntimeError("Cannot reverse this migration. 'RecordObject.original_file_name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'RecordObject.original_file_name'
        db.alter_column('DataEntry_recordobject', 'original_file_name', self.gf('django.db.models.fields.CharField')(max_length=256))

        # User chose to not deal with backwards NULL issues for 'RecordObject.large_file_name'
        raise RuntimeError("Cannot reverse this migration. 'RecordObject.large_file_name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'RecordObject.large_file_name'
        db.alter_column('DataEntry_recordobject', 'large_file_name', self.gf('django.db.models.fields.CharField')(max_length=256))

        # User chose to not deal with backwards NULL issues for 'RecordObject.object_height'
        raise RuntimeError("Cannot reverse this migration. 'RecordObject.object_height' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'RecordObject.object_height'
        db.alter_column('DataEntry_recordobject', 'object_height', self.gf('django.db.models.fields.IntegerField')())

        # User chose to not deal with backwards NULL issues for 'RecordObject.thumbnail'
        raise RuntimeError("Cannot reverse this migration. 'RecordObject.thumbnail' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'RecordObject.thumbnail'
        db.alter_column('DataEntry_recordobject', 'thumbnail', self.gf('django.db.models.fields.CharField')(max_length=256))

    models = {
        'DataEntry.record': {
            'Meta': {'object_name': 'Record'},
            'contributor': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'contributor_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
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
            'file_size': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'full_text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'large_file_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'object_height': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'object_width': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DataEntry.Record']"}),
            'record_object_category_id': ('django.db.models.fields.IntegerField', [], {}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'zoomify_folder': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'})
        },
        'DataEntry.right': {
            'Meta': {'object_name': 'Right'},
            'cc_description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'cc_label': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'cc_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'cccode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['DataEntry']