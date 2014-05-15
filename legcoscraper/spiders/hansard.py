from scrapy.spider import Spider, Request
from scrapy.selector import Selector

from legcoscraper.items import QuestionRecordQuestion
from legcoscraper.items import HansardAgenda, HansardMinutes, HansardRecord

import urlparse
import re


class HansardMixin:

    def parse_hansard_index_page(self, response):
        # http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1314.htm

        sel = Selector(response)    

        # Find any dates at the top of this page. Other dates are identical
        # to this page, and indeed the current page will also be included in
        # the date list. Scrapy will prevent us recursing back into ourselves.
    
        year_urls = sel.xpath('//tr/td/a[contains(@href,"#toptbl")]/@href').extract()
        for year_url in year_urls:
            absolute_url = urlparse.urljoin(response.url, year_url.strip())
            req = Request(absolute_url, callback = self.parse_hansard_index_page)
            yield req
        
        # We are looking for table rows which link to Hansard entries for a
        # particular date. In newer versions these are 6-columned table rows
        # where column 6 is a link to a webcast (doesn't seem to exist)
        # Older revisions are 5 columned rows. These are all after the anchor
        # 'hansard'.

        for row in sel.xpath('//tr[count(td)>=5 and preceding::a[@id="hansard"]]'):
            date_info = ' '.join(row.xpath('.//td[1]/node()/text()').extract())

            # Recurse into the agenda, if it exists
            agenda_url = row.xpath('.//td[2]/a/@href').extract()
            if agenda_url:
                absolute_url = urlparse.urljoin(response.url, agenda_url[0].strip())
                req = Request(absolute_url, callback = self.parse_hansard_agenda)
                yield req
        
            # Download the minutes document if it exists. This is a PDF file
            minutes_url = row.xpath('.//td[3]/a/@href').extract()
            if minutes_url:
                absolute_url = urlparse.urljoin(response.url, minutes_url[0].strip())
                minutes = HansardMinutes()
                minutes['date'] = date_info
                minutes['file_urls'] = [absolute_url]
                yield minutes

            for (lang, index) in [('en',4),('cn',5)]:

                hansard_urls = row.xpath('.//td[%i]/a/@href' % index).extract()
                for url in hansard_urls:
                    # Is this a PDF entry, or do we need to recurse?
                    absolute_url = urlparse.urljoin(response.url, url.strip())
                    if absolute_url.endswith('pdf'):
                        hansard_record = HansardRecord()
                        hansard_record['date'] = date_info
                        hansard_record['language'] = lang
                        hansard_record["file_urls"] = [absolute_url]
                        yield hansard_record
                    else:
                        # Recurse into the HTML handler for the HTML Handard Record Index
                        req = Request(absolute_url, callback = self.parse_hansard_html_record)
                        yield req



    def parse_hansard_agenda(self, response):
        # http://www.legco.gov.hk/yr13-14/english/counmtg/agenda/cm20131009.htm
        # Needs to be completed, large amount of HTML to parse. For now this is
        # just a stub.

        sel = Selector(response)    
        agenda = HansardAgenda()
        agenda['date'] = u' '.join(sel.xpath('//h3[1]/text()').extract())
        yield agenda
        

    def parse_hansard_html_record(self, response):
        # http://www.legco.gov.hk/php/hansard/english/rundown.php?date=2014-01-16&lang=0
        #
        # The HTML record is just an index into a PDF file, and doesn't
        # contain any extra information in itself. We find the PDF link
        # and then download.
        # 
        # <script type="text/javascript">
        #   var HansardID = 12;
        #   var Section = "MEETING SECTIONS";
        #   var PdfLink = "/yr13-14/english/counmtg/hansard/cm0116-translate-e.pdf\\#";
        #
        sel = Selector(response)    
    
        link_re = re.compile('var PdfLink = "(?P<pdf_url>[^\"]+)"')
        config_script = sel.xpath('//script[contains(text(),"PdfLink")]/text()')
        pdf_script_text = config_script.extract()[0]
        match = link_re.search(pdf_script_text)
        pdf_url = match.groupdict()['pdf_url'] 
        pdf_url.replace('\\\\#','')
        absolute_url = urlparse.urljoin(response.url, pdf_url.strip())
        
        hr = HansardRecord()
        hr['file_urls'] = [absolute_url]
        yield hr


