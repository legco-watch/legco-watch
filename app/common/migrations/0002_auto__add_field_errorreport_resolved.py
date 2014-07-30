# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ErrorReport.resolved'
        db.add_column(u'common_errorreport', 'resolved',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ErrorReport.resolved'
        db.delete_column(u'common_errorreport', 'resolved')


    models = {
        u'common.errorreport': {
            'Meta': {'object_name': 'ErrorReport'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reported': ('django.db.models.fields.DateTimeField', [], {}),
            'resolved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'url': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['common']