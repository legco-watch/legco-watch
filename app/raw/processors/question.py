# -*- coding: utf-8 -*-
"""
Processor for Council Questions
"""
import logging
from urlparse import urljoin
import re
from raw.models import RawCouncilQuestion, LANG_EN, LANG_CN, RawMember
from raw.names import MemberName
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
        matcher_en = RawMember.get_matcher()
        matcher_cn = RawMember.get_matcher(False)
        for item in file_wrapper(self.items_file_path):
            try:
                counter += 1
                # For each question, fill in the raw values, then try to match against a RawMember instance

                # Generate a uid and get the object
                uid = self._generate_uid(item)
                obj, created = RawCouncilQuestion.objects.get_or_create(uid=uid)
                if created:
                    self._count_created += 1
                else:
                    self._count_updated += 1

                # Fill in the last parsed and last crawled values
                if self.job is not None:
                    obj.last_crawled = self.job.completed
                obj.last_parsed = now()

                # Fill in the items that can be copied directly
                for k, v in field_map.items():
                    val = item.get(k, None)
                    setattr(obj, v, val)

                if obj.reply_link is None:
                    obj.reply_link = u''

                # the subject_link is sometimes a relative path, so convert it to an absolute url
                subject_link = item.get('subject_link', u'')
                if subject_link != u'':
                    abs_url = urljoin(item['source_url'], subject_link)
                    obj.subject_link = abs_url

                # Convert the language from the string to the constants
                lang = LANG_CN if item['language'] == u'C' else LANG_EN
                obj.language = lang
                if lang == LANG_CN:
                    matcher = matcher_cn
                else:
                    matcher = matcher_en

                # Try to find the RawMember object that matches the asker
                raw_name = item['asker']
                name = MemberName(raw_name)
                match = matcher.match(name)
                if match is not None:
                    member = match[1]
                    obj.asker = member

                # Finally save
                obj.save()
            except (KeyError, RuntimeError) as e:
                self._count_error += 1
                logger.warn(u'Could not process question {} from date {}'.format(item['number_and_type'], item['date']))
                logger.warn(unicode(e))
                continue
        logger.info("{} items processed, {} created, {} updated, {} errors".format(counter, self._count_created, self._count_updated, self._count_error))

    def _generate_uid(self, item):
        """
        UIDs for questions are of the form 'question-09.10.2013-1-e' (question-<date>-<number>-<lang>)
        """
        number_re = ur'Q.\s?(?P<number>\d{1,2})\s?\(?(?P<qtype>\w+)\)?'
        date = item['date']
        match = re.search(number_re, item['number_and_type'], re.UNICODE)
        if match is None:
            raise RuntimeError(u'Could not parse number and type of question from {}'.format(item['number_and_type']))
        matches = match.groupdict()
        number = matches['number']
        lang = item['language'].lower()
        return u'question-{}-{}-{}'.format(date, number, lang)
