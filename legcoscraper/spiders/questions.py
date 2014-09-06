# -*- coding: utf-8 -*-
"""
Scraper for Council Meeting Questions

From http://www.legco.gov.hk/yr13-14/english/counmtg/question/ques1314.htm#toptbl, for example
"""
from lxml.html import HTMLParser
from scrapy.item import Field
from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy import log
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
        # English
        'http://www.legco.gov.hk/yr13-14/english/counmtg/question/ques1314.htm',
        'http://www.legco.gov.hk/yr12-13/english/counmtg/question/ques1213.htm',
        'http://www.legco.gov.hk/yr11-12/english/counmtg/question/ques1112.htm',
        'http://www.legco.gov.hk/yr10-11/english/counmtg/question/ques1011.htm',
        'http://www.legco.gov.hk/yr09-10/english/counmtg/question/ques0910.htm',
        'http://www.legco.gov.hk/yr08-09/english/counmtg/question/ques0809.htm',
        'http://www.legco.gov.hk/yr07-08/english/counmtg/question/ques0708.htm',
        'http://www.legco.gov.hk/yr06-07/english/counmtg/question/ques0607.htm',
        # Chinese
        'http://www.legco.gov.hk/yr13-14/chinese/counmtg/question/ques1314.htm',
        'http://www.legco.gov.hk/yr12-13/chinese/counmtg/question/ques1213.htm',
        'http://www.legco.gov.hk/yr11-12/chinese/counmtg/question/ques1112.htm',
        'http://www.legco.gov.hk/yr10-11/chinese/counmtg/question/ques1011.htm',
        'http://www.legco.gov.hk/yr09-10/chinese/counmtg/question/ques0910.htm',
        'http://www.legco.gov.hk/yr08-09/chinese/counmtg/question/ques0809.htm',
        'http://www.legco.gov.hk/yr07-08/chinese/counmtg/question/ques0708.htm',
        'http://www.legco.gov.hk/yr06-07/chinese/counmtg/question/ques0607.htm',
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
    HEADER_RE_E = u'Council meeting on (?P<date>[0-9.]+)'
    HEADER_RE_C = u'會議日期\s*(?P<date>[0-9.]+)'

    def make_question(self, language, response, row, this_date):
        """
        Given a question row, create a dict with the question fields
        """
        # Sometimes replies don't have links
        this_question = {
            'date': this_date,
            'source_url': response.url,
            'number_and_type': row[0].text_content(),
            'asker': row[1].text_content(),
            'subject': row[2].text_content(),
            'subject_link': row[2][0].get('href', None),
            'language': language
        }
        try:
            this_question['reply_link'] = row[3][0].get('href', None)
        except IndexError:
            self.log(u'No reply link on {} from {}'.format(response.url, this_date), level=log.WARNING)
        return this_question

    def parse(self, response):
        sel = Selector(response)
        body = sel.xpath('//div[@id="_content_"]')
        if len(body) != 1:
            self.log(u'Expected single body element, but found {} on {}'.format(len(body), response.url), level=log.WARNING)
            return
        body = body[0]
        # Store the number of headers as a check for how many tables of questions we should get out
        # Some dates use h2 and others use h3 for the headers
        num_headers = len(body.xpath('./h2|./h3'))
        if u'chinese' in response.url:
            language = 'C'
            matcher = self.HEADER_RE_C
        else:
            language = 'E'
            matcher = self.HEADER_RE_E
        # We'll need lxml to parse this
        parser = HTMLParser(encoding='utf-8')
        body_extract = body.extract().encode('utf-8')
        body_elements = lxml.html.fromstring(body_extract, parser=parser)
        # Iterate over the body elements, processing each h2-table pair for each meeting
        count_sessions = 0
        count_questions = 0
        for elem in body_elements:
            # Skip comments
            if elem.tag == lxml.etree.Comment:
                continue
            # Take the first 50 characters, so RE doesn't scan the whole body of text for large elements
            match = re.search(matcher, elem.text_content()[:50])
            if match is not None:
                this_date = match.groupdict()['date']
                count_sessions += 1
                questions_table = elem.getnext()
                for row in questions_table.xpath('./tr'):
                    # We ignore the header row, which is indicated by ths
                    if row[0].tag == 'th':
                        continue
                    this_question = self.make_question(language, response, row, this_date)
                    count_questions += 1
                    yield Question(**this_question)

        if num_headers != count_sessions:
            self.log(u'Expected {} sessions on {}, but only found tables for {}'.format(num_headers, response.url, count_sessions), level=log.WARNING)
        self.log(u'Processed {} questions in {} sessions'.format(count_questions, count_sessions), level=log.INFO)
