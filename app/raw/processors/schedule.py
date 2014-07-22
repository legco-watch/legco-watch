from datetime import datetime
import logging
import warnings
from raw.models import RawScheduleMember
from raw.processors.base import BaseProcessor, file_wrapper


logger = logging.getLogger('legcowatch')


class ScheduleMemberProcessor(BaseProcessor):
    """
    Class that handles the loading of Library Agenda scraped items into the RawCouncilAgenda table
    """
    def process(self, *args, **kwargs):
        logger.info("Processing file {}".format(self.items_file_path))
        counter = 0
        for item in file_wrapper(self.items_file_path):
            counter += 1
            self._process_item(item)
        logger.info("{} items processed, {} created, {} updated".format(counter, self._count_created, self._count_updated))

    def _process_item(self, item):
        uid = self._generate_uid(item)
        obj = self._get_object(uid)
        if obj is None:
            logger.warn(u'Could not process member item: {}'.format(item))
            return
        obj.last_parsed = datetime.now()
        if self.job is not None:
            obj.last_crawled = self.job.completed

        fields = ['last_name_c', 'first_name_c', 'last_name_e', 'first_name_e', 'english_name']
        for f in fields:
            setattr(obj, f, item.get(f, None))

        obj.save()

    def _get_object(self, uid):
        try:
            obj = RawScheduleMember.objects.get(uid=uid)
            self._count_updated += 1
        except RawScheduleMember.DoesNotExist:
            obj = RawScheduleMember(uid=uid)
            self._count_created += 1
        except RawScheduleMember.MultipleObjectsReturned:
            warnings.warn("Found more than one item with raw id {}".format(uid), RuntimeWarning)
            obj = None
        return obj

    def _generate_uid(self, item):
        return 'smember-{}'.format(item['id'])
