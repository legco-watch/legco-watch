"""
Helpers to load the Scrapy JSON output into RawModels
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import now
import json
import logging
import os
import re
import warnings
from raw.models import RawCouncilAgenda, LANG_EN, LANG_CN, RawMember, GENDER_M, GENDER_F


logger = logging.getLogger('legcowatch')


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


def get_processor_for_spider(spider):
    """
    Returns the function that processes the results of a spider crawl

    Not sure what the best way to store the mapping is.
    """
    proc = PROCESS_MAP.get(spider, None)
    if proc is None:
        raise RuntimeError("Invalid spider {}".format(spider))

    return proc


class BaseProcessor(object):
    """
    Base clase for processing lists of scraped Items and inserting them into the database

    Subclasses should implement a process method
    """
    def __init__(self, items_file_path, job=None):
        self.items_file_path = items_file_path
        self.job = job  # The ScrapeJob, if available
        self._count_created = 0
        self._count_updated = 0


class LibraryAgendaProcessor(BaseProcessor):
    """
    Class that handles the loading of Library Agenda scraped items into the RawCouncilAgenda table
    """
    def process(self, *args, **kwargs):
        logger.info("Processing file {}".format(self.items_file_path))
        counter = 0
        for item in file_wrapper(self.items_file_path):
            counter += 1
            if item['type'] == 'LibraryResultPage':
                # Ignore these entries
                pass
            if item['type'] == 'LibraryAgenda':
                # Filter out ombudsman agendas
                if 'Ombudsman' not in item['title_en']:
                    self._process_agenda_item(item)
        logger.info("{} items processed, {} created, {} updated".format(counter, self._count_created, self._count_updated))

    def _process_agenda_item(self, item):
        # Should generate two items, one for Chinese and one for English
        uid = self._generate_base_agenda_uid(item)
        paper_number = self._get_paper_number(item)
        if len(item['links']) == 2:
            # If there ar exactly two links, then one is English and the other Chinese
            if 'English' in item['links'][0][0]:
                title_en, url_en = item['links'][0]
                title_cn, url_cn = item['links'][1]
            else:
                title_en, url_en = item['links'][1]
                title_cn, url_cn = item['links'][0]
        else:
            en, cn = self._filter_links(item['links'])
            title_en, url_en = en
            title_cn, url_cn = cn

        # Finally, get the local file names
        local_en = self._get_local_filename(url_en, item)
        local_cn = self._get_local_filename(url_cn, item)

        # Try to get an existing record
        obj_en = self._get_agenda_record(uid, 'e')
        if obj_en is not None:
            obj_en = self._build_obj(obj_en, title_en, paper_number, LANG_EN, url_en, local_en, item)
            obj_en.save()

        obj_cn = self._get_agenda_record(uid, 'c')
        if obj_cn is not None:
            obj_cn = self._build_obj(obj_cn, title_cn, paper_number, LANG_CN, url_cn, local_cn, item)
            obj_cn.save()

    def _build_obj(self, obj, title, paper_number, language, url, local_file, item):
        obj.title = title
        obj.paper_number = paper_number
        obj.language = language
        obj.url = url
        obj.local_filename = local_file
        obj.crawled_from = item['source_url']
        obj.last_parsed = now()
        if self.job:
            obj.last_crawled = self.job.completed
        return obj

    def _get_agenda_record(self, uid, lang):
        if lang == 'e':
            uid += '-e'
        elif lang == 'c':
            uid += '-c'
        else:
            raise RuntimeError("Lang must be 'c' or 'e', got {}".format(lang))

        try:
            obj = RawCouncilAgenda.objects.get(uid=uid)
            self._count_updated += 1
        except RawCouncilAgenda.DoesNotExist:
            obj = RawCouncilAgenda(uid=uid)
            self._count_created += 1
        except RawCouncilAgenda.MultipleObjectsReturned:
            warnings.warn("Found more than one item with raw id {}".format(uid), RuntimeWarning)
            obj = None

        return obj

    def _get_local_filename(self, link, item):
        """
        Given a link and an item to which the link belongs, get the local file path that
        matches the link
        """
        for f in item['files']:
            if link == f['url']:
                return f['path']
        return None

    def _filter_links(self, links_array):
        """
        Given an array of links, return the English and Chinese link tuples
        So return signature is [EN Name, EN link], [CN Name, CN Link]
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
                    break
            else:
                res.append(l)

        if len(res) != 2:
            # Still couldn't get down to two URLs
            return None, None
        if 'English' in res[0][0]:
            return res[0], res[1]
        else:
            return res[1], res[0]

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


