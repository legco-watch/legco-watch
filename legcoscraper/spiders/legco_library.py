from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider
import urlparse
from legcoscraper.items import LibraryAgenda, LibraryResultPage


class LegcoLibrarySpider(Spider):
    """
    Common methods for library archive pages
    """
    def pagination_links(self, response):
        # Get the pagination links
        # There are two pagination sections, so use only the first one
        sel = Selector(response)
        more_pages = sel.xpath('//td[@class="browsePager"]')[0]
        page_links = more_pages.xpath('./a[@href]/@href').extract()
        for link in page_links:
            absolute_url = urlparse.urljoin(response.url, link.strip())
            # Expects self.parse to be the main parsing loop for browse index pages
            req = Request(absolute_url, callback=self.parse)
            yield req


class LibraryAgendaSpider(LegcoLibrarySpider):
    name = "library_agenda"
    # allowed_domains = ["library.legco.gov.hk"]
    start_urls = [
        # Older agendas are in HTML
        # Newer agendas are in doc format.  Not sure where the break happens
        "http://library.legco.gov.hk:1080/search~S10?/tAgenda+for+the+meeting+of+the+Legislative+Council/tagenda+for+the+meeting+of+the+legislative+council/1%2C670%2C670%2CB/browse",
    ]

    def parse(self, response):
        sel = Selector(response)
        entries = sel.xpath('//tr[@class="browseEntry"]')
        for entry in entries:
            agenda_link = entry.xpath('./td[@class="browseEntryData"]/a[@href]')
            if len(agenda_link) != 1:
                # Should have exactly one link.  Log it if not.
                pass
            link_url = agenda_link.xpath('./@href').extract()[0]
            link_title = agenda_link.xpath('./text()').extract()[0]
            absolute_url = urlparse.urljoin(response.url, link_url.strip())
            # Log the individual result page
            page = LibraryResultPage(
                title=link_title,
                link=absolute_url,
                browse_url=response.url,
                document_type="Agenda"
            )
            yield page

            # Then follow through the request
            req = Request(absolute_url, callback=self.parse_agenda_page)
            yield req

        for link in self.pagination_links(response):
            yield link

    def parse_agenda_page(self, response):
        sel = Selector(response)

        bib_info = sel.xpath('//td[@class="bibInfoData"]/node()/text()').extract()
        title_en = bib_info[2].strip()
        title_cn = bib_info[3].strip()
        links = sel.xpath('//table[@class="bibLinks"]//a')
        links_href = links.xpath('./@href').extract()
        file_urls = [urlparse.urljoin(response.url, l.strip()) for l in links_href]
        links_title = [xx.strip() for xx in links.xpath('.//text()').extract()]
        # Sometimes there are more than just two records, such as for appendices
        # See http://library.legco.gov.hk:1080/search~S10?/tAgenda+for+the+meeting+of+the+Legislative+Council/tagenda+for+the+meeting+of+the+legislative+council/565%2C670%2C670%2CB/frameset&FF=tagenda+for+the+meeting+of+the+legislative+council+2012+++02+++29&1%2C1%2C
        links = zip(links_title, file_urls)

        item = LibraryAgenda(
            title_en=title_en,
            title_cn=title_cn,
            links=links,
            file_urls=file_urls,
            source_url=response.url
        )
        yield item
