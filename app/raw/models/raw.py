import logging
from datetime import date
from django.db import models
from django.db.models import Count
from django.utils.encoding import force_unicode
import re
from .. import utils
from ..docs.agenda import CouncilAgenda
from ..names import NameMatcher, MemberName


LANG_CN = 1
LANG_EN = 2
LANG_CHOICES = (
    (LANG_CN, 'Chinese'),
    (LANG_EN, 'English')
)
GENDER_M = 1
GENDER_F = 2
GENDER_CHOICES = (
    (GENDER_M, 'Male'),
    (GENDER_F, 'Female')
)


logger = logging.getLogger('legcowatch')


class RawModelManager(models.Manager):
    def get_by_uid(self, uid):
        # Try to retrieve the object by either just the numerical uid
        # or the full uid string
        if self.model.UID_PREFIX is None:
            raise RuntimeError('UID_PREFIX is not defined on {}'.format(self.model))

        if isinstance(uid, int):
            uid = '{}-{}'.format(self.model.UID_PREFIX, uid)
            obj = self.get(uid=uid)
        elif isinstance(uid, basestring):
            obj = self.get(uid=uid)
        else:
            raise RuntimeError('Invalid UID format'.format(uid))
        return obj


class RawModel(models.Model):
    """
    Abstract base class for all raw models
    Provides a few default field, like last_crawled and last_parsed
    """
    # The last time that the raw data was fetched from the LegCo site
    last_crawled = models.DateTimeField(null=True, blank=True)
    # the last time this RawModel was parsed by a parser
    last_parsed = models.DateTimeField(null=True, blank=True)
    # A unique identifier for this type of item
    # We try to generate these as early as possible, but don't enforce a uniqueness constraint
    # for flexibility
    uid = models.CharField(max_length=100, blank=True)
    # Page from which the Item was crawled
    crawled_from = models.TextField(blank=True)

    UID_PREFIX = None
    objects = RawModelManager()

    class Meta:
        abstract = True
        app_label = 'raw'


class RawCouncilAgenda(RawModel):
    """
    Storage of Scrapy items relating to LegCo agenda items

    Should be from the Library Site: http://library.legco.gov.hk:1080/search~S10?/tAgenda+for+the+meeting+of+the+Legislative+Council/tagenda+for+the+meeting+of+the+legislative+council/1%2C670%2C670%2CB/browse
    """
    # Title of the document.  Should be "Agenda of the meeting of the Legislative Council, <date>"
    title = models.CharField(max_length=255, blank=True)
    # The LegCo paper number.  Should be "OP <number>" for pre-1997 agendas, or "A <sessionumber>" for later agendas
    paper_number = models.CharField(max_length=50, blank=True)
    language = models.IntegerField(null=True, blank=True, choices=LANG_CHOICES)
    # The URL link to the agenda document
    url = models.TextField(blank=True)
    # The name of the file saved locally on disk in the scrapy download path
    # Don't use FilePathField or FileField, since those are more for user input via forms
    local_filename = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-uid']

    def __unicode__(self):
        return unicode(self.uid)

    def full_local_filename(self):
        return utils.get_file_path(self.local_filename)

    def get_source(self):
        full_file = self.full_local_filename()
        filetype = utils.check_file_type(full_file)
        if filetype == utils.DOCX:
            src = utils.docx_to_html(full_file)
        elif filetype == utils.DOC:
            src = utils.doc_to_html(full_file)
        else:
            raise NotImplementedError(u"Unexpected filetype for uid {}".format(self.uid))
        return src

    def get_parser(self):
        """
        Returns the parser for this RawCouncilAgenda object
        """
        src = self.get_source()
        return CouncilAgenda(self.uid, src)

    @classmethod
    def get_from_parser(cls, parser):
        """
        Get a model object from a CouncilAgenda parser object
        """
        return cls.objects.get(uid=parser.uid)

    def _dump_as_fixture(self):
        """
        Saves the raw html to a fixture for testing
        """
        with open('raw/tests/fixtures/{}.html'.format(self.uid), 'wb') as f:
            f.write(self.get_source().encode('utf-8'))


