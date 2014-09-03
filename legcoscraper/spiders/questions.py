# -*- coding: utf-8 -*-
"""
Scraper for Council Meeting Questions

From http://www.legco.gov.hk/yr13-14/english/counmtg/question/ques1314.htm#toptbl, for example
"""
from scrapy.item import Field
from scrapy.spider import Spider
from legcoscraper.items import TypedItem


class Question(TypedItem):
    type_name = 'CouncilQuestion'
    source_url = Field()
    number = Field()
    type = Field()
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
