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


class MemberBio(TypedItem):
    type_name = 'LibraryMemberBio'
    language = Field()
    name = Field()
    file_urls = Field()
    files = Field()


class LibraryMemberSpider(Spider):
    name = 'library_member'
    start_urls = [
        'http://app.legco.gov.hk/member_front/english/library/member_search.aspx?surname=&name=&from_day=&from_month=&from_year=&to_day=&to_month=&to_year=&appointed=&elected=&elected_functional=&elected_geographical=&elected_electoralcollege=&btn_submit=Search'
    ]

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
        """
        pass
