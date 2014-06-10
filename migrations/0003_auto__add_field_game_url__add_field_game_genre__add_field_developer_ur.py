# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Game.url'
        db.add_column(u'submit_game', 'url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Game.genre'
        db.add_column(u'submit_game', 'genre',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Developer.url'
        db.add_column(u'submit_developer', 'url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Developer.notes'
        db.add_column(u'submit_developer', 'notes',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Developer.mailing_address'
        db.add_column(u'submit_developer', 'mailing_address',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Game.url'
        db.delete_column(u'submit_game', 'url')

        # Deleting field 'Game.genre'
        db.delete_column(u'submit_game', 'genre')

        # Deleting field 'Developer.url'
        db.delete_column(u'submit_developer', 'url')

        # Deleting field 'Developer.notes'
        db.delete_column(u'submit_developer', 'notes')

        # Deleting field 'Developer.mailing_address'
        db.delete_column(u'submit_developer', 'mailing_address')


    models = {
        u'submit.developer': {
            'Meta': {'object_name': 'Developer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailing_address': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '140', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'submit.game': {
            'Meta': {'object_name': 'Game'},
            'developer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['submit.Developer']"}),
            'genre': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastyear': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['submit']