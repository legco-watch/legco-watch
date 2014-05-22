from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spider import Spider
import urlparse
from legcoscraper.items import LibraryAgenda


class LegcoLibraryAgendaSpider(Spider):
    name = "legco_library_agenda"
    # allowed_domains = ["library.legco.gov.hk"]
    start_urls = [
        "http://library.legco.gov.hk:1080/search~S10?/tAgenda+for+the+meeting+of+the+Legislative+Council/tagenda+for+the+meeting+of+the+legislative+council/1%2C670%2C670%2CB/browse"
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
            absolute_url = urlparse.urljoin(response.url, link_url.strip())
            req = Request(absolute_url, callback=self.parse_agenda_page)
            yield req

    def parse_agenda_page(self, response):
        sel = Selector(response)

        bib_info = sel.xpath('//td[@class="bibInfoData"]/node()/text()').extract()
        title_en = bib_info[2].strip()
        title_cn = bib_info[3].strip()
        links = sel.xpath('//table[@class="bibLinks"]//a')
        links_href = links.xpath('./@href').extract()
        link_en = urlparse.urljoin(response.url, links_href[0].strip())
        link_cn = urlparse.urljoin(response.url, links_href[1].strip())
        link_title = links.xpath('./node()/text()').extract()
        link_title_en = link_title[0].strip()
        link_title_cn = link_title[1].strip()

        item = LibraryAgenda(
            title_en=title_en,
            title_cn=title_cn,
            link_title_en=link_title_en,
            link_title_cn=link_title_cn,
            link_en=link_en,
            link_cn=link_cn,
            file_urls=[link_en, link_cn]
        )
        yield item