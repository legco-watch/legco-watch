"""
Helpers to load the Scrapy JSON output into RawModels
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import json
import os


def file_wrapper(fp):
    """
    Yields parsed JSON objects from a line separated JSON file
    """
    if isinstance(fp, basestring):
        fp = open(fp, 'rb')

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
        self.job = job # The ScrapeJob, if available

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
            pass
        else:
            # Otherwise, there are appendices, and we have ot try to filter these out
            pass

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
        link_title = item['links'][0][0]
        pass