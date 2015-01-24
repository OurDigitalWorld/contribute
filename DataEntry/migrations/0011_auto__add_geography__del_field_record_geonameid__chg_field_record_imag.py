# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Geography'
        db.create_table('DataEntry_geography', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DataEntry.Record'])),
            ('geonameid', self.gf('django.db.models.fields.BigIntegerField')(blank=True, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True, null=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
        ))
        db.send_create_signal('DataEntry', ['Geography'])

        # Deleting field 'Record.geonameid'
        db.delete_column('DataEntry_record', 'geonameid')


        # Changing field 'Record.image_file'
        db.alter_column('DataEntry_record', 'image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))

    def backwards(self, orm):
        # Deleting model 'Geography'
        db.delete_table('DataEntry_geography')

        # Adding field 'Record.geonameid'
        db.add_column('DataEntry_record', 'geonameid',
                      self.gf('django.db.models.fields.BigIntegerField')(null=True),
                      keep_default=False)


        # Changing field 'Record.image_file'
        db.alter_column('DataEntry_record', 'image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, default=1))

    models = {
        'DataEntry.geography': {
            'Meta': {'object_name': 'Geography'},
            'geonameid': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DataEntry.Record']"}),
            'latitude': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True', 'null': 'True'})
        },
        'DataEntry.record': {
            'Meta': {'object_name': 'Record'},
            'agency_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'contributor': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True', 'null': 'True'}),
            'contributor_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True', 'null': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'full_text': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True', 'null': 'True'}),
            'rights': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['DataEntry.Right']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'DataEntry.recordobject': {
            'Meta': {'object_name': 'RecordObject'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
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