class LibraryMemberProcessor(BaseProcessor):
    """
    Processes the results of a library_member spider crawl.
    The crawl results in an item for each member/language bio combination, so each member
    will have two items, one for English, one for Chinese.
    This will create RawMember items for each member and combine these records
    """
    def process(self, *args, **kwargs):
        logger.info("Processing file {}".format(self.items_file_path))
        counter = 0
        for item in file_wrapper(self.items_file_path):
            counter += 1
            self._process_member(item)
        logger.info("{} items processed, {} created, {} updated".format(counter, self._count_created, self._count_updated))

    def _process_member(self, item):
        uid = self._generate_uid(item)
        obj = self._get_member_object(uid)
        if obj is None:
            logger.warn(u'Could not process member item: {}'.format(item))
            return
        obj.last_parsed = now()

        lang = item[u'language']
        if lang == 'e':
            # English only items
            keys_to_copy = [u'year_of_birth', u'place_of_birth', u'homepage']
            for k in keys_to_copy:
                val = item.get(k, None)
                if val is not None:
                    setattr(obj, k, val.strip())
            if item[u'gender'] == u'M':
                obj.gender = GENDER_M
            else:
                obj.gender = GENDER_F
            obj.photo_file = item[u'files'][0][u'path']
            obj.crawled_from = item[u'source_url']
            if self.job:
                obj.last_crawled = self.job.completed

        # All other items
        keys_to_copy = [u'name', u'title', u'honours']
        for k in keys_to_copy:
            target = k + '_e'
            val = item.get(k, None)
            if val is not None:
                setattr(obj, target, val.strip())

        json_objects_to_copy = [u'service', u'education', u'occupation']
        for k in json_objects_to_copy:
            val = item.get(k, None)
            if val is not None:
                setattr(obj, k, json.dumps(val))

        obj.save()

    def _get_member_object(self, uid):
        try:
            obj = RawMember.objects.get(uid=uid)
            self._count_updated += 1
        except RawMember.DoesNotExist:
            obj = RawMember(uid=uid)
            self._count_created += 1
        except RawMember.MultipleObjectsReturned:
            warnings.warn("Found more than one item with raw id {}".format(uid), RuntimeWarning)
            obj = None

        return obj

    def _generate_uid(self, item):
        """
        Generate a uid for members
        The library database already has an internal ID for each member
        We can use these for now, until we can think of a better one
        ex: member-<library_id>
        """
        pattern = ur'member_detail.aspx\?id=(\d+)'
        url = item.get('source_url', None)
        if url is None:
            logger.warn('Could not generate uid, no source url')
        match = re.search(pattern, url)
        if match is None:
            logger.warn('Could not generate uid, url did not match: {}'.format(url))
        uid = match.group(1)
        return 'member-{}'.format(uid)


PROCESS_MAP = {
    'library_agenda': LibraryAgendaProcessor,
    'library_member': LibraryMemberProcessor
}

"""
Some scripts for testing

from raw import processors, models
a = models.ScrapeJob.objects.latest_complete_job('library_agenda')
fp = processors.file_wrapper(processors.get_items_file(a.spider, a.job_id))
items = [xx for xx in fp if xx['type'] == 'LibraryAgenda' and 'Ombudsman' not in xx['title_en']]
multi = [xx for xx in items if len(xx['links']) != 2]
foo = processors.LibraryAgendaProcessor('foo')

[foo._get_paper_number(xx) for xx in items]
[foo._filter_links(xx['links']) for xx in multi]


from raw import processors, models
job = models.ScrapeJob.objects.latest_complete_job('library_agenda')
items_file = processors.get_items_file(job.spider, job.job_id)
proc = processors.LibraryAgendaProcessor(items_file, job)
proc.process()

from raw import processors, models
items_file = processors.file_wrapper('members.jl')
items = [xx for xx in items_file]
proc = processors.LibraryMemberProcessor('members.jl')
uids = [proc._generate_uid(xx) for xx in items]
"""
