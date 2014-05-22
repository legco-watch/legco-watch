from scrapy.spider import Spider, Request
from scrapy.selector import Selector

from legcoscraper.items import QuestionRecordQuestion, LibraryAgenda
from legcoscraper.items import HansardAgenda, HansardMinutes, HansardRecord

import urlparse
import re

from .hansard import HansardMixin
# from .questions import QuestionsRecordMixin


class LegcoSiteSpider(Spider, HansardMixin):
    name = "legcosite"
    allowed_domains = ["www.legco.gov.hk"]
    start_urls = [
        "http://www.legco.gov.hk/general/english/counmtg/cm1216.htm",           # 2012-2016
        "http://www.legco.gov.hk/general/english/counmtg/cm0812.htm",           # 2008-2012
        "http://www.legco.gov.hk/general/english/counmtg/cm0408.htm",           # 2004-2008
        "http://www.legco.gov.hk/general/english/counmtg/cm0004.htm",           # 2000-2004
        "http://www.legco.gov.hk/yr99-00/english/counmtg/general/counmtg.htm",  # 1998-2000
        # These two entries have significantly different structure. 
        #"http://www.legco.gov.hk/yr97-98/english/counmtg/general/yr9798.htm",   # 1997 - 1998 
        #"http://www.legco.gov.hk/yr97-98/english/former/lc_sitg.htm",           # 1858 - 1997
    ]

    def parse(self, response):
        # Parse a set of records for a the lifetime of a council
        # These normally cover around a 2-6 year period

        sel = Selector(response)    

        proceedings_menu = sel.xpath('//a[starts-with(text(),"Official Record of Proceedings")]/@href')
        for url in proceedings_menu.extract():
            absolute_url = urlparse.urljoin(response.url, url.strip())
            req = Request(absolute_url, callback = self.parse_hansard_index_page)
            yield req


        # Placeholder until the Questions Mixin is completed
    
        # questions_menu = sel.xpath('//a[starts-with(text(),"Questions")]/@href')
        # for url in questions_menu.extract():
        #     absolute_url = urlparse.urljoin(response.url, url.strip())
        #     req = Request(absolute_url, callback = self.parse_questions_page)
        #     yield req