class RawCouncilVoteResult(RawModel):
    """
    Storage of LegCo vote results
    Sources can be http://www.legco.gov.hk/general/english/open-legco/cm-201314.html or
    http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1314.htm
    """
    # Some meetings span two days, which is why the raw date is a string
    raw_date = models.CharField(max_length=50, blank=True)
    # URL to the XML file
    xml_url = models.URLField(null=True, blank=True)
    # local filename of the saved XML in the scrapy folder
    xml_filename = models.CharField(max_length=255, blank=True)
    # URL to the PDF file
    pdf_url = models.URLField(null=True, blank=True)
    # local filename of the saved PDF in the scrapy folder
    pdf_filename = models.CharField(max_length=255, blank=True)


class RawCouncilHansard(RawModel):
    """
    Storage of LegCo hansard documents
    Sources can be Library: http://library.legco.gov.hk:1080/search~S10?/tHong+Kong+Hansard/thong+kong+hansard/1%2C3690%2C3697%2CB/browse
    or http://www.legco.gov.hk/general/english/counmtg/yr12-16/mtg_1314.htm
    """
    title = models.CharField(max_length=255, blank=True)
    paper_number = models.CharField(max_length=50, blank=True)
    language = models.IntegerField(null=True, blank=True, choices=LANG_CHOICES)
    url = models.URLField(blank=True)
    local_filename = models.CharField(max_length=255, blank=True)


class RawMember(RawModel):
    name_e = models.CharField(max_length=100, blank=True)
    name_c = models.CharField(max_length=100, blank=True)
    title_e = models.CharField(max_length=100, blank=True)
    title_c = models.CharField(max_length=100, blank=True)
    # In most cases, it looks like the honours are the same
    # in both E and C versions, but there are a few exceptions
    # So save both for now and combine them later
    honours_e = models.CharField(max_length=50, blank=True)
    honours_c = models.CharField(max_length=50, blank=True)
    # For these, we'll assume that Chinese and English
    # contain the same information, so just keep one
    gender = models.IntegerField(null=True, blank=True, choices=GENDER_CHOICES)
    year_of_birth = models.IntegerField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=50, blank=True)
    homepage = models.TextField(blank=True)
    photo_file = models.TextField(blank=True)
    # Below are stored as JSON objects
    service_e = models.TextField(blank=True)
    service_c = models.TextField(blank=True)
    education_e = models.TextField(blank=True)
    education_c = models.TextField(blank=True)
    occupation_e = models.TextField(blank=True)
    occupation_c = models.TextField(blank=True)

    UID_PREFIX = 'member'

    not_overridable = ['service_e', 'service_c', 'photo_file']

    def __unicode__(self):
        return u"{} {}".format(unicode(self.name_e), unicode(self.name_c))

    def get_raw_schedule_member(self):
        try:
            # member-<#> to smember-<#>
            return RawScheduleMember.objects.get(uid='s' + self.uid)
        except RawMember.DoesNotExist:
            return None

    def get_name_object(self, english=True):
        if english:
            return MemberName(self.name_e)
        else:
            return MemberName(self.name_c)

    @classmethod
    def get_matcher(cls, english=True):
        """
        Returns an instance of NameMatcher that is populated with all of the names in the database
        for use when trying to match plain text names against Member entities
        """
        all_members = cls.objects.all()
        names = [(xx.get_name_object(english), xx) for xx in all_members]
        matcher = NameMatcher(names)
        return matcher

    @classmethod
    def get_members_with_questions(cls):
        return cls.objects.annotate(num_q=Count('raw_questions')).filter(num_q__gt=0)


