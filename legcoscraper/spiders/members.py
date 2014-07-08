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


class MemberBio(TypedItem):
    type_name = 'LibraryMemberBio'
    language = Field()
    source_url = Field()
    # Basic info
    title = Field()
    name = Field()
    honours = Field()
    gender = Field()
    year_of_birth = Field()
    place_of_birth = Field()
    homepage = Field()
    # Service, as a list of lists
    # [[period, position], [period, position], etc]
    service = Field()
    # Education, as a lists of lists
    education = Field()
    # Occupation as a lists of lists
    occupation = Field()
    # For the headshot
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
        'education_title': u'Education and professional qualifications',
        'occupation_title': u'Occupation',
        'field_map': {
            u'Title': 'title',
            u'Name': 'name',
            u'Honours': 'honours',
            u'Gender': 'gender',
            u'Year of birth': 'year_of_birth',
            u'Place of birth': 'place_of_birth',
            u'Personal homepage': 'homepage'
        }
    }
    KEYWORDS_C = {
        'basic_title': u'基本資料',
        'service_title': u'在立法局／立法會服務期間',
        'education_title': u'學歷及專業資格',
        'occupation_title': u'職業',
        'field_map': {
            u'稱謂': 'title',
            u'姓名': 'name',
            u'勳銜': 'honours',
            u'性別': 'gender',
            u'出生年份': 'year_of_birth',
            u'出生地點': 'place_of_birth',
            u'個人網頁': 'homepage'
        }
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
        res = {'source_url': response.url}
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
            logging.warn(u'Could not infer language from header: {}'.format(header))
            logging.warn(u'Failed parsing of {}'.format(response.url))
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
        if not tables[0].xpath('./tr[1]/td/text()').extract()[0] == kws['basic_title']:
            logging.warn(u'First table not basic information')
            logging.warn(u'Failed parsing of {}'.format(response.url))
            return

        fields = tables[0].xpath('.//table/tr')
        field_names = fields.xpath('./td[1]/text()').extract()
        field_values = fields.xpath('./td[2]/text()').extract()
        # Copy over basic informtaion
        for k, v in zip(field_names, field_values):
            to_field = kws['field_map'].get(k.strip(), None)
            if to_field is None:
                logging.warn(u'Got unknown field {}'.format(k))
                continue
            res[to_field] = v.strip()

        # Get the image
        res['file_urls'] = tables[0].xpath('.//img/@src').extract()

        # Process service
        if not tables[1].xpath('./tr[1]/td/text()').extract()[0] == kws['service_title']:
            logging.warn(u'Second table not LegCo service')
            logging.warn(u'Failed parsing of {}'.format(response.url))
            return

        services = tables[1].xpath('./tr[position() > 1]')
        service_list = []
        for s in services:
            service_list.append(s.xpath('./td/text()').extract())
        res['service'] = service_list

        # Next two tables are optional
        occupation_table = None
        education_table = None
        if len(tables) == 3:
            # If three tables, then only one of occupation or education
            next_table_title = tables[2].xpath('./tr[1]/td/text()').extract()[0]
            if next_table_title == kws['education_title']:
                education_table = tables[2]
            elif next_table_title == kws['occupation_title']:
                occupation_table = tables[2]
            else:
                logging.warn(u'Could not identify table: {}'.format(next_table_title))
        elif len(tables) == 4:
            # If four tables, then should be education then occupation
            third_table = tables[2].xpath('./tr[1]/td/text()').extract()[0]
            if not third_table == kws['education_title']:
                logging.warn(u'Third table was not education: {}'.format(third_table))
            else:
                education_table = tables[2]
            fourth_table = tables[3].xpath('./tr[1]/td/text()').extract()[0]
            if not fourth_table == kws['occupation_title']:
                logging.warn(u'Fourth table was not occupation: {}'.format(fourth_table))
            else:
                occupation_table = tables[3]
        elif len(tables) > 4:
            logging.warn(u'More than four tables present')

        # Now process the optional tables if they're there
        if education_table is not None:
            educations = education_table.xpath('./tr[position() > 1]/td/text()').extract()
            res['education'] = [xx.strip() for xx in educations]

        if occupation_table is not None:
            occupation = occupation_table.xpath('./tr[position() > 1]/td/text()').extract()
            res['occupation'] = [xx.strip() for xx in occupation]

        logging.info(u"Finished scraping member {}".format(res['name']))
        yield MemberBio(**res)
