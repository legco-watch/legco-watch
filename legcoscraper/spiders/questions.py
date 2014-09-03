# -*- coding: utf-8 -*-
"""
Scraper for Council Meeting Questions

From http://www.legco.gov.hk/yr13-14/english/counmtg/question/ques1314.htm#toptbl, for example
"""
from django.utils.encoding import force_str
import logging
from lxml.html import HTMLParser
from scrapy.item import Field
from scrapy.selector import Selector
from scrapy.spider import Spider
import lxml
import re
from legcoscraper.items import TypedItem


class Question(TypedItem):
    type_name = 'CouncilQuestion'
    source_url = Field()
    date = Field()
    number_and_type = Field()
    asker = Field()
    subject = Field()
    subject_link = Field()
    reply_link = Field()
    language = Field()


class QuestionSpider(Spider):
    name = 'council_question'
    start_urls = [
        'http://www.legco.gov.hk/yr13-14/english/counmtg/question/ques1314.htm',
        'http://www.legco.gov.hk/yr12-13/english/counmtg/question/ques1213.htm',
        'http://www.legco.gov.hk/yr11-12/english/counmtg/question/ques1112.htm',
        'http://www.legco.gov.hk/yr10-11/english/counmtg/question/ques1011.htm',
        'http://www.legco.gov.hk/yr09-10/english/counmtg/question/ques0910.htm',
        'http://www.legco.gov.hk/yr08-09/english/counmtg/question/ques0809.htm',
        'http://www.legco.gov.hk/yr07-08/english/counmtg/question/ques0708.htm',
        'http://www.legco.gov.hk/yr06-07/english/counmtg/question/ques0607.htm',
        # These below no longer have links to replies
        # 'http://www.legco.gov.hk/yr05-06/english/counmtg/question/ques0506.htm',
        # 'http://www.legco.gov.hk/yr04-05/english/counmtg/question/ques0405.htm',
        # 'http://www.legco.gov.hk/yr03-04/english/counmtg/question/ques0304.htm',
        # 'http://www.legco.gov.hk/yr02-03/english/counmtg/question/ques0203.htm',
        # 'http://www.legco.gov.hk/yr01-02/english/counmtg/question/ques0102.htm',
        # 'http://www.legco.gov.hk/yr00-01/english/counmtg/question/ques0001.htm',
        # 'http://www.legco.gov.hk/yr99-00/english/counmtg/question/ques9900.htm',
        # 'http://www.legco.gov.hk/yr98-99/english/counmtg/question/question.htm'
    ]
    HEADER_RE = u'Council meeting on (?P<date>[0-9.]+)'

    def parse(self, response):
        sel = Selector(response)
        body = sel.xpath('//div[@id="_content_"]')
        if len(body) != 1:
            logging.warn(u'Expected single body element, but found {} on {}'.format(len(body), response.url))
            return
        body = body[0]
        # Store the number of headers as a check for how many tables of questions we should get out
        # Some dates use h2 and others use h3 for the headers
        num_headers = len(body.xpath('./h2|./h3'))
        # We'll need lxml to parse this
        parser = HTMLParser(encoding='utf-8')
        body_elements = lxml.html.fromstring(force_str(body.extract()), parser=parser)
        # Iterate over the body elements, processing each h2-table pair for each meeting
        count = 0
        for elem in body_elements:
            # Take the first 50 characters, so RE doesn't scan the whole body of text for large elements
            match = re.search(self.HEADER_RE, elem.text_content()[:50])
            if match is not None:
                this_date = match.groupdict()['date']
                questions_table = elem.getnext()
                for row in questions_table:
                    # We ignore the header row, which is indicated by ths
                    if row[0].tag == 'th':
                        continue
                    this_question = {
                        'date': this_date,
                        'source_url': response.url,
                        'number_and_type': row[0].text_content(),
                        'asker': row[1].text_content(),
                        'subject': row[2].text_content(),
                        'subject_link': row[2][0].get('href', None),
                        'reply_link': row[3][0].get('href', None),
                        'language': 'E'
                    }
