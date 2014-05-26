# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ScrapeJob'
        db.create_table(u'raw_scrapejob', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spider', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('scheduled', self.gf('django.db.models.fields.DateTimeField')()),
            ('job_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('raw_response', self.gf('django.db.models.fields.TextField')()),
            ('completed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_fetched', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'raw', ['ScrapeJob'])

        # Adding model 'RawCouncilAgenda'
        db.create_table(u'raw_rawcouncilagenda', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_crawled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_parsed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('crawled_from', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('paper_number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('language', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('local_filename', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'raw', ['RawCouncilAgenda'])

        # Adding model 'RawCouncilVoteResult'
        db.create_table(u'raw_rawcouncilvoteresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_crawled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_parsed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('crawled_from', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('raw_date', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('xml_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('xml_filename', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pdf_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('pdf_filename', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'raw', ['RawCouncilVoteResult'])

        # Adding model 'RawCouncilHansard'
        db.create_table(u'raw_rawcouncilhansard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_crawled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_parsed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('crawled_from', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('paper_number', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('language', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('local_filename', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'raw', ['RawCouncilHansard'])

        # Adding model 'RawCouncilQuestion'
        db.create_table(u'raw_rawcouncilquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_crawled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_parsed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('crawled_from', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('raw_date', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('number_and_type', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('raised_by', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('subject', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('subject_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('reply_link', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('language', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'raw', ['RawCouncilQuestion'])


    def backwards(self, orm):
        # Deleting model 'ScrapeJob'
        db.delete_table(u'raw_scrapejob')

        # Deleting model 'RawCouncilAgenda'
        db.delete_table(u'raw_rawcouncilagenda')

        # Deleting model 'RawCouncilVoteResult'
        db.delete_table(u'raw_rawcouncilvoteresult')

        # Deleting model 'RawCouncilHansard'
        db.delete_table(u'raw_rawcouncilhansard')

        # Deleting model 'RawCouncilQuestion'
        db.delete_table(u'raw_rawcouncilquestion')


    models = {
        u'raw.rawcouncilagenda': {
            'Meta': {'object_name': 'RawCouncilAgenda'},
            'crawled_from': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
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
        u'raw.rawcouncilhansard': {
            'Meta': {'object_name': 'RawCouncilHansard'},
            'crawled_from': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
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
            'crawled_from': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
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
            'crawled_from': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
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