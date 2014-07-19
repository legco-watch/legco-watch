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
