# -*- coding: utf-8 -*-
"""
Processor for Council Questions
"""
import logging
from urlparse import urljoin
from raw.models import RawCouncilQuestion, LANG_EN, LANG_CN
from raw.processors.base import BaseProcessor, file_wrapper
from django.utils.timezone import now


logger = logging.getLogger('legcowatch')


class QuestionProcessor(BaseProcessor):
    def process(self):
        logger.info("Processing file {}".format(self.items_file_path))
        counter = 0
        # keys are fields in the jsonlines item, values are the fields in the model object
        field_map = {
            'asker': 'raw_asker',
            'reply_link': 'reply_link',
            'number_and_type': 'number_and_type',
            'date': 'raw_date',
            'source_url': 'crawled_from',
            'subject': 'subject',
        }
        for item in file_wrapper(self.items_file_path):
            counter += 1
            # For each question, fill in the raw values, then try to match against a RawMember instance
            obj = RawCouncilQuestion()
            # Generate a uid
            uid = self._generate_uid(item)
            # Fill in the last parsed and last crawled values
            if self.job is not None:
                obj.last_crawled = self.job.completed
            obj.last_parsed = now()
            # Fill in the items that can be copied directly
            for k, v in field_map.items():
                val = item.get(k, None)
                setattr(obj, v, val)
            # the subject_link is sometimes a relative path, so convert it to an absolute url
            subject_link = item.get('subject_link', u'')
            if subject_link != u'':
                abs_url = urljoin(item['source_url'], subject_link)
                obj.subject_link = abs_url
            # Convert the language from the string to the constants
            lang = LANG_CN if item['language'] == u'C' else LANG_EN
            obj.language = lang
            # Try to find the RawMember object that matches the asker
        logger.info("{} items processed, {} created, {} updated, {} errors".format(counter, self._count_created, self._count_updated, self._count_error))

    def _generate_uid(self, item):
        """
        UIDs for questions are of the form 'question-09.10.2013-1-e' (question-<date>-<number>-<lang>)
        """
        pass
