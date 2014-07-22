from django.utils.timezone import now
import logging
import re
import warnings
from raw.models import RawCouncilAgenda, LANG_EN, LANG_CN, RawMember, GENDER_M, GENDER_F
from raw.processors.base import BaseProcessor, file_wrapper


logger = logging.getLogger('legcowatch')


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

