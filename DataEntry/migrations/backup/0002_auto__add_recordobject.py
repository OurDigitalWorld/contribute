# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RecordObject'
        db.create_table('DataEntry_recordobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DataEntry.Record'])),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('thumbnail', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('original_file_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('large_file_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('object_height', self.gf('django.db.models.fields.IntegerField')()),
            ('object_width', self.gf('django.db.models.fields.IntegerField')()),
            ('file_size', self.gf('django.db.models.fields.BigIntegerField')()),
            ('file_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('zoomify_folder', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('full_text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('DataEntry', ['RecordObject'])


    def backwards(self, orm):
        # Deleting model 'RecordObject'
        db.delete_table('DataEntry_recordobject')


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
            'file_size': ('django.db.models.fields.BigIntegerField', [], {}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'full_text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'large_file_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_height': ('django.db.models.fields.IntegerField', [], {}),
            'object_width': ('django.db.models.fields.IntegerField', [], {}),
            'original_file_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DataEntry.Record']"}),
            'thumbnail': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'zoomify_folder': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'DataEntry.right': {
            'Meta': {'object_name': 'Right'},
            'cc_description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'cc_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'cccode': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['DataEntry']