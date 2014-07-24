from datetime import datetime
import logging
import warnings

from raw.models import RawScheduleMember, RawCommittee, RawCommitteeMembership, RawMeetingCommittee
from raw.processors.base import BaseProcessor, file_wrapper


logger = logging.getLogger('legcowatch')


class BaseScheduleProcessor(BaseProcessor):
    # Doing some refactoring, but don't want to affect other processors
    model = None

    def process(self, *args, **kwargs):
        logger.info("Processing file {}".format(self.items_file_path))
        counter = 0
        for item in file_wrapper(self.items_file_path):
            counter += 1
            self._process_item_wrapper(item)
        logger.info("{} items processed, {} created, {} updated".format(counter, self._count_created, self._count_updated))

    def _process_item(self, item, obj):
        raise NotImplementedError()

    def _process_item_wrapper(self, item):
        uid = self._generate_uid(item)
        obj = self._get_object(uid)
        if obj is None:
            logger.warn(u'Could not process member item: {}'.format(item))
            return
        obj.last_parsed = datetime.now()
        if self.job is not None:
            obj.last_crawled = self.job.completed
        self._process_item(item, obj)

    def _get_object(self, uid):
        try:
            obj = self.model.objects.get(uid=uid)
            self._count_updated += 1
        except self.model.DoesNotExist:
            obj = self.model(uid=uid)
            self._count_created += 1
        except self.model.MultipleObjectsReturned:
            warnings.warn("Found more than one item with raw id {}".format(uid), RuntimeWarning)
            obj = None
        return obj

    def _generate_uid(self, item):
        raise NotImplementedError()


class ScheduleMemberProcessor(BaseScheduleProcessor):
    """
    Class that handles the loading of Library Agenda scraped items into the RawCouncilAgenda table
    """
    model = RawScheduleMember

    def _process_item(self, item, obj):
        fields = ['last_name_c', 'first_name_c', 'last_name_e', 'first_name_e', 'english_name']
        for f in fields:
            setattr(obj, f, item.get(f, None))
        obj.save()

    def _generate_uid(self, item):
        return 'smember-{}'.format(item['id'])


class ScheduleCommitteeProcessor(BaseScheduleProcessor):
    model = RawCommittee

    def _process_item(self, item, obj):
        fields = ['code', 'name_e', 'name_c', 'url_e', 'url_c']
        for f in fields:
            setattr(obj, f, item.get(f, None))
        obj.save()

    def _generate_uid(self, item):
        return 'committee-{}'.format(item['id'])


class ScheduleMeetingCommitteeProcessor(BaseScheduleProcessor):
    model = RawMeetingCommittee

    def _process_item(self, item, obj):
        obj.slot_id = int(item['slot_id'])
        cid = int(item['committee_id'])
        obj._committee_id = cid
        try:
            cuid = 'committee-{}'.format(cid)
            committee = RawCommittee.objects.get(uid=cuid)
        except RawCommittee.DoesNotExist:
            logger.warn('Could not find committee {}'.format(cuid))
            committee = None
        obj.committee = committee
        obj.save()

    def _generate_uid(self, item):
        return 'meeting_committee-{}'.format(item['id'])


class ScheduleMembershipProcessor(BaseScheduleProcessor):
    model = RawCommitteeMembership

    def _process_item(self, item, obj):
        fields = ['post_e', 'post_c']
        for f in fields:
            setattr(obj, f, item.get(f, None))
        obj.membership_id = int(item['membership_id'])

        # Parse the dates
        fmt = '%Y-%m-%dT%H:%M:%S'
        start_date = item.get('start_date', None)
        if start_date is not None:
            start_date = datetime.strptime(start_date, fmt)
        obj.start_date = start_date

        end_date = item.get('end_date', None)
        if end_date is not None:
            end_date = datetime.strptime(end_date, fmt)
        obj.end_date = end_date

        # Try to find the member and committee objects
        mid = int(item['member_id'])
        obj._member_id = mid
        try:
            muid = 'smember-{}'.format(mid)
            member = RawScheduleMember.objects.get(uid=muid)
        except RawScheduleMember.DoesNotExist:
            logger.warn('Could not find member {}'.format(muid))
            member = None
        obj.member = member

        cid = int(item['committee_id'])
        obj._committee_id = cid
        try:
            cuid = 'committee-{}'.format(cid)
            committee = RawCommittee.objects.get(uid=cuid)
        except RawCommittee.DoesNotExist:
            # Seems like there are actually a large number
            # of committees that are referenced in the Membership table
            # but are not in the Committee table
            logger.warn('Could not find committee {}'.format(cuid))
            committee = None
        obj.committee = committee
        obj.save()

    def _generate_uid(self, item):
        return 'cmembership-{}'.format(item['id'])
