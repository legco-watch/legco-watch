# -*- coding: utf-8 -*-
"""
Scrapers for Members' information

See https://docs.google.com/document/d/12IMmSGvUXftSi_ly2cNT4crdTJClF8S8oXygiUiY2vQ/edit
for discussion
"""
from scrapy.http import Request
from scrapy.item import Field
from scrapy.selector import Selector
from scrapy.spider import Spider
from legcoscraper.items import TypedItem
import logging


logger = logging.getLogger('legcowatch')


class MemberBio(TypedItem):
    type_name = 'LibraryMemberBio'
    language = Field()
    source_url = Field()
    title = Field()
    name = Field()
    honorifics = Field()
    gender = Field()
    year_of_birth = Field()
    place_of_birth = Field()
    homepage = Field()
    education = Field()
    occupation = Field()
    file_urls = Field()
    files = Field()


class LibraryMemberSpider(Spider):
    name = 'library_member'
    start_urls = [
        'http://app.legco.gov.hk/member_front/english/library/member_search.aspx?surname=&name=&from_day=&from_month=&from_year=&to_day=&to_month=&to_year=&appointed=&elected=&elected_functional=&elected_geographical=&elected_electoralcollege=&btn_submit=Search'
    ]
    KEYWORDS_E = {
        'basic_title': u'Basic information',
        'service_title': u'Period of LegCo service',
        'field_map': {
            u'Title': 'title',
            u'Name': 'name',
            u'Gender' : 'gender'
        }
    }
    KEYWORDS_C = {
        'basic_title': u'基本資料',
        'service_title': u'在立法局／立法會服務期間'
    }

    def parse(self, response):
        sel = Selector(response)
        entries = sel.xpath('//table[@class="text"]//table//a/@href').extract()
        for entry in entries:
            # Follow to full bio page
            req = Request(entry, callback=self.parse_member)
            yield req
            # Also get the Chinese version
            req = Request(entry.replace('english', 'chinese'), callback=self.parse_member)
            yield req

    def parse_member(self, response):
        """
        Parsing for individual member page, like
        http://app.legco.gov.hk/member_front/english/library/member_detail.aspx?id=602
        This may kick you back to the search index unless you execute a search
        but the scraper should handle it correctly since it'll keep track of the session cookies
        """
        res = {}
        sel = Selector(response)
        # Determine in Chinese or English
        header = u''.join(sel.xpath('//td[@id="pageheader"]//text()').extract()).strip()
        if u'Database' in header:
            res['language'] = 'e'
            kws = self.KEYWORDS_E
        elif u'立法局' in header:
            res['language'] = 'c'
            kws = self.KEYWORDS_C
        else:
            logger.warn(u'Could not infer language from header: {}'.format(header))
            logger.warn(u'Failed parsing of {}'.format(response.url))
            return
        # Content is in a series of nested tables, first row is section header
        tables = sel.xpath('//form[@name="FormSearch"]/table/*/*/table')
        # Order appears to be
        # 1) Basic info
        # 2) Period of service
        # 3) Education
        # 4) Occupation
        # with 3 and 4 optional

        # Process basic info
        if not tables[0].xpath('./tr[1]/td/text()').extract() == kws['basic_title']:
            logger.warn(u'First table not basic information')
            logger.warn(u'Failed parsing of {}'.format(response.url))
            return

        fields = tables[0].xpath('.//table/tr')
        field_names = fields.xpath('./td[1]/text()').extract()
        field_values = fields.xpath('./td[2]/text()').extract()
        # Get the image
        res['file_urls'] = tables[0].xpath('.//img/@src').extract()

        # Process service
        if not tables[1].xpath('./tr[1]/td/text()').extract() == kws['service_title']:
            logger.warn(u'Second table not LegCo service')
            logger.warn(u'Failed parsing of {}'.format(response.url))
            return
