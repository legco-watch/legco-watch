# -*- coding: utf-8 -*-
"""
Scrapers for LegCo meeting schedule API
http://www.legco.gov.hk/odata/english/schedule-db.html

This one should be relatively easy, as it's provided as a JSON API.
"""
import json
from scrapy.item import Field
from scrapy.spider import Spider
from legcoscraper.items import TypedItem


class ScheduleMember(TypedItem):
    type_name = 'ScheduleMember'
    id = Field()
    last_name_c = Field()
    first_name_c = Field()
    last_name_e = Field()
    first_name_e = Field()
    english_name = Field()


class ScheduleMemberSpider(Spider):
    """
    Members from the schedule database.  We need this to get the
    member_id for the members so we can rebuild the relationships
    """
    name = 'schedule_member'
    start_urls = [
        'http://app.legco.gov.hk/ScheduleDB/odata/Tmember'
    ]

    def parse(self, response):
        resp = json.loads(response.body_as_unicode())
        for v in resp['value']:
            res = {
                'id': v['member_id'],
                'last_name_c': v['surname_chi'],
                'first_name_c': v['firstname_chi'],
                'last_name_e': v['surname_eng'],
                'first_name_e': v['firstname_eng'],
                'english_name': v['english_name']
            }
            yield ScheduleMember(**res)


class ScheduleCommittee(TypedItem):
    type_name = 'ScheduleCommittee'
    id = Field()
    code = Field()
    name_e = Field()
    name_c = Field()
    url_e = Field()
    url_c = Field()


class ScheduleCommitteeSpider(Spider):
    """
    Committees from the schedule database.
    """
    name = 'schedule_committee'
    start_urls = [
        'http://app.legco.gov.hk/ScheduleDB/odata/Tcommittee'
    ]

    def parse(self, response):
        resp = json.loads(response.body_as_unicode())
        for v in resp['value']:
            res = {
                'id': v['committee_id'],
                'code': v['committee_code'],
                'name_e': v['name_eng'],
                'name_c': v['name_chi'],
                'url_e': v['home_url_eng'],
                'url_c': v['home_url_chi']
            }
            yield ScheduleCommittee(**res)


class ScheduleMembership(TypedItem):
    type_name = 'ScheduleMembership'
    # Not sure what the difference between membership_id and id are
    id = Field()
    membership_id = Field()
    member_id = Field()
    committee_id = Field()
    post_e = Field()
    post_c = Field()
    start_date = Field()
    end_date = Field()


class ScheduleMembershipSpider(Spider):
    """
    Spider for relationships between members and committees
    """
    name = 'schedule_membership'
    start_urls = [
        'http://app.legco.gov.hk/ScheduleDB/odata/Tmembership'
    ]

    def parse(self, response):
        resp = json.loads(response.body_as_unicode())
        for v in resp['value']:
            res = {
                'id': v['id'],
                'membership_id': v['membership_id'],
                'member_id': v['member_id'],
                'committee_id': int(v['committee_id']),
                'post_e': v['post_eng'],
                'post_c': v['post_chi'],
                'start_date': v['post_start_date'],
                'end_date': v['post_end_date']
            }
            yield ScheduleMembership(**res)


class ScheduleMeeting(TypedItem):
    type_name = 'ScheduleMeeting'
    id = Field()
    slot_id = Field()
    subject_e = Field()
    subject_c = Field()
    agenda_url_e = Field()
    agenda_url_c = Field()
    venue_code = Field()
    meeting_type = Field()
    start_date = Field()


class ScheduleMeetingSpider(Spider):
    """
    Meetings API
    Seems like meetings are allocated to slots, and there is a
    separate table relating slots and committees
    """
    name = 'schedule_meeting'
    start_urls = [
        'http://app.legco.gov.hk/ScheduleDB/odata/Tmeeting'
    ]

    def parse(self, response):
        resp = json.loads(response.body_as_unicode())
        for v in resp['value']:
            res = {
                'id': v['meet_id'],
                'slot_id': int(v['slot_id']),
                'subject_e': v['subject_eng'],
                'subject_c': v['subject_chi'],
                'agenda_url_e': v['agenda_url_eng'],
                'agenda_url_c': v['agenda_url_chi'],
                'venue_code': v['venue_code'],
                'meeting_type': v['meeting_type_eng'],
                'start_date': v['start_date_time']
            }
            yield ScheduleMeeting(**res)


class ScheduleMeetingCommittee(TypedItem):
    type_name = 'ScheduleMeetingCommittee'
    id = Field()
    slot_id = Field()
    committee_id = Field()


class ScheduleMeetingCommitteeSpider(Spider):
    """
    A join table for meetings and committees
    """
    name = 'schedule_meeting_committee'
    start_urls = [
        'http://app.legco.gov.hk/ScheduleDB/odata/Tmeeting_committee'
    ]

    def parse(self, response):
        resp = json.loads(response.body_as_unicode())
        for v in resp['value']:
            res = {
                'id': v['meet_committee_id'],
                'slot_id': int(v['slot_id']),
                'committee_id': int(v['committee_id'])
            }
            yield ScheduleMeetingCommittee(**res)
