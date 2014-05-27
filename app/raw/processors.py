"""
Helpers to load the Scrapy JSON output into RawModels
"""
import copy
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import json
import os
import re


def file_wrapper(fp):
    """
    Yields parsed JSON objects from a line separated JSON file
    """
    if isinstance(fp, basestring):
        with open(fp, 'rb') as fp:
            for line in fp:
                yield json.loads(line)
    else:
        for line in fp:
            yield json.loads(line)


def get_items_file(spider, job_id):
    """
    Return the absolute path for an Items file output by scrapy
    """
    items_folder = getattr(settings, 'SCRAPYD_ITEMS_PATH', None)
    if items_folder is None:
        raise ImproperlyConfigured("No SCRAPY_ITEMS_PATH defined")

    spider_folder = os.path.join(items_folder, 'legcoscraper', spider)
    # extension is either .jl or .json
    file_path = os.path.join(spider_folder, job_id + '.jl')
    if not os.path.exists(file_path):
        file_path = os.path.join(spider_folder, job_id + '.json')
        if not os.path.exists(file_path):
            raise RuntimeError("Could not find items file at {}".format(file_path))
    return file_path


def get_file_path(rel_path):
    """
    Given a relative path for a file downloaded by scrapy, get the absolute path
    """
    files_folder = getattr(settings, 'SCRAPYD_FILES_PATH', None)
    if files_folder is None:
        raise ImproperlyConfigured("No SCRAPY_FILES_PATH defined")

    file_path = os.path.join(files_folder, rel_path)
    if not os.path.exists(file_path):
        raise RuntimeError("Could not find file at {}".format(file_path))

    return file_path


def get_processor_for_spider(spider):
    """
    Returns the function that processes the results of a spider crawl

    Not sure what the best way to store the mapping is.
    """
    pass


class LibraryAgendaProcessor(object):
    """
    Class that handles the loading of Library Agenda scraped items into the RawCouncilAgenda table
    """
    def __init__(self, items_file_path, job=None):
        self.items_file_path = items_file_path
        self.job = job  # The ScrapeJob, if available

    def process(self, *args, **kwargs):
        for item in file_wrapper(self.items_file_path):
            if item['type'] == 'LibraryResultPage':
                # Ignore these entries
                pass
            if item['type'] == 'LibraryAgenda':
                # Filter out ombudsman agendas
                if 'Ombudsman' not in item['title_en']:
                    self._process_agenda_item(item)

    def _process_agenda_item(self, item):
        # Should generate two items, one for Chinese and one for English
        uid = self._generate_agenda_uid(item)
        paper_number = self._get_paper_number(item)
        if len(item['links']) != 2:
            # If there ar exactly two links, then one is English and the other Chinese
            if 'English' in item['links'][0]:
                url_en = item['links'][0][1]
                url_cn = item['links'][1][1]
            else:
                url_en = item['links'][1][1]
                url_cn = item['links'][0][1]
        else:
            url_en, url_cn = self._filter_links(item['links'])

    def _filter_links(self, links_array):
        """
        Given an array of links, return a tuple of the English and Chinese urls
        """
        res = []
        # Filter out titles with "Appendix", "Annex" and "fu jian"
        # Sometimes there are (Internet) versions.  Not sure what these mean
        # Sometimes there are additional document with ID number beginning "CB"
        filters = [u'App', u'Annex', u'CB', u'Internet',
                   u'\u9644\u9304', u'\u9644\u4ef6', u'\u7db2\u4e0a\u7248']
        for l in links_array:
            for f in filters:
                if f in l[0]:
                    continue
            res.append(l)

        if len(res) != 2:
            # Still couldn't get down to two URLs
            return None, None
        if 'English' in res[0][0]:
            return res[0][1], res[1][1]
        else:
            return res[1][1], res[0][1]

    def _generate_base_agenda_uid(self, item):
        """
        Try to generate a unique id for an agenda item
        ex: council_agenda-19950110-e
        Basically council_agenda-<date: YYYYMMDD>-<lang>
        e for English, c for Chinese

        We leave out the language prefix, since each item has both languages
        """
        date = item['title_en'][-11:].replace('.', '')
        return 'council_agenda-{}'.format(date)

    def _get_paper_number(self, item):
        """
        Extracts the LegCo paper number from the item

        Seems like there are some inconsistencies in the paper number.  Missing spaces, etc.
        A single date, 1996.05.22 has the Chinese document listed first, instead of second

        """
        # Even if there are appendices, they are never the first link (at the moment)
        link_title = item['links'][0][0]
        # Each paper number is followed by " (<lang>)", but can also have
        # other parenthesis, so we have to filter for parenthesis with non-digit contents
        return re.split(ur'\([\D]', link_title, 0, re.UNICODE)[0].strip()


"""
Some scripts for testing

from raw import processors, models
a = models.ScrapeJob.objects.latest_complete_job('library_agenda')
fp = processors.file_wrapper(processors.get_items_file(a.spider, a.job_id))
items = [xx for xx in fp if xx['type'] == 'LibraryAgenda' and 'Ombudsman' not in xx['title_en']]
multi = [xx for xx in items if len(xx['links']) != 2]
foo = processors.LibraryAgendaProcessor('foo')

[foo._get_paper_number(xx) for xx in items]
[foo._filter_links(xx) for xx in multi]

"""
