# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Developer.skype'
        db.add_column(u'submit_developer', 'skype',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=75, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Developer.skype'
        db.delete_column(u'submit_developer', 'skype')


    models = {
        u'submit.developer': {
            'Meta': {'object_name': 'Developer'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'skype': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
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