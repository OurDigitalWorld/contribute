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
            ('cc_description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('cc_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal('DataEntry', ['Right'])

        # Adding model 'Record'
        db.create_table('DataEntry_record', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True)),
            ('contributor', self.gf('django.db.models.fields.CharField')(max_length=256, null=True)),
            ('contributor_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('rights', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['DataEntry.Right'], null=True)),
            ('geonameid', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('image_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('full_text', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('DataEntry', ['Record'])


    def backwards(self, orm):
        # Deleting model 'Right'
        db.delete_table('DataEntry_right')

        # Deleting model 'Record'
        db.delete_table('DataEntry_record')


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
            'rights': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['DataEntry.Right']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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