# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ParsedPerson', fields ['uid']
        db.delete_unique(u'raw_parsedperson', ['uid'])

        # Removing unique constraint on 'ParsedMembership', fields ['uid']
        db.delete_unique(u'raw_parsedmembership', ['uid'])

        # Adding field 'ParsedMembership.person'
        db.add_column(u'raw_parsedmembership', 'person',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='memberships', to=orm['raw.ParsedPerson']),
                      keep_default=False)

        # Adding field 'ParsedMembership.start_date'
        db.add_column(u'raw_parsedmembership', 'start_date',
                      self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2014, 12, 18, 0, 0)),
                      keep_default=False)

        # Adding field 'ParsedMembership.end_date'
        db.add_column(u'raw_parsedmembership', 'end_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'ParsedMembership.method_obtained'
        db.add_column(u'raw_parsedmembership', 'method_obtained',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'ParsedMembership.position'
        db.add_column(u'raw_parsedmembership', 'position',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'ParsedMembership.note'
        db.add_column(u'raw_parsedmembership', 'note',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


        # Changing field 'ParsedMembership.uid'
        db.alter_column(u'raw_parsedmembership', 'uid', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'ParsedPerson.uid'
        db.alter_column(u'raw_parsedperson', 'uid', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):
        # Deleting field 'ParsedMembership.person'
        db.delete_column(u'raw_parsedmembership', 'person_id')

        # Deleting field 'ParsedMembership.start_date'
        db.delete_column(u'raw_parsedmembership', 'start_date')

        # Deleting field 'ParsedMembership.end_date'
        db.delete_column(u'raw_parsedmembership', 'end_date')

        # Deleting field 'ParsedMembership.method_obtained'
        db.delete_column(u'raw_parsedmembership', 'method_obtained')

        # Deleting field 'ParsedMembership.position'
        db.delete_column(u'raw_parsedmembership', 'position')

        # Deleting field 'ParsedMembership.note'
        db.delete_column(u'raw_parsedmembership', 'note')


        # Changing field 'ParsedMembership.uid'
        db.alter_column(u'raw_parsedmembership', 'uid', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True))
        # Adding unique constraint on 'ParsedMembership', fields ['uid']
        db.create_unique(u'raw_parsedmembership', ['uid'])


        # Changing field 'ParsedPerson.uid'
        db.alter_column(u'raw_parsedperson', 'uid', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True))
        # Adding unique constraint on 'ParsedPerson', fields ['uid']
        db.create_unique(u'raw_parsedperson', ['uid'])


    models = {
        'raw.override': {
            'Meta': {'object_name': 'Override'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ref_model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ref_uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'raw.parsedmembership': {
            'Meta': {'object_name': 'ParsedMembership'},
            'deactivate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method_obtained': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'note': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'memberships'", 'to': "orm['raw.ParsedPerson']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'raw.parsedperson': {
            'Meta': {'object_name': 'ParsedPerson'},
            'deactivate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.IntegerField', [], {}),
            'homepage': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'honours_c': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'honours_e': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_c': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_e': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'photo_file': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'place_of_birth': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'title_c': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title_e': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'year_of_birth': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'raw.rawcommittee': {
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
        'raw.rawcommitteemembership': {
            'Meta': {'object_name': 'RawCommitteeMembership'},
            '_committee_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            '_member_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'memberships'", 'null': 'True', 'to': "orm['raw.RawCommittee']"}),
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'memberships'", 'null': 'True', 'to': "orm['raw.RawScheduleMember']"}),
            'membership_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'post_c': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'post_e': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'raw.rawcouncilagenda': {
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
        'raw.rawcouncilhansard': {
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
        'raw.rawcouncilquestion': {
            'Meta': {'ordering': "['-raw_date']", 'object_name': 'RawCouncilQuestion'},
            'asker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'raw_questions'", 'null': 'True', 'to': "orm['raw.RawMember']"}),
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'number_and_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'raw_asker': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'raw_date': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'reply_link': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subject': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'subject_link': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'raw.rawcouncilvoteresult': {
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
        'raw.rawmeeting': {
            'Meta': {'object_name': 'RawMeeting'},
            'agenda_url_c': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'agenda_url_e': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'committees': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'meetings'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['raw.RawCommittee']"}),
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
        'raw.rawmeetingcommittee': {
            'Meta': {'object_name': 'RawMeetingCommittee'},
            '_committee_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'committee': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'meeting_committees'", 'null': 'True', 'to': "orm['raw.RawCommittee']"}),
            'crawled_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_crawled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_parsed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'slot_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'uid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'raw.rawmember': {
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
        'raw.rawschedulemember': {
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
        'raw.scrapejob': {
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