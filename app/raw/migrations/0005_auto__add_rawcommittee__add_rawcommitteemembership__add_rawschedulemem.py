# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RawCommittee'
        db.create_table(u'raw_rawcommittee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_crawled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_parsed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('crawled_from', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('name_e', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name_c', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url_e', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('url_c', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'raw', ['RawCommittee'])

        # Adding model 'RawCommitteeMembership'
        db.create_table(u'raw_rawcommitteemembership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_crawled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_parsed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('crawled_from', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('membership_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('_member_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['raw.RawScheduleMember'], null=True, blank=True)),
            ('_committee_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('committee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['raw.RawCommittee'], null=True, blank=True)),
            ('post_e', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('post_c', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'raw', ['RawCommitteeMembership'])

        # Adding model 'RawScheduleMember'
        db.create_table(u'raw_rawschedulemember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_crawled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_parsed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('crawled_from', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('last_name_c', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('first_name_c', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('last_name_e', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('first_name_e', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('english_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'raw', ['RawScheduleMember'])

        # Adding model 'RawMeeting'
        db.create_table(u'raw_rawmeeting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_crawled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_parsed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('crawled_from', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('meeting_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slot_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('subject_e', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('subject_c', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('agenda_url_e', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('agenda_url_c', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('venue_code', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('meeting_type', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'raw', ['RawMeeting'])


    def backwards(self, orm):
        # Deleting model 'RawCommittee'
        db.delete_table(u'raw_rawcommittee')

        # Deleting model 'RawCommitteeMembership'
        db.delete_table(u'raw_rawcommitteemembership')

        # Deleting model 'RawScheduleMember'
        db.delete_table(u'raw_rawschedulemember')

        # Deleting model 'RawMeeting'
        db.delete_table(u'raw_rawmeeting')


    models = {
        u'raw.rawcommittee': {
            'Meta': {'object_name': 'RawCommittee'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name_c': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name_e': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'url_c': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url_e': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'raw.rawcommitteemembership': {
            'Meta': {'object_name': 'RawCommitteeMembership'},
            '_committee_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_member_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['raw.RawCommittee']", 'null': 'True', 'blank': 'True'}),
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['raw.RawScheduleMember']", 'null': 'True', 'blank': 'True'}),
            'membership_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'post_c': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'post_e': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'raw.rawcouncilagenda': {
            'Meta': {'ordering': "['-uid']", 'object_name': 'RawCouncilAgenda'},
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
        u'raw.rawmeeting': {
            'Meta': {'object_name': 'RawMeeting'},
            'agenda_url_c': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'agenda_url_e': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'meeting_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'meeting_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'slot_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'subject_c': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subject_e': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'venue_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
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
        u'raw.rawschedulemember': {
            'Meta': {'object_name': 'RawScheduleMember'},
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'english_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name_c': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'first_name_e': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_name_c': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'last_name_e': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
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