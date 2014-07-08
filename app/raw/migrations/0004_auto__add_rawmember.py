# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RawMember'
        db.create_table(u'raw_rawmember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_crawled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_parsed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('crawled_from', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name_e', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name_c', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('title_e', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('title_c', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('honours_e', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('honours_c', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('gender', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('year_of_birth', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('place_of_birth', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('homepage', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('photo_file', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('service_e', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('service_c', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('education_e', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('education_c', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('occupation_e', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('occupation_c', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'raw', ['RawMember'])


    def backwards(self, orm):
        # Deleting model 'RawMember'
        db.delete_table(u'raw_rawmember')


    models = {
        u'raw.rawcouncilagenda': {
            'Meta': {'object_name': 'RawCouncilAgenda'},
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'local_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'paper_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'raw.rawcouncilhansard': {
            'Meta': {'object_name': 'RawCouncilHansard'},
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'local_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'paper_number': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'raw.rawcouncilquestion': {
            'Meta': {'object_name': 'RawCouncilQuestion'},
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'number_and_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'raised_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'raw_date': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'reply_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subject_link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'raw.rawcouncilvoteresult': {
            'Meta': {'object_name': 'RawCouncilVoteResult'},
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pdf_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'pdf_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'raw_date': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'xml_filename': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'xml_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'raw.rawmember': {
            'Meta': {'object_name': 'RawMember'},
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'education_c': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'education_e': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'homepage': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'honours_c': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'honours_e': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name_c': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'name_e': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'occupation_c': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'occupation_e': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'photo_file': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'place_of_birth': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'service_c': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'service_e': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title_c': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'title_e': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'year_of_birth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'raw.scrapejob': {
            'Meta': {'object_name': 'ScrapeJob'},
            'completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_fetched': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'raw_response': ('django.db.models.fields.TextField', [], {}),
            'scheduled': ('django.db.models.fields.DateTimeField', [], {}),
            'spider': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['raw']