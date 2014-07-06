from scrapy.spider import Spider, Request
from scrapy.selector import Selector
from scrapy import log

from legcoscraper.items import QuestionRecordQuestion
from legcoscraper.items import HansardAgenda, HansardMinutes, HansardRecord

import urlparse
import re


class HansardMixin:

    def parse_hansard_index_page(self, response):
        """ Parse the handard record for a particular year

            Pages from 1998 onward
            Example: http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1314.htm

            Pages from 1994-1997
            Example: http://www.legco.gov.hk/yr95-96/english/lc_sitg/general/yr9596.htm
            Currently unsupported

            Pages from 1994 and before
            Example: http://www.legco.gov.hk/yr94-95/english/lc_sitg/yr9495.htm
        """
        sel = Selector(response)    

        # First find out what format we are dealing with
    
        if sel.xpath("//table//td/strong[starts-with(text(),'Meetings')]"):
            self.log("%s: HANSARD - Post 1998 Hansard" % response.url, level=log.INFO)
            return self.parse_hansard_post_1998(response)
        elif sel.xpath("//table//td/strong[starts-with(text(),'Hansard')]"):
            self.log("%s: HANSARD - Pre 1995 Hansard" % response.url, level=log.INFO)
            return self.parse_hansard_pre_1995(response)
        elif sel.xpath("//h2[starts-with(text(),'LegCo Sittings')]"):
            self.log("%s: HANSARD - 1995 - 1997 Hansard" % response.url, level=log.INFO)
            self.log("%s: Page type not currently supported" % response.url, level=log.WARNING)
            return self.parse_hansard_1995_to_1997(response)
        else:
            raise Exception("Unknown Hansard page type")

    def parse_hansard_1995_to_1997(self, response):
        sel = Selector(response)    
        return None
        
    def parse_hansard_pre_1995(self, response):
        sel = Selector(response)    
        current_year = ""

        table = sel.xpath("//div[@id='_content_']/ul/table")[0]
        rows = table.xpath(".//tr")
        for entry in rows:
            cells = entry.xpath(".//td")

            # Year is sometimes defined, when a new year starts
            year_str = cells[0].xpath(".//strong/text()").extract()
            if year_str:
                if year_str[0].strip():
                    current_year = year_str[0].strip()
            
            # Month is always defined
            month_str = cells[1].xpath(".//strong/text()").extract()[0].strip()

            for cell in cells[2:]:
                day_str = cell.xpath(".//a/text()").extract()[0].strip()

                date_info = "%s %s %s" % (day_str, month_str, current_year)
        
                # PDF Url
                hansard_url = cell.xpath('.//a/@href').extract()[0]
                absolute_url = urlparse.urljoin(response.url, hansard_url.strip())
                hansard_record = HansardRecord()
                hansard_record['date'] = date_info
                hansard_record['language'] = 'en' # Only english for these records
                hansard_record["file_urls"] = [absolute_url]
                yield hansard_record
            

    def parse_hansard_post_1998(self, response):
        sel = Selector(response)    

        # Get the year that this index page is for
        # Meetings (Year 2013 - 2014)
        # This is mostly for debugging purposes so we can spit this out in the logs
        year_range = sel.xpath('//strong/em/text()').extract()
        if not year_range:
            self.log("%s: Could not find year range on hansard index page" % response.url, level=log.WARNING)
            return
        else:
            self.log("%s: Parsing Hansard Index: %s" % (response.url, year_range), level=log.INFO)

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

        print "Parsing Rows"
        # Find the handsard table
        table = sel.xpath("//div[@class='table_overflow']//a[@name='hansard']/following::table[1]")
        if not table:
            # http://www.legco.gov.hk/general/english/counmtg/yr08-12/mtg_0910.htm
            table = sel.xpath("//div[@id='_content_']//a[@name='hansard']/following::table[1]")

        rows = table.xpath(".//tr[count(td)>=5]")
        if not rows:
            self.log("%s: Could not find any Handard entries to crawl into" % response.url, level=log.WARNING)
            return
    
        self.log("%s: %i rows found" % (response.url, len(rows)), level=log.INFO)

        for row in rows:
            date_info = ' '.join(row.xpath('.//td[1]/node()/text()').extract())
            self.log("%s: Row: %s" % (response.url, date_info), level=log.INFO)

            # Recurse into the agenda, if it exists
            agenda_url = row.xpath('.//td[2]/a/@href').extract()
            if agenda_url:
                absolute_url = urlparse.urljoin(response.url, agenda_url[0].strip())
                req = Request(absolute_url, callback = self.parse_hansard_agenda)
                yield req
            else:
                self.log("%s: Could not find an agenda URL for %s" % (response.url, date_info), level=log.WARNING)
        
            # Download the minutes document if it exists. This is a PDF file
            minutes_url = row.xpath('.//td[3]/a/@href').extract()
            if minutes_url:
                absolute_url = urlparse.urljoin(response.url, minutes_url[0].strip())
                minutes = HansardMinutes()
                minutes['date'] = date_info
                minutes['file_urls'] = [absolute_url]
                yield minutes
            else:
                self.log("%s: Could not find an minutes URL for %s" % (response.url, date_info), level=log.WARNING)

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

                if not hansard_urls:
                    self.log("%s: Could not find an hansard URL for %s, lang %s" % (response.url, date_info, lang), level=log.WARNING)



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
        pdf_url = pdf_url.replace('\\\\#','')
        print "PDF URL", pdf_url
        absolute_url = urlparse.urljoin(response.url, pdf_url.strip())
        
        hr = HansardRecord()
        hr['file_urls'] = [absolute_url]
        yield hr