class RawCouncilQuestion(RawModel):
    """
    Storage for Members' questions, from http://www.legco.gov.hk/yr13-14/english/counmtg/question/ques1314.htm#toptbl
    """
    raw_date = models.CharField(max_length=50, blank=True)
    # Q. 5 <br> (Oral), for example
    number_and_type = models.CharField(max_length=255, blank=True)
    raw_asker = models.CharField(max_length=255, blank=True)
    asker = models.ForeignKey(RawMember, blank=True, null=True, related_name='raw_questions')
    subject = models.TextField(blank=True)
    # Link to the agenda anchor with the text of the question
    subject_link = models.TextField(blank=True)
    reply_link = models.TextField(blank=True)
    language = models.IntegerField(null=True, blank=True, choices=LANG_CHOICES)

    UID_PREFIX = 'question'
    DATE_RE = ur'(?P<day>\d{1,2})\.(?P<mon>\d{1,2})\.(?P<year>\d{2,4})'

    class Meta:
        ordering = ['-raw_date']

    def __unicode__(self):
        if self.asker_id is None:
            return u'{} on {}'.format(force_unicode(self.raw_asker), force_unicode(self.raw_date))
        else:
            return u'{} on {}'.format(force_unicode(self.asker), force_unicode(self.raw_date))

    @property
    def date(self):
        match = re.match(self.DATE_RE, self.raw_date)
        if match is None:
            return None
        groups = match.groupdict()
        return date(int(groups['year']), int(groups['mon']), int(groups['day']))


class RawScheduleMember(RawModel):
    """
    Member records from the Schedule API
    """
    last_name_c = models.CharField(max_length=100, blank=True)
    first_name_c = models.CharField(max_length=100, blank=True)
    last_name_e = models.CharField(max_length=100, blank=True)
    first_name_e = models.CharField(max_length=100, blank=True)
    english_name = models.CharField(max_length=100, blank=True)

    UID_PREFIX = 'smember'

    def __unicode__(self):
        return u"{} {} {} {} {}".format(
            self.uid,
            self.last_name_c, self.first_name_c,
            self.first_name_e, self.last_name_e
        )

    @property
    def name_c(self):
        return u'{}{}'.format(self.last_name_c, self.first_name_c)

    @property
    def name_e(self):
        first_name = self.english_name if self.english_name != '' else self.first_name_e
        return u'{} {}'.format(first_name, self.last_name_e)

    def get_raw_member(self):
        try:
            # smember-<#> to member-<#>
            return RawMember.objects.get(uid=self.uid[1:])
        except RawMember.DoesNotExist:
            return None


class RawCommittee(RawModel):
    code = models.CharField(max_length=100, blank=True)
    name_e = models.TextField(blank=True)
    name_c = models.TextField(blank=True)
    url_e = models.TextField(blank=True)
    url_c = models.TextField(blank=True)

    UID_PREFIX = 'committee'

    def __unicode__(self):
        return u'{} {}'.format(unicode(self.uid), unicode(self.name_e))


class RawCommitteeMembership(RawModel):
    membership_id = models.IntegerField(null=True, blank=True)
    _member_id = models.IntegerField(null=True, blank=True)
    member = models.ForeignKey(RawScheduleMember, null=True, blank=True, related_name='memberships')
    _committee_id = models.IntegerField(null=True, blank=True)
    committee = models.ForeignKey(RawCommittee, null=True, blank=True, related_name='memberships')
    post_e = models.CharField(max_length=100, blank=True)
    post_c = models.CharField(max_length=100, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    UID_PREFIX = 'cmembership'

    def __unicode__(self):
        if self.member is not None:
            member = unicode(self.member)
        else:
            member = self._member_id
        if self.committee is not None:
            committee = unicode(self.committee)
        else:
            committee = self._committee_id
        return u'{} {}'.format(member, committee)


class RawMeeting(RawModel):
    meeting_id = models.IntegerField(null=True, blank=True)
    # This is the primary key in the council's table
    slot_id = models.IntegerField(null=True, blank=True)
    committees = models.ManyToManyField(RawCommittee, null=True, blank=True, related_name='meetings')
    subject_e = models.TextField(blank=True)
    subject_c = models.TextField(blank=True)
    agenda_url_e = models.TextField(blank=True)
    agenda_url_c = models.TextField(blank=True)
    venue_code = models.CharField(max_length=50, blank=True)
    meeting_type = models.CharField(max_length=50, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)

    UID_PREFIX = 'meeting'

    def __unicode__(self):
        return u'{} {}'.format(self.uid, self.subject_e)


class RawMeetingCommittee(RawModel):
    slot_id = models.IntegerField(null=True, blank=True)
    _committee_id = models.IntegerField(null=True, blank=True)
    committee = models.ForeignKey(RawCommittee, null=True, blank=True, related_name='meeting_committees')

    def __unicode__(self):
        return u'{} {}'.format(self.slot_id, self._committee_id)
