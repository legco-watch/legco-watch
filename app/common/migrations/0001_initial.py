# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ErrorReport'
        db.create_table(u'common_errorreport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('reported', self.gf('django.db.models.fields.DateTimeField')()),
            ('url', self.gf('django.db.models.fields.TextField')()),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'common', ['ErrorReport'])


    def backwards(self, orm):
        # Deleting model 'ErrorReport'
        db.delete_table(u'common_errorreport')


    models = {
        u'common.errorreport': {
            'Meta': {'object_name': 'ErrorReport'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reported': ('django.db.models.fields.DateTimeField', [], {}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['common']