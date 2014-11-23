from scrapy.spider import Spider, Request
from scrapy.selector import Selector


import urlparse
import re

from .hansard import HansardMixin


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
#        "http://www.legco.gov.hk/yr97-98/english/counmtg/general/yr9798.htm",   # 1997 - 1998 
#        Not yet implemented
        "http://www.legco.gov.hk/yr97-98/english/former/lc_sitg.htm",           # 1858 - 1997
    ]

    def parse(self, response):
        sel = Selector(response)    

        # Pages from 1998 onwards, new format
        # These normally cover around a 2-6 year period
        proceedings_menu = sel.xpath('//a[starts-with(text(),"Official Record of Proceedings")]/@href')
        if proceedings_menu:
            for url in proceedings_menu.extract():
                absolute_url = urlparse.urljoin(response.url, url.strip())
                req = Request(absolute_url, callback = self.parse_hansard_index_page)
                yield req
        
        # Former Legislative Council (before 7/1997)
        table = sel.xpath("//h3[contains(text(),'Former Legislative Council (before 7/1997)')]/following::table[1]")
        if table:
            links = table[0].xpath(".//td/a[contains(text(),'Session')]/@href").extract()
            if links:
                for url in links:
                    absolute_url = urlparse.urljoin(response.url, url.strip())
                    req = Request(absolute_url, callback = self.parse_hansard_index_page)
                    yield req
            
