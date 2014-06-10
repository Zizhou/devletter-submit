# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Developer'
        db.create_table(u'submit_developer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=140, blank=True)),
        ))
        db.send_create_signal(u'submit', ['Developer'])

        # Adding model 'Game'
        db.create_table(u'submit_game', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('developer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['submit.Developer'])),
            ('lastyear', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'submit', ['Game'])


    def backwards(self, orm):
        # Deleting model 'Developer'
        db.delete_table(u'submit_developer')

        # Deleting model 'Game'
        db.delete_table(u'submit_game')


    models = {
        u'submit.developer': {
            'Meta': {'object_name': 'Developer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'})
        },
        u'submit.game': {
            'Meta': {'object_name': 'Game'},
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['submit.Developer']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastyear': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['submit']