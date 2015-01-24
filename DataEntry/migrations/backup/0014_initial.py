# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Right'
        db.create_table('DataEntry_right', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cccode', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('cc_label', self.gf('django.db.models.fields.CharField')(null=True, max_length=30)),
            ('cc_description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('cc_url', self.gf('django.db.models.fields.URLField')(null=True, max_length=200)),
        ))
        db.send_create_signal('DataEntry', ['Right'])

        # Adding model 'Record'
        db.create_table('DataEntry_record', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agency_id', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('contributor', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=256)),
            ('contributor_email', self.gf('django.db.models.fields.EmailField')(blank=True, null=True, max_length=75)),
            ('rights', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, null=True, to=orm['DataEntry.Right'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(blank=True, null=True, max_length=100)),
            ('full_text', self.gf('django.db.models.fields.TextField')(blank=True, null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(blank=True, max_length=60)),
        ))
        db.send_create_signal('DataEntry', ['Record'])

        # Adding model 'RecordObject'
        db.create_table('DataEntry_recordobject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DataEntry.Record'])),
            ('record_object_category_id', self.gf('django.db.models.fields.IntegerField')()),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('thumbnail', self.gf('django.db.models.fields.CharField')(null=True, max_length=256)),
            ('original_file_name', self.gf('django.db.models.fields.CharField')(null=True, max_length=256)),
            ('large_file_name', self.gf('django.db.models.fields.CharField')(null=True, max_length=256)),
            ('object_height', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('object_width', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('file_size', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('file_type', self.gf('django.db.models.fields.CharField')(null=True, max_length=10)),
            ('zoomify_folder', self.gf('django.db.models.fields.CharField')(null=True, max_length=256)),
            ('full_text', self.gf('django.db.models.fields.TextField')(null=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
        ))
        db.send_create_signal('DataEntry', ['RecordObject'])

        # Adding model 'Site'
        db.create_table('DataEntry_site', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('site_url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
        ))
        db.send_create_signal('DataEntry', ['Site'])

        # Adding model 'SiteSetup'
        db.create_table('DataEntry_sitesetup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DataEntry.Site'])),
            ('afield', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('avalue', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('DataEntry', ['SiteSetup'])

        # Adding model 'Geography'
        db.create_table('DataEntry_geography', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DataEntry.Record'])),
            ('geonameid', self.gf('django.db.models.fields.BigIntegerField')(blank=True, null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=256)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('relationship', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=20)),
        ))
        db.send_create_signal('DataEntry', ['Geography'])


    def backwards(self, orm):
        # Deleting model 'Right'
        db.delete_table('DataEntry_right')

        # Deleting model 'Record'
        db.delete_table('DataEntry_record')

        # Deleting model 'RecordObject'
        db.delete_table('DataEntry_recordobject')

        # Deleting model 'Site'
        db.delete_table('DataEntry_site')

        # Deleting model 'SiteSetup'
        db.delete_table('DataEntry_sitesetup')

        # Deleting model 'Geography'
        db.delete_table('DataEntry_geography')


    models = {
        'DataEntry.geography': {
            'Meta': {'object_name': 'Geography'},
            'geonameid': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '256'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DataEntry.Record']"}),
            'relationship': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '20'})
        },
        'DataEntry.record': {
            'Meta': {'object_name': 'Record'},
            'agency_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'contributor': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '256'}),
            'contributor_email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'null': 'True', 'max_length': '75'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'full_text': ('django.db.models.fields.TextField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_file': ('django.db.models.fields.files.FileField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'rights': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'to': "orm['DataEntry.Right']"}),
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