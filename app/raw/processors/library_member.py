from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.timezone import now
import json
import logging
import os
import re
import shutil
import warnings
from raw.models import RawCouncilAgenda, LANG_EN, LANG_CN, RawMember, GENDER_M, GENDER_F
from raw import utils
from raw.processors.base import BaseProcessor, file_wrapper


logger = logging.getLogger('legcowatch')


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
            # Copy and rename the photo to the app
            # Unless it is the generic photo
            if 'photo.jpg' not in item[u'files'][0][u'url']:
                try:
                    source_photo_path = utils.get_file_path(item[u'files'][0][u'path'])
                    new_photo_path = 'member_photos/{}.jpg'.format(uid)
                    new_photo_abspath = os.path.abspath(os.path.join('.', 'raw', 'static', 'member_photos', '{}.jpg'.format(uid)))
                    # This should be moved up in the process, since we don't need to check if the directory exsts
                    # for each photo
                    if not os.path.exists(os.path.dirname(new_photo_abspath)):
                        os.makedirs(os.path.dirname(new_photo_abspath))
                    if not os.path.exists(new_photo_abspath) and os.path.exists(source_photo_path):
                        shutil.copyfile(source_photo_path, new_photo_abspath)
                    obj.photo_file = new_photo_path
                except RuntimeError:
                    # Photo didn't download for some reason
                    logger.warn(u'Photo for {} did not download properly to path'.format(uid, item[u'files'][0][u'path']))
            else:
                # Clear old photos
                obj.photo_file = ''
            obj.crawled_from = item[u'source_url']
            if self.job:
                obj.last_crawled = self.job.completed

        # All other items
        keys_to_copy = [u'name', u'title', u'honours']
        for k in keys_to_copy:
            target = u'{}_{}'.format(k, lang)
            val = item.get(k, None)
            if val is not None:
                setattr(obj, target, val.strip())

        json_objects_to_copy = [u'service', u'education', u'occupation']
        for k in json_objects_to_copy:
            target = u'{}_{}'.format(k, lang)
            val = item.get(k, None)
            if val is not None:
                setattr(obj, target, json.dumps(val))

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

