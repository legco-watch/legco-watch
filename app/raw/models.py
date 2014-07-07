from django.db import models
from raw import utils
from raw.docs.agenda import CouncilAgenda


LANG_CN = 1
LANG_EN = 2
LANG_CHOICES = (
    (LANG_CN, 'Chinese'),
    (LANG_EN, 'English')
)


class ScrapeJobManager(models.Manager):
    def pending_jobs(self):
        """
        Returns the jobs that are still at the scraper
        """
        return self.filter(completed=None)

    def complete_jobs(self):
        """
        Jobs that have been completed
        """
        return self.exclude(completed=None)

    def latest_complete_job(self, spider):
        """
        Latest complete job for a single spider
        """
        return self.filter(spider=spider).exclude(completed=None).latest('completed')

    def unprocessed_jobs(self):
        """
        Returns jobs that have been completed by the scraper, but have not yet been loaded
        into the raw models.  There may be more than one job per spider
        """
        return self.exclude(completed=None).filter(last_fetched=None).order_by('-completed')

    def latest_unprocessed_job(self, spider):
        """
        Gets the latest unprocessed job for a single spider
        """
        return self.filter(spider=spider).exclude(completed=None).filter(last_fetched=None).latest('completed')

    def orphaned_jobs(self):
        """
        Returns jobs that are somehow malformed.  This includes jobs:
          - That are marked as completed but do not have a corresponding items file on disk
        """
        pass


class ScrapeJob(models.Model):
    """
    A call to the Scrapyd server for a job
    """
    spider = models.CharField(max_length=100)
    scheduled = models.DateTimeField()
    job_id = models.CharField(max_length=100)
    raw_response = models.TextField()
    completed = models.DateTimeField(null=True, blank=True)
    last_fetched = models.DateTimeField(null=True, blank=True)

    objects = ScrapeJobManager()

    def __unicode__(self):
        return u"{}: {}".format(self.spider, self.job_id)


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

    class Meta:
        abstract = True


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

    def __unicode__(self):
        return unicode(self.uid)

    def full_local_filename(self):
        return utils.get_file_path(self.local_filename)

    def get_parser(self):
        """
        Returns the parser for this RawCouncilAgenda object
        """
        full_file = self.full_local_filename()
        filetype = utils.check_file_type(full_file)
        if filetype == utils.DOCX:
            src = utils.docx_to_html(full_file)
        elif filetype == utils.DOC:
            src = utils.doc_to_html(full_file)
        else:
            raise NotImplementedError(u"Unexpected filetype for uid {}".format(self.uid))
        return CouncilAgenda(self.uid, src)

    @classmethod
    def get_from_parser(cls, parser):
        """
        Get a model object from a CouncilAgenda parser object
        """
        return cls.objects.get(uid=parser.uid)


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


class RawCouncilQuestion(RawModel):
    """
    Storage for Members' questions, from http://www.legco.gov.hk/yr13-14/english/counmtg/question/ques1314.htm#toptbl
    """
    raw_date = models.CharField(max_length=50, blank=True)
    # Q. 5 <br> (Oral), for example
    number_and_type = models.CharField(max_length=255, blank=True)
    raised_by = models.CharField(max_length=255, blank=True)
    subject = models.TextField(blank=True)
    # Link to the agenda anchor with the text of the question
    subject_link = models.URLField(blank=True)
    reply_link = models.URLField(blank=True)
    language = models.IntegerField(null=True, blank=True, choices=LANG_CHOICES)


class RawMember(RawModel):
    name_e = models.CharField(max_length=100, blank=True)
    name_c = models.CharField(max_length=100, blank=True)
